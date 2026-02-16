-- ============================================================
-- BauDok - Seed Data
-- ============================================================

-- Default company settings (to be updated by user)
INSERT INTO unternehmen (firmenname, strasse, plz, ort, telefon, email)
VALUES (
    'Musterbau GmbH',
    'Baustrasse 1',
    '10115',
    'Berlin',
    '+49 30 12345678',
    'info@musterbau.de'
);

-- Initialize number counters for current year
INSERT INTO nummernkreise (typ, praefix, jahr, letzter_wert) VALUES
    ('angebot', 'AN', 2026, 0),
    ('rechnung', 'RE', 2026, 0),
    ('abschlagsrechnung', 'AB', 2026, 0),
    ('schlussrechnung', 'SR', 2026, 0),
    ('mahnung', 'MA', 2026, 0),
    ('leistungsverzeichnis', 'LV', 2026, 0),
    ('nachtrag', 'NT', 2026, 0),
    ('aufmass', 'AM', 2026, 0);
