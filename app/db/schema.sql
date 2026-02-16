-- ============================================================
-- BauDok - Datenbank-Schema fuer Supabase (PostgreSQL)
-- ============================================================

-- ============================================================
-- ENUM TYPES
-- ============================================================
CREATE TYPE document_type AS ENUM (
    'angebot',
    'rechnung',
    'abschlagsrechnung',
    'schlussrechnung',
    'mahnung',
    'leistungsverzeichnis',
    'nachtrag',
    'aufmass'
);

CREATE TYPE document_status AS ENUM (
    'entwurf',
    'gesendet',
    'akzeptiert',
    'abgelehnt',
    'bezahlt',
    'teilbezahlt',
    'ueberfaellig',
    'storniert'
);

CREATE TYPE mahnstufe AS ENUM (
    'erste',
    'zweite',
    'dritte'
);

CREATE TYPE tax_rate_type AS ENUM (
    'standard',
    'ermaessigt',
    'befreit'
);

CREATE TYPE projekt_status AS ENUM (
    'geplant',
    'aktiv',
    'pausiert',
    'abgeschlossen',
    'abgerechnet'
);

CREATE TYPE einheit AS ENUM (
    'stueck',
    'stunde',
    'm',
    'm2',
    'm3',
    'kg',
    't',
    'pauschal',
    'lfm',
    'liter',
    'tag'
);

-- ============================================================
-- UPDATED_AT TRIGGER FUNCTION
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- UNTERNEHMEN (Company Settings / Letterhead)
-- ============================================================
CREATE TABLE unternehmen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    firmenname TEXT NOT NULL,
    inhaberin TEXT,
    strasse TEXT NOT NULL,
    plz TEXT NOT NULL,
    ort TEXT NOT NULL,
    telefon TEXT,
    email TEXT,
    website TEXT,
    steuernummer TEXT,
    ust_id TEXT,
    handelsregister TEXT,
    bankname TEXT,
    iban TEXT,
    bic TEXT,
    logo_url TEXT,
    freistellungsbescheinigung_nr TEXT,
    freistellung_gueltig_bis DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_updated_at_unternehmen
    BEFORE UPDATE ON unternehmen
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- KUNDEN (Customers)
-- ============================================================
CREATE TABLE kunden (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    kundennummer TEXT NOT NULL UNIQUE,
    firmenname TEXT,
    anrede TEXT,
    vorname TEXT,
    nachname TEXT NOT NULL,
    strasse TEXT NOT NULL,
    plz TEXT NOT NULL,
    ort TEXT NOT NULL,
    land TEXT DEFAULT 'Deutschland',
    telefon TEXT,
    mobil TEXT,
    email TEXT,
    ust_id TEXT,
    steuernummer TEXT,
    ist_auftraggeber_bau BOOLEAN DEFAULT FALSE,
    freistellungsbescheid_vorhanden BOOLEAN DEFAULT FALSE,
    zahlungsziel_tage INTEGER DEFAULT 30,
    skonto_prozent DECIMAL(5,2) DEFAULT 0,
    skonto_tage INTEGER DEFAULT 0,
    notizen TEXT,
    aktiv BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_updated_at_kunden
    BEFORE UPDATE ON kunden
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- PROJEKTE (Construction Projects)
-- ============================================================
CREATE TABLE projekte (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    projektnummer TEXT NOT NULL UNIQUE,
    kunde_id UUID NOT NULL REFERENCES kunden(id) ON DELETE RESTRICT,
    bezeichnung TEXT NOT NULL,
    strasse TEXT,
    plz TEXT,
    ort TEXT,
    beschreibung TEXT,
    status projekt_status DEFAULT 'geplant',
    beginn_datum DATE,
    ende_datum DATE,
    auftragssumme DECIMAL(12,2),
    bauabzugsteuer_relevant BOOLEAN DEFAULT FALSE,
    bauabzugsteuer_prozent DECIMAL(5,2) DEFAULT 15.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_updated_at_projekte
    BEFORE UPDATE ON projekte
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- NUMMERNKREISE (GoBD-compliant Document Number Counters)
-- ============================================================
CREATE TABLE nummernkreise (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    typ document_type NOT NULL,
    praefix TEXT NOT NULL,
    jahr INTEGER NOT NULL,
    letzter_wert INTEGER DEFAULT 0,
    UNIQUE(typ, jahr)
);

-- Atomic document number generation function
CREATE OR REPLACE FUNCTION naechste_dokumentennummer(p_typ document_type, p_jahr INTEGER)
RETURNS TEXT AS $$
DECLARE
    v_praefix TEXT;
    v_nummer INTEGER;
BEGIN
    INSERT INTO nummernkreise (typ, praefix, jahr, letzter_wert)
    VALUES (
        p_typ,
        CASE p_typ
            WHEN 'angebot' THEN 'AN'
            WHEN 'rechnung' THEN 'RE'
            WHEN 'abschlagsrechnung' THEN 'AB'
            WHEN 'schlussrechnung' THEN 'SR'
            WHEN 'mahnung' THEN 'MA'
            WHEN 'leistungsverzeichnis' THEN 'LV'
            WHEN 'nachtrag' THEN 'NT'
            WHEN 'aufmass' THEN 'AM'
        END,
        p_jahr,
        1
    )
    ON CONFLICT (typ, jahr) DO UPDATE
        SET letzter_wert = nummernkreise.letzter_wert + 1
    RETURNING praefix, letzter_wert INTO v_praefix, v_nummer;

    RETURN v_praefix || '-' || p_jahr::TEXT || '-' || LPAD(v_nummer::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- DOKUMENTE (Base Table for ALL Document Types)
-- ============================================================
CREATE TABLE dokumente (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokumentennummer TEXT NOT NULL UNIQUE,
    typ document_type NOT NULL,
    status document_status DEFAULT 'entwurf',
    kunde_id UUID NOT NULL REFERENCES kunden(id) ON DELETE RESTRICT,
    projekt_id UUID REFERENCES projekte(id) ON DELETE SET NULL,

    -- Dates
    datum DATE NOT NULL DEFAULT CURRENT_DATE,
    lieferdatum DATE,
    leistungszeitraum_von DATE,
    leistungszeitraum_bis DATE,
    zahlungsziel DATE,

    -- Financial
    netto_summe DECIMAL(12,2) DEFAULT 0,
    mwst_betrag DECIMAL(12,2) DEFAULT 0,
    brutto_summe DECIMAL(12,2) DEFAULT 0,

    -- Skonto
    skonto_prozent DECIMAL(5,2) DEFAULT 0,
    skonto_tage INTEGER DEFAULT 0,
    skonto_betrag DECIMAL(12,2) DEFAULT 0,

    -- Bauabzugsteuer
    bauabzugsteuer_relevant BOOLEAN DEFAULT FALSE,
    bauabzugsteuer_betrag DECIMAL(12,2) DEFAULT 0,
    zahlbetrag DECIMAL(12,2) DEFAULT 0,

    -- Text
    einleitungstext TEXT,
    schlusstext TEXT,
    interne_notizen TEXT,

    -- Reference to related document
    referenz_dokument_id UUID REFERENCES dokumente(id),

    -- PDF template
    template_id UUID,

    -- PDF
    pdf_url TEXT,
    pdf_generiert_am TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_updated_at_dokumente
    BEFORE UPDATE ON dokumente
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- POSITIONEN (Line Items)
-- ============================================================
CREATE TABLE positionen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    position_nr INTEGER NOT NULL,
    titel TEXT,
    beschreibung TEXT NOT NULL,
    einheit einheit DEFAULT 'stueck',
    menge DECIMAL(12,3) NOT NULL,
    einzelpreis DECIMAL(12,2) NOT NULL,
    gesamt_netto DECIMAL(12,2) NOT NULL,
    steuersatz tax_rate_type DEFAULT 'standard',
    steuersatz_prozent DECIMAL(5,2) DEFAULT 19.0,
    mwst_betrag DECIMAL(12,2) DEFAULT 0,
    gesamt_brutto DECIMAL(12,2) DEFAULT 0,
    aufmass_referenz TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(dokument_id, position_nr)
);

CREATE TRIGGER set_updated_at_positionen
    BEFORE UPDATE ON positionen
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- ABSCHLAGSRECHNUNGEN (Progress Invoice Details)
-- ============================================================
CREATE TABLE abschlagsrechnungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id),
    abschlagsnummer INTEGER NOT NULL,
    leistungsstand_prozent DECIMAL(5,2),
    kumuliert_netto DECIMAL(12,2),
    vorherige_abschlaege_netto DECIMAL(12,2) DEFAULT 0,
    aktueller_abschlag_netto DECIMAL(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(projekt_id, abschlagsnummer)
);

-- ============================================================
-- SCHLUSSRECHNUNGEN (Final Invoice Details)
-- ============================================================
CREATE TABLE schlussrechnungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id),
    gesamtleistung_netto DECIMAL(12,2),
    summe_abschlaege_netto DECIMAL(12,2),
    restbetrag_netto DECIMAL(12,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- MAHNUNGEN (Dunning Details)
-- ============================================================
CREATE TABLE mahnungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    rechnung_dokument_id UUID NOT NULL REFERENCES dokumente(id),
    stufe mahnstufe NOT NULL,
    faelligkeitsdatum DATE NOT NULL,
    offener_betrag DECIMAL(12,2),
    mahngebuehr DECIMAL(12,2) DEFAULT 0,
    verzugszinsen DECIMAL(12,2) DEFAULT 0,
    mahnfrist DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- LEISTUNGSVERZEICHNISSE (Bills of Quantities)
-- ============================================================
CREATE TABLE leistungsverzeichnisse (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id),
    gewerk TEXT,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- LV POSITIONEN (Bill of Quantities Line Items)
-- ============================================================
CREATE TABLE lv_positionen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lv_id UUID NOT NULL REFERENCES leistungsverzeichnisse(id) ON DELETE CASCADE,
    ordnungszahl TEXT NOT NULL,
    titel TEXT,
    beschreibung TEXT NOT NULL,
    einheit einheit DEFAULT 'stueck',
    menge DECIMAL(12,3),
    einzelpreis DECIMAL(12,2),
    gesamtpreis DECIMAL(12,2),
    ist_titel BOOLEAN DEFAULT FALSE,
    parent_id UUID REFERENCES lv_positionen(id),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- NACHTRAEGE (Change Orders)
-- ============================================================
CREATE TABLE nachtraege (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id),
    nachtragsnummer INTEGER NOT NULL,
    begruendung TEXT,
    referenz_lv_id UUID REFERENCES leistungsverzeichnisse(id),
    genehmigt BOOLEAN DEFAULT FALSE,
    genehmigt_am DATE,
    genehmigt_von TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(projekt_id, nachtragsnummer)
);

-- ============================================================
-- AUFMASSE (Measurement Records)
-- ============================================================
CREATE TABLE aufmasse (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id),
    aufmass_nummer INTEGER NOT NULL,
    aufnahmedatum DATE NOT NULL,
    aufgenommen_von TEXT,
    geprueft_von TEXT,
    geprueft_am DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(projekt_id, aufmass_nummer)
);

CREATE TABLE aufmass_positionen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aufmass_id UUID NOT NULL REFERENCES aufmasse(id) ON DELETE CASCADE,
    lv_position_id UUID REFERENCES lv_positionen(id),
    beschreibung TEXT NOT NULL,
    formel TEXT,
    laenge DECIMAL(10,3),
    breite DECIMAL(10,3),
    hoehe DECIMAL(10,3),
    anzahl DECIMAL(10,3) DEFAULT 1,
    ergebnis DECIMAL(12,3) NOT NULL,
    einheit einheit,
    notizen TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ZAHLUNGEN (Payment Records)
-- ============================================================
CREATE TABLE zahlungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dokument_id UUID NOT NULL REFERENCES dokumente(id) ON DELETE CASCADE,
    betrag DECIMAL(12,2) NOT NULL,
    datum DATE NOT NULL,
    zahlungsart TEXT,
    referenz TEXT,
    ist_skonto BOOLEAN DEFAULT FALSE,
    bauabzugsteuer_einbehalten DECIMAL(12,2) DEFAULT 0,
    notizen TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- PDF TEMPLATES (Uploadable PDF Designs)
-- ============================================================
CREATE TABLE pdf_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    beschreibung TEXT,
    dokument_typ document_type,
    html_template TEXT NOT NULL,
    css_styles TEXT,
    header_html TEXT,
    footer_html TEXT,
    logo_url TEXT,
    ist_standard BOOLEAN DEFAULT FALSE,
    aktiv BOOLEAN DEFAULT TRUE,
    vorschau_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER set_updated_at_pdf_templates
    BEFORE UPDATE ON pdf_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Add foreign key from dokumente to pdf_templates
ALTER TABLE dokumente
    ADD CONSTRAINT fk_dokumente_template
    FOREIGN KEY (template_id) REFERENCES pdf_templates(id) ON DELETE SET NULL;

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_dokumente_kunde ON dokumente(kunde_id);
CREATE INDEX idx_dokumente_projekt ON dokumente(projekt_id);
CREATE INDEX idx_dokumente_typ ON dokumente(typ);
CREATE INDEX idx_dokumente_status ON dokumente(status);
CREATE INDEX idx_dokumente_datum ON dokumente(datum);
CREATE INDEX idx_dokumente_zahlungsziel ON dokumente(zahlungsziel);
CREATE INDEX idx_positionen_dokument ON positionen(dokument_id);
CREATE INDEX idx_projekte_kunde ON projekte(kunde_id);
CREATE INDEX idx_zahlungen_dokument ON zahlungen(dokument_id);
CREATE INDEX idx_mahnungen_rechnung ON mahnungen(rechnung_dokument_id);
CREATE INDEX idx_kunden_kundennummer ON kunden(kundennummer);
CREATE INDEX idx_kunden_aktiv ON kunden(aktiv);
CREATE INDEX idx_lv_positionen_lv ON lv_positionen(lv_id);

-- ============================================================
-- ROW LEVEL SECURITY (enable for Supabase)
-- ============================================================
ALTER TABLE unternehmen ENABLE ROW LEVEL SECURITY;
ALTER TABLE kunden ENABLE ROW LEVEL SECURITY;
ALTER TABLE projekte ENABLE ROW LEVEL SECURITY;
ALTER TABLE dokumente ENABLE ROW LEVEL SECURITY;
ALTER TABLE positionen ENABLE ROW LEVEL SECURITY;
ALTER TABLE abschlagsrechnungen ENABLE ROW LEVEL SECURITY;
ALTER TABLE schlussrechnungen ENABLE ROW LEVEL SECURITY;
ALTER TABLE mahnungen ENABLE ROW LEVEL SECURITY;
ALTER TABLE leistungsverzeichnisse ENABLE ROW LEVEL SECURITY;
ALTER TABLE lv_positionen ENABLE ROW LEVEL SECURITY;
ALTER TABLE nachtraege ENABLE ROW LEVEL SECURITY;
ALTER TABLE aufmasse ENABLE ROW LEVEL SECURITY;
ALTER TABLE aufmass_positionen ENABLE ROW LEVEL SECURITY;
ALTER TABLE zahlungen ENABLE ROW LEVEL SECURITY;
ALTER TABLE nummernkreise ENABLE ROW LEVEL SECURITY;
ALTER TABLE pdf_templates ENABLE ROW LEVEL SECURITY;

-- Allow all operations for service role (used by our backend)
CREATE POLICY "Service role full access" ON unternehmen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON kunden FOR ALL USING (true);
CREATE POLICY "Service role full access" ON projekte FOR ALL USING (true);
CREATE POLICY "Service role full access" ON dokumente FOR ALL USING (true);
CREATE POLICY "Service role full access" ON positionen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON abschlagsrechnungen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON schlussrechnungen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON mahnungen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON leistungsverzeichnisse FOR ALL USING (true);
CREATE POLICY "Service role full access" ON lv_positionen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON nachtraege FOR ALL USING (true);
CREATE POLICY "Service role full access" ON aufmasse FOR ALL USING (true);
CREATE POLICY "Service role full access" ON aufmass_positionen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON zahlungen FOR ALL USING (true);
CREATE POLICY "Service role full access" ON nummernkreise FOR ALL USING (true);
CREATE POLICY "Service role full access" ON pdf_templates FOR ALL USING (true);
