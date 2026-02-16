"""Pydantic models for Angebote (Quotes)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.position import PositionCreate, PositionResponse
from app.utils.enums import DocumentStatus


class AngebotCreate(BaseModel):
    """Request body for creating a quote."""
    kunde_id: UUID
    projekt_id: UUID | None = None
    datum: date | None = None
    gueltig_bis: date | None = None
    einleitungstext: str | None = None
    schlusstext: str | None = None
    positionen: list[PositionCreate]


class AngebotResponse(BaseModel):
    """Response model for a quote."""
    id: UUID
    dokumentennummer: str
    status: DocumentStatus
    kunde_id: UUID
    projekt_id: UUID | None = None
    datum: date
    netto_summe: Decimal
    mwst_betrag: Decimal
    brutto_summe: Decimal
    einleitungstext: str | None = None
    schlusstext: str | None = None
    positionen: list[PositionResponse] = []
    pdf_url: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
