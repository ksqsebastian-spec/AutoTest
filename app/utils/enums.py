from enum import Enum


class DocumentType(str, Enum):
    ANGEBOT = "angebot"
    RECHNUNG = "rechnung"
    ABSCHLAGSRECHNUNG = "abschlagsrechnung"
    SCHLUSSRECHNUNG = "schlussrechnung"
    MAHNUNG = "mahnung"
    LEISTUNGSVERZEICHNIS = "leistungsverzeichnis"
    NACHTRAG = "nachtrag"
    AUFMASS = "aufmass"


class DocumentStatus(str, Enum):
    ENTWURF = "entwurf"
    GESENDET = "gesendet"
    AKZEPTIERT = "akzeptiert"
    ABGELEHNT = "abgelehnt"
    BEZAHLT = "bezahlt"
    TEILBEZAHLT = "teilbezahlt"
    UEBERFAELLIG = "ueberfaellig"
    STORNIERT = "storniert"


class TaxRateType(str, Enum):
    STANDARD = "standard"       # 19%
    ERMAESSIGT = "ermaessigt"   # 7%
    BEFREIT = "befreit"         # 0%


class Einheit(str, Enum):
    STUECK = "stueck"
    STUNDE = "stunde"
    M = "m"
    M2 = "m2"
    M3 = "m3"
    KG = "kg"
    T = "t"
    PAUSCHAL = "pauschal"
    LFM = "lfm"
    LITER = "liter"
    TAG = "tag"


class ProjektStatus(str, Enum):
    GEPLANT = "geplant"
    AKTIV = "aktiv"
    PAUSIERT = "pausiert"
    ABGESCHLOSSEN = "abgeschlossen"
    ABGERECHNET = "abgerechnet"


class Mahnstufe(str, Enum):
    ERSTE = "erste"
    ZWEITE = "zweite"
    DRITTE = "dritte"


# Display labels for German UI
EINHEIT_LABELS: dict[Einheit, str] = {
    Einheit.STUECK: "Stk.",
    Einheit.STUNDE: "Std.",
    Einheit.M: "m",
    Einheit.M2: "m\u00b2",
    Einheit.M3: "m\u00b3",
    Einheit.KG: "kg",
    Einheit.T: "t",
    Einheit.PAUSCHAL: "psch.",
    Einheit.LFM: "lfm",
    Einheit.LITER: "l",
    Einheit.TAG: "Tag(e)",
}

DOCUMENT_TYPE_LABELS: dict[DocumentType, str] = {
    DocumentType.ANGEBOT: "Angebot",
    DocumentType.RECHNUNG: "Rechnung",
    DocumentType.ABSCHLAGSRECHNUNG: "Abschlagsrechnung",
    DocumentType.SCHLUSSRECHNUNG: "Schlussrechnung",
    DocumentType.MAHNUNG: "Mahnung",
    DocumentType.LEISTUNGSVERZEICHNIS: "Leistungsverzeichnis",
    DocumentType.NACHTRAG: "Nachtrag",
    DocumentType.AUFMASS: "Aufmass",
}

DOCUMENT_STATUS_LABELS: dict[DocumentStatus, str] = {
    DocumentStatus.ENTWURF: "Entwurf",
    DocumentStatus.GESENDET: "Gesendet",
    DocumentStatus.AKZEPTIERT: "Akzeptiert",
    DocumentStatus.ABGELEHNT: "Abgelehnt",
    DocumentStatus.BEZAHLT: "Bezahlt",
    DocumentStatus.TEILBEZAHLT: "Teilbezahlt",
    DocumentStatus.UEBERFAELLIG: "Ueberfaellig",
    DocumentStatus.STORNIERT: "Storniert",
}

PROJEKT_STATUS_LABELS: dict[ProjektStatus, str] = {
    ProjektStatus.GEPLANT: "Geplant",
    ProjektStatus.AKTIV: "Aktiv",
    ProjektStatus.PAUSIERT: "Pausiert",
    ProjektStatus.ABGESCHLOSSEN: "Abgeschlossen",
    ProjektStatus.ABGERECHNET: "Abgerechnet",
}

MAHNSTUFE_LABELS: dict[Mahnstufe, str] = {
    Mahnstufe.ERSTE: "1. Mahnung",
    Mahnstufe.ZWEITE: "2. Mahnung",
    Mahnstufe.DRITTE: "3. Mahnung",
}

TAX_RATES: dict[TaxRateType, float] = {
    TaxRateType.STANDARD: 19.0,
    TaxRateType.ERMAESSIGT: 7.0,
    TaxRateType.BEFREIT: 0.0,
}
