"""Tax calculation service for MwSt, Skonto, and Bauabzugsteuer."""

from decimal import Decimal, ROUND_HALF_UP

from app.utils.enums import TAX_RATES, TaxRateType


def _q(value: Decimal) -> Decimal:
    """Quantize to 2 decimal places."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def berechne_position(
    menge: Decimal,
    einzelpreis: Decimal,
    steuersatz: TaxRateType = TaxRateType.STANDARD,
) -> dict:
    """
    Calculate a single line item's financial values.

    Returns dict with: gesamt_netto, steuersatz_prozent, mwst_betrag, gesamt_brutto
    """
    netto = _q(Decimal(str(menge)) * Decimal(str(einzelpreis)))
    satz = Decimal(str(TAX_RATES[steuersatz]))
    mwst = _q(netto * satz / Decimal("100"))
    brutto = netto + mwst

    return {
        "gesamt_netto": netto,
        "steuersatz_prozent": satz,
        "mwst_betrag": mwst,
        "gesamt_brutto": brutto,
    }


def berechne_dokument(
    positionen: list[dict],
    skonto_prozent: Decimal = Decimal("0"),
    skonto_tage: int = 0,
    bauabzugsteuer_relevant: bool = False,
    freistellung_gueltig: bool = False,
) -> dict:
    """
    Full tax calculation for a document.

    Args:
        positionen: List of dicts with gesamt_netto, steuersatz, steuersatz_prozent, mwst_betrag
        skonto_prozent: Cash discount percentage
        skonto_tage: Days for cash discount eligibility
        bauabzugsteuer_relevant: Whether 15% construction withholding tax applies
        freistellung_gueltig: Whether a valid exemption certificate exists

    Returns dict with all calculated financial values.
    """
    # Group by tax rate
    mwst_gruppen: dict[str, dict] = {}
    netto_summe = Decimal("0")
    mwst_gesamt = Decimal("0")

    for pos in positionen:
        satz_key = str(pos.get("steuersatz_prozent", "19.0"))
        netto = Decimal(str(pos["gesamt_netto"]))
        mwst = Decimal(str(pos["mwst_betrag"]))

        netto_summe += netto
        mwst_gesamt += mwst

        if satz_key not in mwst_gruppen:
            mwst_gruppen[satz_key] = {
                "steuersatz_prozent": Decimal(satz_key),
                "netto_summe": Decimal("0"),
                "mwst_betrag": Decimal("0"),
            }
        mwst_gruppen[satz_key]["netto_summe"] += netto
        mwst_gruppen[satz_key]["mwst_betrag"] += mwst

    # Quantize group totals
    for g in mwst_gruppen.values():
        g["netto_summe"] = _q(g["netto_summe"])
        g["mwst_betrag"] = _q(g["mwst_betrag"])
        g["brutto_summe"] = g["netto_summe"] + g["mwst_betrag"]

    netto_summe = _q(netto_summe)
    mwst_gesamt = _q(mwst_gesamt)
    brutto_summe = netto_summe + mwst_gesamt

    # Skonto
    skonto_betrag = Decimal("0")
    if skonto_prozent > 0:
        skonto_betrag = _q(brutto_summe * Decimal(str(skonto_prozent)) / Decimal("100"))

    # Bauabzugsteuer (15% withholding)
    bauabzugsteuer_betrag = Decimal("0")
    if bauabzugsteuer_relevant and not freistellung_gueltig:
        bauabzugsteuer_betrag = _q(brutto_summe * Decimal("15") / Decimal("100"))

    # Final payment amount
    zahlbetrag = brutto_summe - bauabzugsteuer_betrag

    return {
        "netto_summe": netto_summe,
        "mwst_betrag": mwst_gesamt,
        "brutto_summe": brutto_summe,
        "mwst_aufschluesselung": list(mwst_gruppen.values()),
        "skonto_prozent": Decimal(str(skonto_prozent)),
        "skonto_tage": skonto_tage,
        "skonto_betrag": skonto_betrag,
        "bauabzugsteuer_relevant": bauabzugsteuer_relevant,
        "bauabzugsteuer_betrag": bauabzugsteuer_betrag,
        "zahlbetrag": zahlbetrag,
    }
