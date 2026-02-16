"""Pydantic models for Positionen (Line Items)."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.utils.enums import Einheit, TaxRateType


class PositionBase(BaseModel):
    """Shared fields for a line item."""
    position_nr: int = Field(ge=1)
    titel: str | None = None
    beschreibung: str
    einheit: Einheit = Einheit.STUECK
    menge: Decimal = Field(ge=0)
    einzelpreis: Decimal
    steuersatz: TaxRateType = TaxRateType.STANDARD


class PositionCreate(PositionBase):
    """Request body for creating a line item."""
    pass


class PositionResponse(PositionBase):
    """Response model for a line item."""
    id: UUID
    dokument_id: UUID
    gesamt_netto: Decimal
    steuersatz_prozent: Decimal
    mwst_betrag: Decimal
    gesamt_brutto: Decimal
    aufmass_referenz: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
