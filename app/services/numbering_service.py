"""GoBD-compliant document numbering service."""

from datetime import date

from supabase import Client

from app.utils.enums import DocumentType


async def naechste_nummer(db: Client, typ: DocumentType, jahr: int | None = None) -> str:
    """
    Generate the next sequential document number.

    Uses the PostgreSQL function naechste_dokumentennummer() for atomic,
    gap-free numbering. Format: {PREFIX}-{YEAR}-{NUMBER:04d}

    Examples: RE-2026-0001, AN-2026-0042, MA-2026-0003
    """
    if jahr is None:
        jahr = date.today().year

    result = db.rpc("naechste_dokumentennummer", {"p_typ": typ.value, "p_jahr": jahr}).execute()
    return result.data
