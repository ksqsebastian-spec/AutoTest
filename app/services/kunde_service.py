"""Service layer for Kunden (Customers)."""

from uuid import UUID

from supabase import Client

from app.models.kunde import KundeCreate, KundeResponse, KundeUpdate


async def generate_kundennummer(db: Client) -> str:
    """Generate the next sequential customer number (K-0001, K-0002, ...)."""
    result = (
        db.table("kunden")
        .select("kundennummer")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if result.data:
        last = result.data[0]["kundennummer"]
        num = int(last.split("-")[1]) + 1
    else:
        num = 1
    return f"K-{num:04d}"


async def list_kunden(
    db: Client,
    page: int = 1,
    per_page: int = 25,
    search: str | None = None,
    aktiv: bool | None = None,
) -> dict:
    """List customers with pagination and optional filters."""
    query = db.table("kunden").select("*", count="exact")

    if aktiv is not None:
        query = query.eq("aktiv", aktiv)

    if search:
        query = query.or_(
            f"nachname.ilike.%{search}%,"
            f"firmenname.ilike.%{search}%,"
            f"kundennummer.ilike.%{search}%,"
            f"email.ilike.%{search}%,"
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


async def get_kunde(db: Client, kunde_id: UUID) -> dict | None:
    """Get a single customer by ID."""
    result = db.table("kunden").select("*").eq("id", str(kunde_id)).execute()
    return result.data[0] if result.data else None


async def create_kunde(db: Client, data: KundeCreate) -> dict:
    """Create a new customer with auto-generated kundennummer."""
    kundennummer = await generate_kundennummer(db)
    payload = data.model_dump(exclude_none=True)
    payload["kundennummer"] = kundennummer

    # Convert Decimal fields to float for JSON
    for key in ("skonto_prozent",):
        if key in payload:
            payload[key] = float(payload[key])

    result = db.table("kunden").insert(payload).execute()
    return result.data[0]


async def update_kunde(db: Client, kunde_id: UUID, data: KundeUpdate) -> dict | None:
    """Update an existing customer."""
    payload = data.model_dump(exclude_none=True)
    if not payload:
        return await get_kunde(db, kunde_id)

    # Convert Decimal fields to float for JSON
    for key in ("skonto_prozent",):
        if key in payload:
            payload[key] = float(payload[key])

    result = (
        db.table("kunden").update(payload).eq("id", str(kunde_id)).execute()
    )
    return result.data[0] if result.data else None


async def deactivate_kunde(db: Client, kunde_id: UUID) -> dict | None:
    """Soft-delete a customer by setting aktiv=False."""
    result = (
        db.table("kunden")
        .update({"aktiv": False})
        .eq("id", str(kunde_id))
        .execute()
    )
    return result.data[0] if result.data else None
