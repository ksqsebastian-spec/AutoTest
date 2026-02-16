"""API endpoints for Dashboard."""

from fastapi import APIRouter, Depends
from supabase import Client

from app.dependencies import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/uebersicht")
async def dashboard_uebersicht(db: Client = Depends(get_db)):
    """Main dashboard data: open invoices, overdue, revenue, projects."""
    # Count active customers
    kunden_result = (
        db.table("kunden").select("id", count="exact").eq("aktiv", True).execute()
    )

    # Count active projects
    projekte_result = (
        db.table("projekte")
        .select("id", count="exact")
        .in_("status", ["geplant", "aktiv"])
        .execute()
    )

    # Count open invoices (sent, partially paid, overdue)
    offene_result = (
        db.table("dokumente")
        .select("id,brutto_summe,zahlbetrag", count="exact")
        .in_("typ", ["rechnung", "abschlagsrechnung", "schlussrechnung"])
        .in_("status", ["gesendet", "teilbezahlt", "ueberfaellig"])
        .execute()
    )

    offene_summe = sum(
        float(d.get("zahlbetrag", 0) or 0) for d in (offene_result.data or [])
    )

    return {
        "kunden_aktiv": kunden_result.count or 0,
        "projekte_aktiv": projekte_result.count or 0,
        "offene_rechnungen_anzahl": offene_result.count or 0,
        "offene_rechnungen_summe": round(offene_summe, 2),
    }
