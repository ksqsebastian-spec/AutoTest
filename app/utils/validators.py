"""German-specific input validators."""

import re


def validate_ust_id(ust_id: str) -> bool:
    """Validate a German USt-IdNr format (DE followed by 9 digits)."""
    return bool(re.match(r"^DE\d{9}$", ust_id.replace(" ", "")))


def validate_iban_de(iban: str) -> bool:
    """Basic format validation for German IBAN (DE + 20 chars)."""
    cleaned = iban.replace(" ", "").upper()
    return bool(re.match(r"^DE\d{20}$", cleaned))


def validate_plz(plz: str) -> bool:
    """Validate a German postal code (5 digits)."""
    return bool(re.match(r"^\d{5}$", plz.strip()))
