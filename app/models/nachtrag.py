"""Pydantic models for Nachtraege (Change Orders)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.position import PositionCreate, PositionResponse


class NachtragCreate(BaseModel):
    """Request body for creating a change order."""
    projekt_id: UUID
    begruendung: str | None = None
    referenz_lv_id: UUID | None = None
    positionen: list[PositionCreate] = []


class NachtragResponse(BaseModel):
    """Response model for a change order."""
    id: UUID
    dokumentennummer: str
    projekt_id: UUID
    nachtragsnummer: int
    begruendung: str | None = None
    genehmigt: bool
    genehmigt_am: date | None = None
    genehmigt_von: str | None = None
    netto_summe: Decimal
    brutto_summe: Decimal
    positionen: list[PositionResponse] = []
    created_at: datetime | None = None
