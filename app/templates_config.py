"""Shared Jinja2 templates instance with custom filters."""

from fastapi.templating import Jinja2Templates

from app.utils.formatting import format_date, format_einheit, format_eur, format_menge

templates = Jinja2Templates(directory="app/templates")
templates.env.filters["format_eur"] = format_eur
templates.env.filters["format_date"] = format_date
templates.env.filters["format_menge"] = format_menge
templates.env.filters["format_einheit"] = format_einheit
