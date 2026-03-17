"""Module used to run git commands."""

import logging
import re
import subprocess

from tools.workflow.start.models import Ticket

_logger = logging.getLogger(__name__)


def _build_branch_name(ticket: Ticket) -> str:
    """
    Parse, format and build a branch name from the ticket name.
    Returns the branch name in the format:
      <type>/GCR-<id>-<component>-<description>
      e.g. feat/GCR-11-kmp-implement-data-layer
    Raises ValueError if the ticket name is not well formatted.
    """
    ticket_name_parts = ticket.name.split(": ", 1)
    if len(ticket_name_parts) != 2:
        raise ValueError(f"Ticket name '{ticket.name}' does not respect the expected format 'Type: Description'")

    formatted_ticket_type = ticket.ticket_type.name.lower() # "FEAT" → "feat" - uses enum identifier, not Notion value
    ticket_id = ticket.ticket_id
    formatted_ticket_component = ticket.component.name.lower() # "KMP" → "kmp" uses enum identifier, not Notion value
    formatted_description = re.sub(
        r"[^a-z0-9]+",
        "-",
        ticket_name_parts[1].strip().lower(),
    ).strip("-")

    branch_name = f"{formatted_ticket_type}/GCR-{ticket_id}-{formatted_ticket_component}-{formatted_description}"
    return branch_name


def checkout_new_branch(ticket: Ticket) -> None:
    """
    Build the branch name from the ticket and create it with git checkout -b.
    Raises ValueError if the ticket name is not well formatted.
    """
    branch_name = _build_branch_name(ticket)
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    _logger.info("Switched to a new branch %s", branch_name)
