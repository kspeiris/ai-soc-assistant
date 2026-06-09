from openai import OpenAI
from ..config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def explain_alert(alert_description: str) -> str:
    prompt = f"""
You are a SOC analyst AI. Explain the following security alert in simple terms, describe the potential risk, and suggest immediate mitigation steps.

Alert: {alert_description}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def chat_assistant(user_message: str, context: str = "") -> str:
    system_prompt = """You are an AI SOC assistant. Help analysts understand alerts, MITRE ATT&CK techniques, mitigation steps, and incident response."""
    full_prompt = f"{system_prompt}\nContext from knowledge base:\n{context}\nUser: {user_message}\nAssistant:"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content