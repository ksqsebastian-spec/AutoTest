"""Tests for tax calculation service."""

from decimal import Decimal

from app.services.tax_service import berechne_dokument, berechne_position
from app.utils.enums import TaxRateType


class TestBerechnePosition:
    def test_standard_rate(self):
        result = berechne_position(
            menge=Decimal("10"),
            einzelpreis=Decimal("100"),
            steuersatz=TaxRateType.STANDARD,
        )
        assert result["gesamt_netto"] == Decimal("1000.00")
        assert result["steuersatz_prozent"] == Decimal("19.0")
        assert result["mwst_betrag"] == Decimal("190.00")
        assert result["gesamt_brutto"] == Decimal("1190.00")

    def test_reduced_rate(self):
        result = berechne_position(
            menge=Decimal("5"),
            einzelpreis=Decimal("200"),
            steuersatz=TaxRateType.ERMAESSIGT,
        )
        assert result["gesamt_netto"] == Decimal("1000.00")
        assert result["mwst_betrag"] == Decimal("70.00")
        assert result["gesamt_brutto"] == Decimal("1070.00")

    def test_exempt_rate(self):
        result = berechne_position(
            menge=Decimal("1"),
            einzelpreis=Decimal("500"),
            steuersatz=TaxRateType.BEFREIT,
        )
        assert result["gesamt_netto"] == Decimal("500.00")
        assert result["mwst_betrag"] == Decimal("0.00")
        assert result["gesamt_brutto"] == Decimal("500.00")

    def test_decimal_precision(self):
        result = berechne_position(
            menge=Decimal("3.333"),
            einzelpreis=Decimal("99.99"),
            steuersatz=TaxRateType.STANDARD,
        )
        # 3.333 * 99.99 = 333.2667 -> rounded to 333.27
        assert result["gesamt_netto"] == Decimal("333.27")


class TestBerechneDokument:
    def test_simple_document(self):
        positionen = [
            {
                "gesamt_netto": Decimal("1000.00"),
                "steuersatz_prozent": Decimal("19.0"),
                "mwst_betrag": Decimal("190.00"),
            },
        ]
        result = berechne_dokument(positionen)
        assert result["netto_summe"] == Decimal("1000.00")
        assert result["mwst_betrag"] == Decimal("190.00")
        assert result["brutto_summe"] == Decimal("1190.00")
        assert result["zahlbetrag"] == Decimal("1190.00")

    def test_mixed_tax_rates(self):
        positionen = [
            {
                "gesamt_netto": Decimal("1000.00"),
                "steuersatz_prozent": Decimal("19.0"),
                "mwst_betrag": Decimal("190.00"),
            },
            {
                "gesamt_netto": Decimal("500.00"),
                "steuersatz_prozent": Decimal("7.0"),
                "mwst_betrag": Decimal("35.00"),
            },
        ]
        result = berechne_dokument(positionen)
        assert result["netto_summe"] == Decimal("1500.00")
        assert result["mwst_betrag"] == Decimal("225.00")
        assert result["brutto_summe"] == Decimal("1725.00")
        assert len(result["mwst_aufschluesselung"]) == 2

    def test_skonto(self):
        positionen = [
            {
                "gesamt_netto": Decimal("1000.00"),
                "steuersatz_prozent": Decimal("19.0"),
                "mwst_betrag": Decimal("190.00"),
            },
        ]
        result = berechne_dokument(positionen, skonto_prozent=Decimal("2"))
        assert result["skonto_betrag"] == Decimal("23.80")  # 2% of 1190

    def test_bauabzugsteuer(self):
        positionen = [
            {
                "gesamt_netto": Decimal("10000.00"),
                "steuersatz_prozent": Decimal("19.0"),
                "mwst_betrag": Decimal("1900.00"),
            },
        ]
        result = berechne_dokument(
            positionen,
            bauabzugsteuer_relevant=True,
            freistellung_gueltig=False,
        )
        # 15% of 11900 = 1785
        assert result["bauabzugsteuer_betrag"] == Decimal("1785.00")
        assert result["zahlbetrag"] == Decimal("10115.00")

    def test_bauabzugsteuer_with_freistellung(self):
        positionen = [
            {
                "gesamt_netto": Decimal("10000.00"),
                "steuersatz_prozent": Decimal("19.0"),
                "mwst_betrag": Decimal("1900.00"),
            },
        ]
        result = berechne_dokument(
            positionen,
            bauabzugsteuer_relevant=True,
            freistellung_gueltig=True,
        )
        # Freistellung: no withholding
        assert result["bauabzugsteuer_betrag"] == Decimal("0")
        assert result["zahlbetrag"] == Decimal("11900.00")
