import requests

BASE_URL = "http://localhost:8000"

print("Registering admin...")
resp = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
})
if resp.status_code == 200:
    print("Registered admin user.")
else:
    print("Admin might already exist:", resp.text)

print("Logging in...")
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
})
if resp.status_code == 200:
    token = resp.json().get("access_token")
    print("Logged in successfully, token retrieved.")
else:
    print("Login failed:", resp.text)
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

logs = [
    {
        "source_ip": "192.168.1.100",
        "event_type": "Failed Login",
        "raw_log": "sshd[12345]: Failed password for invalid user root from 192.168.1.100 port 2222 ssh2",
        "severity": "high"
    },
    {
        "source_ip": "10.0.0.5",
        "event_type": "Malware Detected",
        "raw_log": "Antivirus alert: Trojan.Ransomware in C:\\Users\\Public\\Downloads\\invoice.exe",
        "severity": "critical"
    },
    {
        "source_ip": "172.16.0.2",
        "event_type": "Privilege Escalation",
        "raw_log": "sudo: developer : TTY=pts/0 ; PWD=/home/developer ; USER=root ; COMMAND=/bin/bash",
        "severity": "medium"
    },
    {
        "source_ip": "192.168.1.15",
        "event_type": "Port Scan",
        "raw_log": "Firewall block: multiple connection attempts from 192.168.1.15 to ports 21, 22, 23, 80",
        "severity": "low"
    }
]

for log in logs:
    r = requests.post(f"{BASE_URL}/logs/ingest", json=log, headers=headers)
    print(f"Ingested log '{log['event_type']}': Status {r.status_code}")

print("\nSeed data added successfully!")
