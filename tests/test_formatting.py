"""Tests for German formatting utilities."""

from datetime import date
from decimal import Decimal

from app.utils.formatting import format_date, format_einheit, format_eur, format_menge


class TestFormatEUR:
    def test_simple_amount(self):
        assert format_eur(Decimal("1234.56")) == "1.234,56 EUR"

    def test_zero(self):
        assert format_eur(0) == "0,00 EUR"

    def test_none(self):
        assert format_eur(None) == "0,00 EUR"

    def test_large_amount(self):
        assert format_eur(Decimal("1234567.89")) == "1.234.567,89 EUR"

    def test_small_amount(self):
        assert format_eur(Decimal("0.99")) == "0,99 EUR"


class TestFormatDate:
    def test_standard_date(self):
        assert format_date(date(2026, 2, 16)) == "16.02.2026"

    def test_none(self):
        assert format_date(None) == ""


class TestFormatMenge:
    def test_integer_quantity(self):
        assert format_menge(Decimal("10")) == "10,000"

    def test_decimal_quantity(self):
        assert format_menge(Decimal("3.5")) == "3,500"


class TestFormatEinheit:
    def test_m2(self):
        assert format_einheit("m2") == "m\u00b2"

    def test_stueck(self):
        assert format_einheit("stueck") == "Stk."

    def test_none(self):
        assert format_einheit(None) == ""
