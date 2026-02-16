"""Pydantic models for Mahnungen (Dunning / Payment Reminders)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.utils.enums import Mahnstufe


class MahnungCreate(BaseModel):
    """Request body for creating a dunning notice."""
    rechnung_dokument_id: UUID
    stufe: Mahnstufe
    mahngebuehr: Decimal = Field(default=Decimal("0"), ge=0)
    verzugszinsen: Decimal = Field(default=Decimal("0"), ge=0)
    mahnfrist_tage: int = Field(default=14, ge=1)


class MahnungResponse(BaseModel):
    """Response model for a dunning notice."""
    id: UUID
    dokumentennummer: str
    stufe: Mahnstufe
    rechnung_dokument_id: UUID
    rechnung_nummer: str | None = None
    offener_betrag: Decimal
    mahngebuehr: Decimal
    verzugszinsen: Decimal
    mahnfrist: date | None = None
    faelligkeitsdatum: date
    kunde_name: str | None = None
    created_at: datetime | None = None


class MahnvorschlagResponse(BaseModel):
    """Suggestion for which invoices need dunning."""
    rechnung_id: UUID
    rechnung_nummer: str
    kunde_name: str
    brutto_summe: Decimal
    offener_betrag: Decimal
    faellig_seit_tagen: int
    aktuelle_stufe: Mahnstufe | None = None
    naechste_stufe: Mahnstufe
