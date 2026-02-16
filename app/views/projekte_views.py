"""Server-side rendered HTML views for Projekte (Projects)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from supabase import Client

from app.dependencies import get_db
from app.models.projekt import ProjektCreate, ProjektUpdate
from app.services import kunde_service, projekt_service
from app.templates_config import templates

router = APIRouter(tags=["Projekte Views"])


@router.get("/projekte")
async def projekte_list(
    request: Request,
    page: int = 1,
    search: str | None = None,
    status: str | None = None,
    db: Client = Depends(get_db),
):
    """Render project list page."""
    result = await projekt_service.list_projekte(
        db, page=page, search=search, status=status
    )

    return templates.TemplateResponse(
        "pages/projekte/list.html",
        {
            "request": request,
            "active_page": "projekte",
            "projekte": result["items"],
            "page": result["page"],
            "total_pages": result["total_pages"],
            "total": result["total"],
            "search": search or "",
            "status_filter": status or "",
            "messages": [],
        },
    )


@router.get("/projekte/neu")
async def projekte_form_new(request: Request, db: Client = Depends(get_db)):
    """Render new project form."""
    kunden_result = await kunde_service.list_kunden(db, per_page=500, aktiv=True)

    return templates.TemplateResponse(
        "pages/projekte/form.html",
        {
            "request": request,
            "active_page": "projekte",
            "projekt": None,
            "kunden": kunden_result["items"],
            "messages": [],
        },
    )


@router.post("/projekte")
async def projekte_create(
    request: Request,
    db: Client = Depends(get_db),
    kunde_id: str = Form(...),
    bezeichnung: str = Form(...),
    strasse: str = Form(""),
    plz: str = Form(""),
    ort: str = Form(""),
    beschreibung: str = Form(""),
    beginn_datum: str = Form(""),
    ende_datum: str = Form(""),
    auftragssumme: float = Form(0),
    bauabzugsteuer_relevant: bool = Form(False),
):
    """Handle new project form submission."""
    from datetime import date as date_type

    data = ProjektCreate(
        kunde_id=UUID(kunde_id),
        bezeichnung=bezeichnung,
        strasse=strasse or None,
        plz=plz or None,
        ort=ort or None,
        beschreibung=beschreibung or None,
        beginn_datum=date_type.fromisoformat(beginn_datum) if beginn_datum else None,
        ende_datum=date_type.fromisoformat(ende_datum) if ende_datum else None,
        auftragssumme=auftragssumme if auftragssumme else None,
        bauabzugsteuer_relevant=bauabzugsteuer_relevant,
    )
    projekt = await projekt_service.create_projekt(db, data)
    return RedirectResponse(url=f"/projekte/{projekt['id']}", status_code=303)


@router.get("/projekte/{projekt_id}")
async def projekte_detail(
    request: Request, projekt_id: UUID, db: Client = Depends(get_db)
):
    """Render project detail page."""
    projekt = await projekt_service.get_projekt(db, projekt_id)
    if not projekt:
        return RedirectResponse(url="/projekte", status_code=303)

    # Get customer info
    kunde = await kunde_service.get_kunde(db, UUID(projekt["kunde_id"]))

    return templates.TemplateResponse(
        "pages/projekte/detail.html",
        {
            "request": request,
            "active_page": "projekte",
            "projekt": projekt,
            "kunde": kunde,
            "messages": [],
        },
    )
