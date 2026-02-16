"""Pydantic models for Leistungsverzeichnisse (Bills of Quantities)."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums import Einheit


class LVPositionCreate(BaseModel):
    """Request body for a LV line item."""
    ordnungszahl: str
    titel: str | None = None
    beschreibung: str
    einheit: Einheit = Einheit.STUECK
    menge: Decimal | None = None
    einzelpreis: Decimal | None = None
    ist_titel: bool = False
    parent_id: UUID | None = None
    sort_order: int = 0


class LVPositionResponse(BaseModel):
    """Response model for a LV line item."""
    id: UUID
    lv_id: UUID
    ordnungszahl: str
    titel: str | None = None
    beschreibung: str
    einheit: Einheit
    menge: Decimal | None = None
    einzelpreis: Decimal | None = None
    gesamtpreis: Decimal | None = None
    ist_titel: bool
    parent_id: UUID | None = None
    sort_order: int
    children: list["LVPositionResponse"] = []
    created_at: datetime | None = None


class LVCreate(BaseModel):
    """Request body for creating a Bill of Quantities."""
    projekt_id: UUID
    gewerk: str | None = None
    positionen: list[LVPositionCreate] = []


class LVResponse(BaseModel):
    """Response model for a Bill of Quantities."""
    id: UUID
    dokumentennummer: str
    projekt_id: UUID
    gewerk: str | None = None
    version: int
    positionen: list[LVPositionResponse] = []
    created_at: datetime | None = None
