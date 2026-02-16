"""API endpoints for Projekte (Construction Projects)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client

from app.dependencies import get_db
from app.models.projekt import ProjektCreate, ProjektUpdate
from app.services import projekt_service

router = APIRouter(prefix="/api/projekte", tags=["Projekte"])


@router.get("")
async def list_projekte(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    kunde_id: UUID | None = None,
    status: str | None = None,
    search: str | None = None,
    db: Client = Depends(get_db),
):
    """List all projects with pagination and filters."""
    return await projekt_service.list_projekte(db, page, per_page, kunde_id, status, search)


@router.post("", status_code=201)
async def create_projekt(data: ProjektCreate, db: Client = Depends(get_db)):
    """Create a new project."""
    return await projekt_service.create_projekt(db, data)


@router.get("/{projekt_id}")
async def get_projekt(projekt_id: UUID, db: Client = Depends(get_db)):
    """Get a single project by ID."""
    projekt = await projekt_service.get_projekt(db, projekt_id)
    if not projekt:
        raise HTTPException(status_code=404, detail="Projekt nicht gefunden")
    return projekt


@router.put("/{projekt_id}")
async def update_projekt(
    projekt_id: UUID, data: ProjektUpdate, db: Client = Depends(get_db)
):
    """Update an existing project."""
    projekt = await projekt_service.update_projekt(db, projekt_id, data)
    if not projekt:
        raise HTTPException(status_code=404, detail="Projekt nicht gefunden")
    return projekt
