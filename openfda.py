"""Drug safety information from the U.S. FDA drug label API (openFDA).

openFDA has no Indian brand names, so we look up by generic salt name
(taken from the Indian dataset's composition) and translate the common
Indian (INN/BP) spellings to the U.S. (USAN) names first.
"""

import requests

LABEL_URL = "https://api.fda.gov/drug/label.json"

# Indian / British spelling -> U.S. generic name used in FDA labels
INDIAN_TO_US_NAMES = {
    "paracetamol": "acetaminophen",
    "amoxycillin": "amoxicillin",
    "salbutamol": "albuterol",
    "levosalbutamol": "levalbuterol",
    "frusemide": "furosemide",
    "glibenclamide": "glyburide",
    "adrenaline": "epinephrine",
    "noradrenaline": "norepinephrine",
    "lignocaine": "lidocaine",
    "cephalexin": "cephalexin",
    "cefalexin": "cephalexin",
    "rifampicin": "rifampin",
    "clavulanic acid": "clavulanate potassium",
    "mesalazine": "mesalamine",
    "pethidine": "meperidine",
    "chlorpheniramine maleate": "chlorpheniramine",
    "chlorphenamine": "chlorpheniramine",
    "ciclosporin": "cyclosporine",
    "oxetacaine": "oxethazaine",
}

# Sections shown to the user, in order
SECTIONS = [
    ("indications_and_usage", "Uses"),
    ("warnings", "Warnings"),
    ("boxed_warning", "Boxed warning"),
    ("do_not_use", "Do not use"),
    ("contraindications", "Contraindications"),
    ("adverse_reactions", "Side effects"),
    ("drug_interactions", "Interactions"),
    ("pregnancy_or_breast_feeding", "Pregnancy / breastfeeding"),
]


def to_us_name(salt):
    s = salt.strip().lower()
    return INDIAN_TO_US_NAMES.get(s, s)


def _trim(text, max_chars):
    text = " ".join(text.split())
    return text if len(text) <= max_chars else text[:max_chars].rsplit(" ", 1)[0] + "..."


def get_drug_label(generic_name, max_chars=600):
    """Return {'name', 'sections': {title: text}} or None if not found."""
    name = to_us_name(generic_name)
    if not name:
        return None
    for field in ("openfda.generic_name", "openfda.substance_name"):
        try:
            resp = requests.get(
                LABEL_URL,
                params={"search": f'{field}:"{name}"', "limit": 1},
                timeout=15,
            )
        except requests.RequestException:
            return None
        if resp.status_code == 404:
            continue
        if not resp.ok:
            return None
        results = resp.json().get("results") or []
        if not results:
            continue
        label = results[0]
        sections = {}
        for key, title in SECTIONS:
            if label.get(key):
                sections[title] = _trim(" ".join(label[key]), max_chars)
        return {"name": name, "sections": sections}
    return None
