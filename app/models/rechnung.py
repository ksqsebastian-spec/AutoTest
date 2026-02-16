"""Pydantic models for Rechnungen (Invoices)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.position import PositionCreate, PositionResponse
from app.utils.enums import DocumentStatus, DocumentType


class RechnungCreate(BaseModel):
    """Request body for creating a standard invoice."""
    kunde_id: UUID
    projekt_id: UUID | None = None
    datum: date | None = None
    lieferdatum: date | None = None
    leistungszeitraum_von: date | None = None
    leistungszeitraum_bis: date | None = None
    zahlungsziel_tage: int = Field(default=30, ge=0)
    skonto_prozent: Decimal = Field(default=Decimal("0"), ge=0)
    skonto_tage: int = Field(default=0, ge=0)
    bauabzugsteuer_relevant: bool = False
    einleitungstext: str | None = None
    schlusstext: str | None = None
    positionen: list[PositionCreate]
    template_id: UUID | None = None


class AbschlagsrechnungCreate(RechnungCreate):
    """Additional fields for progress invoices."""
    leistungsstand_prozent: Decimal = Field(ge=0, le=100)


class SchlussrechnungCreate(RechnungCreate):
    """Fields for final invoices."""
    pass


class ZahlungCreate(BaseModel):
    """Request body for recording a payment."""
    betrag: Decimal = Field(gt=0)
    datum: date
    zahlungsart: str | None = None
    referenz: str | None = None
    ist_skonto: bool = False
    bauabzugsteuer_einbehalten: Decimal = Field(default=Decimal("0"), ge=0)
    notizen: str | None = None


class ZahlungResponse(BaseModel):
    """Response model for a payment record."""
    id: UUID
    dokument_id: UUID
    betrag: Decimal
    datum: date
    zahlungsart: str | None = None
    referenz: str | None = None
    ist_skonto: bool
    bauabzugsteuer_einbehalten: Decimal
    created_at: datetime | None = None


class AbschlagDetails(BaseModel):
    """Progress invoice specific details."""
    abschlagsnummer: int
    leistungsstand_prozent: Decimal
    kumuliert_netto: Decimal
    vorherige_abschlaege_netto: Decimal
    aktueller_abschlag_netto: Decimal


class SchlussDetails(BaseModel):
    """Final invoice specific details."""
    gesamtleistung_netto: Decimal
    summe_abschlaege_netto: Decimal
    restbetrag_netto: Decimal


class RechnungResponse(BaseModel):
    """Response model for an invoice (all types)."""
    id: UUID
    dokumentennummer: str
    typ: DocumentType
    status: DocumentStatus
    kunde_id: UUID
    projekt_id: UUID | None = None
    datum: date
    zahlungsziel: date | None = None
    leistungszeitraum_von: date | None = None
    leistungszeitraum_bis: date | None = None
    netto_summe: Decimal
    mwst_betrag: Decimal
    brutto_summe: Decimal
    skonto_prozent: Decimal
    skonto_tage: int
    skonto_betrag: Decimal
    bauabzugsteuer_relevant: bool
    bauabzugsteuer_betrag: Decimal
    zahlbetrag: Decimal
    einleitungstext: str | None = None
    schlusstext: str | None = None
    positionen: list[PositionResponse] = []
    zahlungen: list[ZahlungResponse] = []
    abschlag_details: AbschlagDetails | None = None
    schluss_details: SchlussDetails | None = None
    pdf_url: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
