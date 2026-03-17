"""Domain models for the Mytho Compendium workflow scripts."""

from dataclasses import dataclass
from enum import StrEnum


class TicketStatus(StrEnum):
    """Possible lifecycle statuses of a Notion backlog ticket."""
    TO_DO = "TO DO"
    IN_PROGRESS = "IN PROGRESS"
    BLOCKED = "BLOCKED"
    IN_REVIEW = "IN REVIEW"
    IN_TESTING = "IN TESTING"
    DONE = "DONE"
    PROD = "PROD"


class TicketType(StrEnum):
    """Possible types of a Notion backlog ticket."""
    FEAT = "Feat"
    FIX = "Fix"
    REFACTOR = "Refactor"
    LEARNING = "Learning"
    DOC = "Doc"
    CHORE = "Chore"


class TicketComponent(StrEnum):
    """Possible components of a Notion backlog ticket."""
    INIT = "INIT"
    CI = "CI"
    CLOUD = "CLOUD"
    DESIGN = "DESIGN"
    FIREBASE = "FIREBASE"
    IOS = "IOS"
    KMP = "KMP"
    KTOR = "KTOR"
    LLM = "LLM"
    NEO4J = "NEO4J"
    POSTGRESQL = "POSTGRESQL"


@dataclass(frozen=True, slots=True)
class Ticket:
    """Immutable domain object representing a single Notion backlog ticket."""
    page_id: str
    ticket_id: int
    name: str
    status: TicketStatus
    ticket_type: TicketType
    component: TicketComponent
    is_in_active_sprint: bool

    @property
    def reference(self) -> str:
        """The human-readable ticket reference, e.g. GCR-11."""
        return f"GCR-{self.ticket_id}"
