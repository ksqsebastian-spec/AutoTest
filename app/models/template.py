"""Pydantic models for PDF Templates."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.utils.enums import DocumentType


class TemplateCreate(BaseModel):
    """Request body for uploading a PDF template."""
    name: str
    beschreibung: str | None = None
    dokument_typ: DocumentType | None = None
    html_template: str
    css_styles: str | None = None
    header_html: str | None = None
    footer_html: str | None = None


class TemplateUpdate(BaseModel):
    """Request body for updating a PDF template."""
    name: str | None = None
    beschreibung: str | None = None
    dokument_typ: DocumentType | None = None
    html_template: str | None = None
    css_styles: str | None = None
    header_html: str | None = None
    footer_html: str | None = None


class TemplateResponse(BaseModel):
    """Response model for a PDF template."""
    id: UUID
    name: str
    beschreibung: str | None = None
    dokument_typ: DocumentType | None = None
    html_template: str
    css_styles: str | None = None
    header_html: str | None = None
    footer_html: str | None = None
    logo_url: str | None = None
    ist_standard: bool
    aktiv: bool
    vorschau_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
