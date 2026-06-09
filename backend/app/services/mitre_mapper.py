def map_to_mitre(attack_type: str) -> str:
    mapping = {
        "bruteforce": "T1110",
        "privilege_escalation": "T1068",
        "malware": "T1204",
        "phishing": "T1566",
        "lateral_movement": "T1021"
    }
    return mapping.get(attack_type.lower(), "Unknown")