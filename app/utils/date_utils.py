"""Date utility functions for payment terms and deadlines."""

from datetime import date, timedelta


def berechne_zahlungsziel(rechnungsdatum: date, tage: int = 30) -> date:
    """Calculate payment due date from invoice date + days."""
    return rechnungsdatum + timedelta(days=tage)


def berechne_skonto_frist(rechnungsdatum: date, skonto_tage: int) -> date:
    """Calculate cash discount deadline."""
    return rechnungsdatum + timedelta(days=skonto_tage)


def tage_ueberfaellig(zahlungsziel: date, stichtag: date | None = None) -> int:
    """Calculate how many days past due an invoice is. Returns 0 if not overdue."""
    if stichtag is None:
        stichtag = date.today()
    delta = (stichtag - zahlungsziel).days
    return max(0, delta)


def ist_ueberfaellig(zahlungsziel: date, stichtag: date | None = None) -> bool:
    """Check if a payment is overdue."""
    return tage_ueberfaellig(zahlungsziel, stichtag) > 0
