from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from ..config import settings

# Load MITRE ATT&CK knowledge base (simplified)
mitre_knowledge = [
    "T1110: Brute force - attacker tries many passwords.",
    "T1068: Exploitation for privilege escalation.",
    "T1204: User execution - malware runs when user opens file."
]

def retrieve_context(query: str) -> str:
    # In production, use a real vector DB with MITRE ATT&CK data
    # Here we do keyword matching
    query_lower = query.lower()
    relevant = []
    for tech in mitre_knowledge:
        if any(word in tech.lower() for word in query_lower.split()):
            relevant.append(tech)
    return "\n".join(relevant) if relevant else "No relevant MITRE technique found."