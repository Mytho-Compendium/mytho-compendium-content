"""Data Transfer Objects for the Mytho Compendium workflow scripts."""

from typing import TypedDict, Any


class NotionTicketDTO(TypedDict):
    """Partial representation of a Notion page response. Only fields consumed by the workflow scripts are declared."""
    # properties values vary by Notion property type (number, title, select, checkbox, etc.)
    # Fully typing this would require a TypedDict per property type, not worth it for a CLI script.
    id: str
    properties: dict[str, Any]
