# Complete MITRE ATT&CK mapping (expanded)
MITRE_MAPPING = {
    "bruteforce": "T1110",
    "password_guessing": "T1110.001",
    "password_spraying": "T1110.003",
    "privilege_escalation": "T1068",
    "malware": "T1204",
    "phishing": "T1566",
    "lateral_movement": "T1021",
    "persistence": "T1547",
    "defense_evasion": "T1070",
    "credential_dumping": "T1003",
    "command_and_control": "T1071",
    "exfiltration": "T1048"
}

def map_to_mitre(attack_type: str) -> str:
    return MITRE_MAPPING.get(attack_type.lower(), "Unknown")

def get_mitre_description(technique_id: str) -> str:
    descriptions = {
        "T1110": "Brute Force: Adversaries may use brute force techniques to gain access to accounts.",
        "T1110.001": "Password Guessing: Repeatedly guess passwords.",
        "T1068": "Exploitation for Privilege Escalation.",
        "T1204": "User Execution: Malware runs when user opens a file or link.",
        "T1566": "Phishing: Adversaries send malicious emails.",
        "T1021": "Remote Services: Use of remote access protocols.",
        "T1547": "Boot or Logon Autostart Execution.",
        "T1070": "Indicator Removal on Host.",
        "T1003": "OS Credential Dumping.",
        "T1071": "Application Layer Protocol.",
        "T1048": "Exfiltration Over Alternative Protocol."
    }
    return descriptions.get(technique_id, "No description available.")