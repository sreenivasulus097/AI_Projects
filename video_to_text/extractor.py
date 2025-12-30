import re

class ProfileExtractor:
    def extract(self, text: str) -> dict:
        profile = {
            "name": None,
            "role": None,
            "company": None,
            "confidence": 0.0
        }

        # Very simple heuristic extraction (baseline)
        name_match = re.search(r"([A-Z][a-z]+ [A-Z][a-z]+)", text)
        role_match = re.search(r"\b(CEO|Director|Manager|Founder|Engineer)\b", text, re.I)
        company_match = re.search(r"at ([A-Z][A-Za-z0-9 &]+)", text)

        if name_match:
            profile["name"] = name_match.group(1)
            profile["confidence"] += 0.3

        if role_match:
            profile["role"] = role_match.group(1)
            profile["confidence"] += 0.3

        if company_match:
            profile["company"] = company_match.group(1)
            profile["confidence"] += 0.2

        return profile
