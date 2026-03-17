"""Module used to handle Notion Backlog Database and ticket management."""

import logging
import os
import re

import requests
from dotenv import load_dotenv

from tools.workflow.start.dtos import NotionTicketDTO
from tools.workflow.start.models import Ticket, TicketStatus, TicketType, TicketComponent

_NOTION_API_VERSION = "2022-06-28"
_NOTION_API_BASE = "https://api.notion.com/v1"

_session: requests.Session | None = None
_notion_backlog_database_id: str | None = None

_logger = logging.getLogger(__name__)


def _get_session() -> requests.Session:
    """
    Initialize and return the shared HTTP session (lazy singleton).
    Loads environment variables from .env on first call via load_dotenv().
    Raises EnvironmentError if NOTION_TOKEN or NOTION_BACKLOG_DATABASE_ID is not set.
    """

    global _session, _notion_backlog_database_id
    if _session is None:
        load_dotenv()
        session = requests.Session()

        notion_token = os.environ.get("NOTION_TOKEN")
        if not notion_token:
            raise EnvironmentError("NOTION_TOKEN is not set. Add it to your .env file.")

        _notion_backlog_database_id = os.environ.get("NOTION_BACKLOG_DATABASE_ID")
        if not _notion_backlog_database_id:
            raise EnvironmentError("NOTION_BACKLOG_DATABASE_ID is not set. Add it to your .env file.")

        session.headers.update({
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": _NOTION_API_VERSION,
        })
        _session = session
    return _session


def _parse_ticket_id(ticket_reference: str) -> int:
    """Parse 'GCR-XX' into XX. Raises ValueError if the format is invalid."""

    match = re.fullmatch(r"GCR-(\d+)", ticket_reference)
    if not match:
        raise ValueError("ticket_reference must match format 'GCR-<number>'")
    return int(match.group(1))


def _parse_ticket(ticket_dto: NotionTicketDTO) -> Ticket:
    """Map a raw Notion page response to a Ticket domain object."""

    properties = ticket_dto["properties"]
    title = properties["Name"]["title"]
    if not title:
        raise ValueError("Ticket must have Title property")

    return Ticket(
        page_id=ticket_dto["id"],
        ticket_id=properties["Ticket ID"]["number"],
        name=title[0]["plain_text"],
        status=TicketStatus(properties["Status"]["select"]["name"]),
        ticket_type=TicketType(properties["Type"]["select"]["name"]),
        component=TicketComponent(properties["Component"]["select"]["name"]),
        is_in_active_sprint=properties["Active Sprint"]["checkbox"],
    )


def fetch_ticket(ticket_reference: str) -> Ticket:
    """Fetch a ticket from the Notion backlog by its reference (e.g. GCR-12). Raises ValueError if not found."""

    session = _get_session()

    notion_backlog_url = f"{_NOTION_API_BASE}/databases/{_notion_backlog_database_id}/query"
    ticket_id = _parse_ticket_id(ticket_reference)

    response = session.post(
        notion_backlog_url,
        json={
            "filter": {
                "property": "Ticket ID",
                "number": {
                    "equals": ticket_id
                }
            }
        },
    )

    response.raise_for_status()

    data = response.json()
    results = data["results"]
    if not results:
        raise ValueError(f"Ticket {ticket_reference} does not exist")

    ticket_dto: NotionTicketDTO = results[0]
    ticket = _parse_ticket(ticket_dto)
    _logger.info("Ticket %s fetched successfully", ticket.reference)
    return ticket


def update_ticket_status(ticket: Ticket, new_status: TicketStatus) -> None:
    """Update a ticket's status in Notion. Raises HTTPError if the request fails."""

    ticket_path = f"{_NOTION_API_BASE}/pages/{ticket.page_id}"

    response = _get_session().patch(
        ticket_path,
        json={
            "properties": {
                "Status": {
                    "select": {
                        "name": new_status,
                    }
                }
            }
        },
    )

    response.raise_for_status()

    _logger.info(
        "Ticket %s moved from %s to %s successfully",
        ticket.reference,
        ticket.status,
        new_status,
    )
