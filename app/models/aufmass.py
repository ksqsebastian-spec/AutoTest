"""Pydantic models for Aufmasse (Measurement Records)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums import Einheit


class AufmassPositionCreate(BaseModel):
    """Request body for a measurement entry."""
    lv_position_id: UUID | None = None
    beschreibung: str
    formel: str | None = None
    laenge: Decimal | None = None
    breite: Decimal | None = None
    hoehe: Decimal | None = None
    anzahl: Decimal = Decimal("1")
    ergebnis: Decimal
    einheit: Einheit | None = None
    notizen: str | None = None
    sort_order: int = 0


class AufmassPositionResponse(BaseModel):
    """Response model for a measurement entry."""
    id: UUID
    aufmass_id: UUID
    lv_position_id: UUID | None = None
    beschreibung: str
    formel: str | None = None
    laenge: Decimal | None = None
    breite: Decimal | None = None
    hoehe: Decimal | None = None
    anzahl: Decimal
    ergebnis: Decimal
    einheit: Einheit | None = None
    notizen: str | None = None
    sort_order: int
    created_at: datetime | None = None


class AufmassCreate(BaseModel):
    """Request body for creating a measurement record."""
    projekt_id: UUID
    aufnahmedatum: date
    aufgenommen_von: str | None = None
    positionen: list[AufmassPositionCreate] = []


class AufmassResponse(BaseModel):
    """Response model for a measurement record."""
    id: UUID
    dokumentennummer: str
    projekt_id: UUID
    aufmass_nummer: int
    aufnahmedatum: date
    aufgenommen_von: str | None = None
    geprueft_von: str | None = None
    geprueft_am: date | None = None
    positionen: list[AufmassPositionResponse] = []
    created_at: datetime | None = None
