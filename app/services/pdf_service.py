"""PDF generation service using WeasyPrint."""

import os
from pathlib import Path
from uuid import UUID

from jinja2 import Environment, FileSystemLoader

from app.utils.enums import DocumentType
from app.utils.formatting import format_date, format_einheit, format_eur, format_menge

# Base directory for templates
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
STATIC_DIR = Path(__file__).parent.parent / "static"

# Template mapping for default PDF templates
DEFAULT_TEMPLATE_MAP: dict[DocumentType, str] = {
    DocumentType.ANGEBOT: "pdf/default/angebot.html",
    DocumentType.RECHNUNG: "pdf/default/rechnung.html",
    DocumentType.ABSCHLAGSRECHNUNG: "pdf/default/abschlagsrechnung.html",
    DocumentType.SCHLUSSRECHNUNG: "pdf/default/schlussrechnung.html",
    DocumentType.MAHNUNG: "pdf/default/mahnung.html",
    DocumentType.LEISTUNGSVERZEICHNIS: "pdf/default/leistungsverzeichnis.html",
    DocumentType.NACHTRAG: "pdf/default/nachtrag.html",
    DocumentType.AUFMASS: "pdf/default/aufmass.html",
}


def _create_jinja_env() -> Environment:
    """Create a Jinja2 environment with German formatting filters."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
    )
    env.filters["format_eur"] = format_eur
    env.filters["format_date"] = format_date
    env.filters["format_menge"] = format_menge
    env.filters["format_einheit"] = format_einheit
    return env


def render_html(
    template_path: str,
    context: dict,
    custom_html: str | None = None,
    custom_css: str | None = None,
) -> str:
    """
    Render a document to HTML.

    If custom_html is provided (from uploaded template), use that instead
    of the file-based template.
    """
    env = _create_jinja_env()

    if custom_html:
        # Use uploaded template string
        template = env.from_string(custom_html)
    else:
        template = env.get_template(template_path)

    # Add CSS to context if custom
    if custom_css:
        context["custom_css"] = custom_css

    context["static_dir"] = str(STATIC_DIR)
    return template.render(**context)


def generate_pdf(
    template_path: str,
    context: dict,
    custom_html: str | None = None,
    custom_css: str | None = None,
) -> bytes:
    """
    Generate a PDF from a template and context data.

    Returns PDF bytes.
    """
    try:
        from weasyprint import HTML
    except ImportError:
        raise RuntimeError(
            "WeasyPrint is not installed. Install it with: pip install weasyprint"
        )

    html_content = render_html(template_path, context, custom_html, custom_css)
    base_url = str(TEMPLATE_DIR)
    pdf_bytes = HTML(string=html_content, base_url=base_url).write_pdf()
    return pdf_bytes


def get_template_path(doc_type: DocumentType) -> str:
    """Get the default template path for a document type."""
    return DEFAULT_TEMPLATE_MAP.get(doc_type, "pdf/default/rechnung.html")
