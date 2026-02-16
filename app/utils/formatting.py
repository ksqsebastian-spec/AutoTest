"""German locale formatting utilities for currency, numbers, and dates."""

from datetime import date, datetime
from decimal import Decimal

from app.utils.enums import EINHEIT_LABELS, Einheit


def format_eur(value: Decimal | float | int | None) -> str:
    """Format a number as German currency: 1.234,56 EUR"""
    if value is None:
        return "0,00 EUR"
    val = Decimal(str(value))
    formatted = f"{val:,.2f}"
    # Convert from 1,234.56 to 1.234,56
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted} EUR"


def format_decimal(value: Decimal | float | int | None, decimals: int = 2) -> str:
    """Format a number with German decimal notation: 1.234,56"""
    if value is None:
        return "0" + "," + "0" * decimals
    val = Decimal(str(value))
    formatted = f"{val:,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_menge(value: Decimal | float | int | None) -> str:
    """Format a quantity with 3 decimal places: 1.234,500"""
    return format_decimal(value, 3)


def format_date(value: date | datetime | None) -> str:
    """Format as German date: 16.02.2026"""
    if value is None:
        return ""
    if isinstance(value, datetime):
        value = value.date()
    return value.strftime("%d.%m.%Y")


def format_einheit(value: str | Einheit | None) -> str:
    """Convert einheit enum value to display label."""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = Einheit(value)
        except ValueError:
            return value
    return EINHEIT_LABELS.get(value, str(value))
