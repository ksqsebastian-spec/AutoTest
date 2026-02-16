"""Server-side rendered HTML views for Kunden (Customers)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from supabase import Client

from app.dependencies import get_db
from app.models.kunde import KundeCreate, KundeUpdate
from app.services import kunde_service, projekt_service
from app.templates_config import templates

router = APIRouter(tags=["Kunden Views"])


@router.get("/kunden")
async def kunden_list(
    request: Request,
    page: int = 1,
    search: str | None = None,
    db: Client = Depends(get_db),
):
    """Render customer list page."""
    result = await kunde_service.list_kunden(db, page=page, search=search)

    return templates.TemplateResponse(
        "pages/kunden/list.html",
        {
            "request": request,
            "active_page": "kunden",
            "kunden": result["items"],
            "page": result["page"],
            "total_pages": result["total_pages"],
            "total": result["total"],
            "search": search or "",
            "messages": [],
        },
    )


@router.get("/kunden/neu")
async def kunden_form_new(request: Request):
    """Render new customer form."""
    return templates.TemplateResponse(
        "pages/kunden/form.html",
        {
            "request": request,
            "active_page": "kunden",
            "kunde": None,
            "messages": [],
        },
    )


@router.post("/kunden")
async def kunden_create(
    request: Request,
    db: Client = Depends(get_db),
    nachname: str = Form(...),
    strasse: str = Form(...),
    plz: str = Form(...),
    ort: str = Form(...),
    firmenname: str = Form(""),
    anrede: str = Form(""),
    vorname: str = Form(""),
    land: str = Form("Deutschland"),
    telefon: str = Form(""),
    mobil: str = Form(""),
    email: str = Form(""),
    ust_id: str = Form(""),
    steuernummer: str = Form(""),
    zahlungsziel_tage: int = Form(30),
    skonto_prozent: float = Form(0),
    skonto_tage: int = Form(0),
    ist_auftraggeber_bau: bool = Form(False),
    freistellungsbescheid_vorhanden: bool = Form(False),
    notizen: str = Form(""),
):
    """Handle new customer form submission."""
    data = KundeCreate(
        nachname=nachname,
        strasse=strasse,
        plz=plz,
        ort=ort,
        firmenname=firmenname or None,
        anrede=anrede or None,
        vorname=vorname or None,
        land=land,
        telefon=telefon or None,
        mobil=mobil or None,
        email=email or None,
        ust_id=ust_id or None,
        steuernummer=steuernummer or None,
        zahlungsziel_tage=zahlungsziel_tage,
        skonto_prozent=skonto_prozent,
        skonto_tage=skonto_tage,
        ist_auftraggeber_bau=ist_auftraggeber_bau,
        freistellungsbescheid_vorhanden=freistellungsbescheid_vorhanden,
        notizen=notizen or None,
    )
    kunde = await kunde_service.create_kunde(db, data)
    return RedirectResponse(url=f"/kunden/{kunde['id']}", status_code=303)


@router.get("/kunden/{kunde_id}")
async def kunden_detail(
    request: Request, kunde_id: UUID, db: Client = Depends(get_db)
):
    """Render customer detail page."""
    kunde = await kunde_service.get_kunde(db, kunde_id)
    if not kunde:
        return RedirectResponse(url="/kunden", status_code=303)

    # Load projects for this customer
    projekte_result = await projekt_service.list_projekte(
        db, kunde_id=kunde_id, per_page=100
    )

    return templates.TemplateResponse(
        "pages/kunden/detail.html",
        {
            "request": request,
            "active_page": "kunden",
            "kunde": kunde,
            "projekte": projekte_result["items"],
            "messages": [],
        },
    )


@router.get("/kunden/{kunde_id}/bearbeiten")
async def kunden_form_edit(
    request: Request, kunde_id: UUID, db: Client = Depends(get_db)
):
    """Render edit customer form."""
    kunde = await kunde_service.get_kunde(db, kunde_id)
    if not kunde:
        return RedirectResponse(url="/kunden", status_code=303)

    return templates.TemplateResponse(
        "pages/kunden/form.html",
        {
            "request": request,
            "active_page": "kunden",
            "kunde": kunde,
            "messages": [],
        },
    )


@router.post("/kunden/{kunde_id}")
async def kunden_update(
    request: Request,
    kunde_id: UUID,
    db: Client = Depends(get_db),
    nachname: str = Form(...),
    strasse: str = Form(...),
    plz: str = Form(...),
    ort: str = Form(...),
    firmenname: str = Form(""),
    anrede: str = Form(""),
    vorname: str = Form(""),
    land: str = Form("Deutschland"),
    telefon: str = Form(""),
    mobil: str = Form(""),
    email: str = Form(""),
    ust_id: str = Form(""),
    steuernummer: str = Form(""),
    zahlungsziel_tage: int = Form(30),
    skonto_prozent: float = Form(0),
    skonto_tage: int = Form(0),
    ist_auftraggeber_bau: bool = Form(False),
    freistellungsbescheid_vorhanden: bool = Form(False),
    notizen: str = Form(""),
):
    """Handle edit customer form submission."""
    data = KundeUpdate(
        nachname=nachname,
        strasse=strasse,
        plz=plz,
        ort=ort,
        firmenname=firmenname or None,
        anrede=anrede or None,
        vorname=vorname or None,
        land=land,
        telefon=telefon or None,
        mobil=mobil or None,
        email=email or None,
        ust_id=ust_id or None,
        steuernummer=steuernummer or None,
        zahlungsziel_tage=zahlungsziel_tage,
        skonto_prozent=skonto_prozent,
        skonto_tage=skonto_tage,
        ist_auftraggeber_bau=ist_auftraggeber_bau,
        freistellungsbescheid_vorhanden=freistellungsbescheid_vorhanden,
        notizen=notizen or None,
    )
    await kunde_service.update_kunde(db, kunde_id, data)
    return RedirectResponse(url=f"/kunden/{kunde_id}", status_code=303)
