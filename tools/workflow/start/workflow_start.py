"""Script that creates workspace and starts workflow of a specified ticket."""

import logging
import sys
from subprocess import CalledProcessError

from requests.exceptions import RequestException

from tools.workflow.shared.git import checkout_new_branch
from tools.workflow.start.models import Ticket, TicketStatus
from tools.workflow.shared.notion import fetch_ticket, update_ticket_status

_logger = logging.getLogger(__name__)


def check_is_in_active_sprint(ticket: Ticket) -> None:
    """Check if the ticket is in Active Sprint. Raises ValueError if it isn't."""
    if not ticket.is_in_active_sprint:
        raise ValueError(f"Ticket {ticket.reference} is not in Active Sprint")


def check_status_allows_start(ticket: Ticket) -> None:
    """Check if the ticket has the status: TO DO or BLOCKED. Raises ValueError if it doesn't."""
    if ticket.status not in {TicketStatus.TO_DO, TicketStatus.BLOCKED}:
        raise ValueError(f"Ticket {ticket.reference} should have status: TO DO or BLOCKED")


def main() -> None:
    """
    Start a ticket.
    Fetch the ticket by its ID in Notion Backlog Database.
    Check that the ticket is in Active Sprint. Raises ValueError if it isn't.
    Check that the ticket has the status: TO DO or BLOCKED. Raises ValueError if it isn't.
    Create a new branch based on the ticket name. Raises ValueError if the name is not well formatted.
    Move the ticket status to IN PROGRESS, by updating the Ticket Page in Notion, with its ID.
    """

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if len(sys.argv) < 2:
        _logger.error("Usage: python workflow_start.py <notion_ticket_ref>")
        sys.exit(1)

    ticket_reference = sys.argv[1]
    try:
        ticket = fetch_ticket(ticket_reference)
        check_is_in_active_sprint(ticket)
        check_status_allows_start(ticket)
        checkout_new_branch(ticket)
        update_ticket_status(ticket, TicketStatus.IN_PROGRESS)
    except (
            ValueError,
            CalledProcessError,
            RequestException,
            EnvironmentError,
    ) as error:
        _logger.error(error)
        sys.exit(1)


# Only run main() if this file was executed directly, not if it was imported.
# When Python runs a file directly (e.g. python workflow_start.py GCR-11),
# it sets a special variable __name__ to "__main__".
# When Python imports that same file from another file (e.g. in a test),
# it sets __name__ to the module name ("workflow_start") instead.

if __name__ == "__main__":
    main()
