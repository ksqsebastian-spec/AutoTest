"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_kunde_data():
    """Sample customer data for tests."""
    return {
        "nachname": "Mustermann",
        "vorname": "Max",
        "firmenname": "Musterbau GmbH",
        "anrede": "Herr",
        "strasse": "Musterstrasse 1",
        "plz": "10115",
        "ort": "Berlin",
        "land": "Deutschland",
        "email": "max@musterbau.de",
        "telefon": "+49 30 12345678",
        "zahlungsziel_tage": 30,
        "skonto_prozent": 2.0,
        "skonto_tage": 10,
    }


@pytest.fixture
def sample_positionen():
    """Sample line items for tests."""
    return [
        {
            "position_nr": 1,
            "beschreibung": "Erdarbeiten - Baugrubenaushub",
            "einheit": "m3",
            "menge": 150.0,
            "einzelpreis": 25.50,
            "steuersatz": "standard",
        },
        {
            "position_nr": 2,
            "beschreibung": "Beton C25/30",
            "einheit": "m3",
            "menge": 45.0,
            "einzelpreis": 120.00,
            "steuersatz": "standard",
        },
        {
            "position_nr": 3,
            "beschreibung": "Bewehrungsstahl BSt 500 S",
            "einheit": "t",
            "menge": 2.5,
            "einzelpreis": 850.00,
            "steuersatz": "standard",
        },
    ]
