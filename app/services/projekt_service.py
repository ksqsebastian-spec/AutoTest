"""Service layer for Projekte (Construction Projects)."""

from datetime import date
from uuid import UUID

from supabase import Client

from app.models.projekt import ProjektCreate, ProjektUpdate


async def generate_projektnummer(db: Client) -> str:
    """Generate the next sequential project number (P-2026-001)."""
    jahr = date.today().year
    result = (
        db.table("projekte")
        .select("projektnummer")
        .ilike("projektnummer", f"P-{jahr}-%")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if result.data:
        last = result.data[0]["projektnummer"]
        num = int(last.split("-")[2]) + 1
    else:
        num = 1
    return f"P-{jahr}-{num:03d}"


async def list_projekte(
    db: Client,
    page: int = 1,
    per_page: int = 25,
    kunde_id: UUID | None = None,
    status: str | None = None,
    search: str | None = None,
) -> dict:
    """List projects with pagination and optional filters."""
    query = db.table("projekte").select("*", count="exact")

    if kunde_id:
        query = query.eq("kunde_id", str(kunde_id))
    if status:
        query = query.eq("status", status)
    if search:
        query = query.or_(
            f"bezeichnung.ilike.%{search}%,"
            f"projektnummer.ilike.%{search}%,"
            f"ort.ilike.%{search}%"
        )

    query = query.order("created_at", desc=True)
    offset = (page - 1) * per_page
    query = query.range(offset, offset + per_page - 1)

    result = query.execute()
    total = result.count or 0
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return {
        "items": result.data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
    }


async def get_projekt(db: Client, projekt_id: UUID) -> dict | None:
    """Get a single project by ID."""
    result = db.table("projekte").select("*").eq("id", str(projekt_id)).execute()
    return result.data[0] if result.data else None


async def create_projekt(db: Client, data: ProjektCreate) -> dict:
    """Create a new project with auto-generated projektnummer."""
    projektnummer = await generate_projektnummer(db)
    payload = data.model_dump(exclude_none=True)
    payload["projektnummer"] = projektnummer
    payload["kunde_id"] = str(payload["kunde_id"])

    for key in ("auftragssumme", "bauabzugsteuer_prozent"):
        if key in payload:
            payload[key] = float(payload[key])

    result = db.table("projekte").insert(payload).execute()
    return result.data[0]


async def update_projekt(db: Client, projekt_id: UUID, data: ProjektUpdate) -> dict | None:
    """Update an existing project."""
    payload = data.model_dump(exclude_none=True)
    if not payload:
        return await get_projekt(db, projekt_id)

    if "kunde_id" in payload:
        payload["kunde_id"] = str(payload["kunde_id"])
    for key in ("auftragssumme", "bauabzugsteuer_prozent"):
        if key in payload:
            payload[key] = float(payload[key])

    result = db.table("projekte").update(payload).eq("id", str(projekt_id)).execute()
    return result.data[0] if result.data else None
