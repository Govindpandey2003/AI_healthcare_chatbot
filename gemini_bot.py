"""Gemini-powered healthcare assistant with tools for Indian medicine
lookup (local dataset) and drug safety labels (openFDA).

Needs GEMINI_API_KEY in the environment or in a .env file.
Get a free key at https://aistudio.google.com/apikey
"""

import os

from dotenv import load_dotenv

import medicine_data
import openfda

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are GoviCare AI, a friendly healthcare information assistant for users in India.

Rules:
- Give general, educational health information only. Never diagnose, never prescribe, and never give personalised doses. Encourage seeing a qualified doctor or pharmacist when appropriate.
- If the user describes anything that could be an emergency (chest pain, trouble breathing, stroke signs, severe bleeding, unconsciousness, suicidal thoughts, poisoning), tell them to call 112 (India emergency) or go to the nearest hospital immediately, before anything else. For mental-health crises also mention Tele-MANAS 14416.
- Reply in the same language and style as the user: English, Hindi, or Hinglish (Hindi in Roman script).
- When the user mentions a medicine brand or salt, call search_indian_medicine to get Indian brand names, prices in ₹, manufacturers and compositions. Use cheaper_alternatives when they ask about cheaper or generic options, and mention Jan Aushadhi Kendras as a low-cost source of generics.
- For side effects, warnings, interactions or pregnancy questions, call drug_safety_info with the generic salt name. That data comes from U.S. FDA labels; say so, and note that Indian labelling may differ.
- Keep answers concise and easy to read: short paragraphs or bullet points.
- Never invent medicine names, prices or facts. If a tool returns nothing, say you could not find it."""


def search_indian_medicine(query: str) -> list[dict]:
    """Search medicines sold in India by brand name or salt/composition.

    Args:
        query: Brand name (e.g. "Dolo 650") or salt (e.g. "paracetamol").

    Returns:
        Up to 8 matching medicines with id, name, price in rupees,
        manufacturer, pack size and composition.
    """
    results = medicine_data.search_medicines(query, limit=8)
    return [
        {k: m[k] for k in ("id", "name", "price", "manufacturer",
                           "pack_size", "composition")}
        for m in results
    ]


def cheaper_alternatives(medicine_id: int) -> list[dict]:
    """List other Indian brands with exactly the same composition and
    strength, cheapest first.

    Args:
        medicine_id: The id from a search_indian_medicine result.
    """
    med = medicine_data.get_medicine(medicine_id)
    if not med:
        return []
    return [
        {k: m[k] for k in ("name", "price", "manufacturer", "pack_size")}
        for m in medicine_data.find_alternatives(med, limit=8)
    ]


def drug_safety_info(generic_name: str) -> dict:
    """Get uses, warnings, side effects and interactions for a generic
    drug from the U.S. FDA label database (openFDA).

    Args:
        generic_name: Generic salt name, e.g. "paracetamol" or "cetirizine".
    """
    label = openfda.get_drug_label(generic_name, max_chars=800)
    if not label:
        return {"found": False, "generic_name": generic_name}
    return {"found": True, "source": "U.S. FDA label (openFDA)", **label}


TOOLS = [search_indian_medicine, cheaper_alternatives, drug_safety_info]


def is_configured():
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))


def model_name():
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL)


_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        )
    return _client


def ask_gemini(user_message, chat_history=None):
    """chat_history: list of {'role': 'user'|'assistant', 'content': str}."""
    from google.genai import types

    contents = []
    for msg in (chat_history or [])[-20:]:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(types.Content(
            role=role, parts=[types.Part.from_text(text=msg["content"])]
        ))
    chat = _get_client().chats.create(
        model=model_name(),
        history=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=TOOLS,  # Gemini calls these Python functions itself
            temperature=0.4,
        ),
    )
    response = chat.send_message(user_message)
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    return text
