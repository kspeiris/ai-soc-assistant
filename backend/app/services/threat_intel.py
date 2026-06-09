import httpx
from typing import Optional
from ..config import settings

async def check_ip_reputation(ip: str) -> dict:
    """
    Check IP reputation using AbuseIPDB (free tier)
    """
    if not settings.ABUSEIPDB_API_KEY:
        return {"reputation": "unknown", "message": "No API key"}
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://api.abuseipdb.com/api/v2/check",
                params={"ipAddress": ip, "maxAgeInDays": 90},
                headers={"Key": settings.ABUSEIPDB_API_KEY, "Accept": "application/json"}
            )
            data = resp.json()
            return {
                "reputation": "malicious" if data["data"]["abuseConfidenceScore"] > 50 else "clean",
                "score": data["data"]["abuseConfidenceScore"],
                "country": data["data"].get("countryCode", "Unknown"),
                "reports": len(data["data"].get("reports", []))
            }
        except Exception as e:
            return {"reputation": "error", "message": str(e)}

# Add to config.py: ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")