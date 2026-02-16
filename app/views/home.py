"""Dashboard view routes."""

from fastapi import APIRouter, Depends, Request
from supabase import Client

from app.dependencies import get_db
from app.templates_config import templates

router = APIRouter(tags=["Views"])


@router.get("/")
async def dashboard(request: Request, db: Client = Depends(get_db)):
    """Render the main dashboard page."""
    # Gather stats
    kunden_result = (
        db.table("kunden").select("id", count="exact").eq("aktiv", True).execute()
    )
    projekte_result = (
        db.table("projekte")
        .select("id", count="exact")
        .in_("status", ["geplant", "aktiv"])
        .execute()
    )
    offene_result = (
        db.table("dokumente")
        .select("id,zahlbetrag", count="exact")
        .in_("typ", ["rechnung", "abschlagsrechnung", "schlussrechnung"])
        .in_("status", ["gesendet", "teilbezahlt", "ueberfaellig"])
        .execute()
    )
    offene_summe = sum(
        float(d.get("zahlbetrag", 0) or 0) for d in (offene_result.data or [])
    )

    stats = {
        "kunden_aktiv": kunden_result.count or 0,
        "projekte_aktiv": projekte_result.count or 0,
        "offene_rechnungen_anzahl": offene_result.count or 0,
        "offene_rechnungen_summe": round(offene_summe, 2),
    }

    return templates.TemplateResponse(
        "pages/dashboard/index.html",
        {
            "request": request,
            "active_page": "dashboard",
            "stats": stats,
            "messages": [],
        },
    )
