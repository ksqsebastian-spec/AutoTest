"""API endpoints for Kunden (Customers)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.dependencies import get_db
from app.models.kunde import KundeCreate, KundeResponse, KundeUpdate
from app.services import kunde_service

router = APIRouter(prefix="/api/kunden", tags=["Kunden"])


@router.get("")
async def list_kunden(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    search: str | None = None,
    aktiv: bool | None = None,
    db: Client = Depends(get_db),
):
    """List all customers with pagination and search."""
    return await kunde_service.list_kunden(db, page, per_page, search, aktiv)


@router.post("", status_code=201)
async def create_kunde(data: KundeCreate, db: Client = Depends(get_db)):
    """Create a new customer."""
    return await kunde_service.create_kunde(db, data)


@router.get("/{kunde_id}")
async def get_kunde(kunde_id: UUID, db: Client = Depends(get_db)):
    """Get a single customer by ID."""
    kunde = await kunde_service.get_kunde(db, kunde_id)
    if not kunde:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return kunde


@router.put("/{kunde_id}")
async def update_kunde(
    kunde_id: UUID, data: KundeUpdate, db: Client = Depends(get_db)
):
    """Update an existing customer."""
    kunde = await kunde_service.update_kunde(db, kunde_id, data)
    if not kunde:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return kunde


@router.delete("/{kunde_id}")
async def delete_kunde(kunde_id: UUID, db: Client = Depends(get_db)):
    """Soft-delete (deactivate) a customer."""
    kunde = await kunde_service.deactivate_kunde(db, kunde_id)
    if not kunde:
        raise HTTPException(status_code=404, detail="Kunde nicht gefunden")
    return {"message": "Kunde deaktiviert", "kunde": kunde}
