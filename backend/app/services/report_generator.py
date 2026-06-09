from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from ..models import Incident

def generate_incident_report(incident: Incident) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, f"Incident Report: {incident.title}")
    c.drawString(100, 730, f"ID: {incident.id}")
    c.drawString(100, 710, f"Severity: {incident.severity.value}")
    c.drawString(100, 690, f"Status: {incident.status.value}")
    c.drawString(100, 670, f"Created: {incident.created_at}")
    if incident.resolved_at:
        c.drawString(100, 650, f"Resolved: {incident.resolved_at}")
    c.drawString(100, 630, "Description:")
    text = incident.description
    c.drawString(100, 610, text[:80])
    c.save()
    buffer.seek(0)
    return buffer.getvalue()