"""Pydantic models for Kunden (Customers)."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class KundeBase(BaseModel):
    """Shared fields for customer create/update."""
    firmenname: str | None = None
    anrede: str | None = None
    vorname: str | None = None
    nachname: str
    strasse: str
    plz: str
    ort: str
    land: str = "Deutschland"
    telefon: str | None = None
    mobil: str | None = None
    email: str | None = None
    ust_id: str | None = None
    steuernummer: str | None = None
    ist_auftraggeber_bau: bool = False
    freistellungsbescheid_vorhanden: bool = False
    zahlungsziel_tage: int = Field(default=30, ge=0)
    skonto_prozent: Decimal = Field(default=Decimal("0"), ge=0)
    skonto_tage: int = Field(default=0, ge=0)
    notizen: str | None = None


class KundeCreate(KundeBase):
    """Request body for creating a customer."""
    pass


class KundeUpdate(BaseModel):
    """Request body for updating a customer. All fields optional."""
    firmenname: str | None = None
    anrede: str | None = None
    vorname: str | None = None
    nachname: str | None = None
    strasse: str | None = None
    plz: str | None = None
    ort: str | None = None
    land: str | None = None
    telefon: str | None = None
    mobil: str | None = None
    email: str | None = None
    ust_id: str | None = None
    steuernummer: str | None = None
    ist_auftraggeber_bau: bool | None = None
    freistellungsbescheid_vorhanden: bool | None = None
    zahlungsziel_tage: int | None = None
    skonto_prozent: Decimal | None = None
    skonto_tage: int | None = None
    notizen: str | None = None


class KundeResponse(KundeBase):
    """Response model for a customer."""
    id: UUID
    kundennummer: str
    aktiv: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class KundeListItem(BaseModel):
    """Compact customer for list views."""
    id: UUID
    kundennummer: str
    firmenname: str | None = None
    nachname: str
    vorname: str | None = None
    ort: str
    email: str | None = None
    aktiv: bool = True
