"""Pydantic models for Projekte (Construction Projects)."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.utils.enums import ProjektStatus


class ProjektBase(BaseModel):
    """Shared fields for project create/update."""
    kunde_id: UUID
    bezeichnung: str
    strasse: str | None = None
    plz: str | None = None
    ort: str | None = None
    beschreibung: str | None = None
    status: ProjektStatus = ProjektStatus.GEPLANT
    beginn_datum: date | None = None
    ende_datum: date | None = None
    auftragssumme: Decimal | None = Field(default=None, ge=0)
    bauabzugsteuer_relevant: bool = False
    bauabzugsteuer_prozent: Decimal = Field(default=Decimal("15.0"), ge=0)


class ProjektCreate(ProjektBase):
    """Request body for creating a project."""
    pass


class ProjektUpdate(BaseModel):
    """Request body for updating a project. All fields optional."""
    kunde_id: UUID | None = None
    bezeichnung: str | None = None
    strasse: str | None = None
    plz: str | None = None
    ort: str | None = None
    beschreibung: str | None = None
    status: ProjektStatus | None = None
    beginn_datum: date | None = None
    ende_datum: date | None = None
    auftragssumme: Decimal | None = None
    bauabzugsteuer_relevant: bool | None = None
    bauabzugsteuer_prozent: Decimal | None = None


class ProjektResponse(ProjektBase):
    """Response model for a project."""
    id: UUID
    projektnummer: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ProjektListItem(BaseModel):
    """Compact project for list views."""
    id: UUID
    projektnummer: str
    bezeichnung: str
    status: ProjektStatus
    ort: str | None = None
    kunde_name: str | None = None
