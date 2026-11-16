import re

import gemini_bot
import medicine_data


def rule_based_response(user_message):
    message = user_message.lower().strip()

    # Emergency symptoms
    emergency_words = [
        "chest pain", "pain in chest", "chest hurts",
        "chest mein dard", "seene mein dard", "seene me dard",
        "saans nahi aa rahi", "saans lene mein dikkat",
        "breathing difficulty", "difficulty breathing",
        "can't breathe", "cannot breathe","accident",
        "severe bleeding", "unconscious", "stroke",
        "face drooping", "sudden weakness one side"
    ]

    if any(word in message for word in emergency_words):
        return (
            "EMERGENCY ALERT: These symptoms may indicate a serious "
            "medical emergency. Call 112 in India or visit the nearest "
            "emergency department immediately. Do not delay medical help."
        )

    # Greeting
    elif any(word in message.split() for word in [
        "hello","hlo", "hi", "hey", "namaste"
    ]):
        return (
            "Hello! Welcome to AI Healthcare Assistant. "
            "How can I help you today?"
        )

    # Fever
    elif any(word in message for word in [
        "fever", "bukhar", "temperature"
    ]):
        return (
            "Fever can have many causes. Drink enough fluids, rest "
            "and monitor your temperature. Consult a doctor if fever "
            "persists, worsens or is accompanied by serious symptoms."
        )

    # Headache
    elif any(word in message for word in [
        "headache", "sir dard", "head pain", "sar dard"
    ]):
        return (
            "Headache may occur due to several reasons. Rest and stay "
            "hydrated. Seek medical advice if it is severe, unusual "
            "or persistent."
        )

    # Allergy and itching
    elif any(word in message for word in [
        "itch", "itching", "khujli", "khujali",
        "allergy", "rash", "skin irritation"
    ]):
        return (
            "Itching can have several causes, including skin irritation "
            "or allergy. Avoid scratching and possible triggers. "
            "Consult a doctor if it persists or worsens. If you have "
            "breathing difficulty or tongue/throat swelling, seek "
            "emergency help immediately."
        )

    # Cough and cold
    elif any(word in message for word in [
        "cough", "coughing", "khansi", "khasi",
        "cold", "jukam", "sardi"
    ]):
        return (
            "Cough and cold can occur due to infections, allergies "
            "or irritation. Drink fluids and rest. Consult a doctor "
            "if symptoms persist or worsen."
        )

    # Stomach pain
    elif any(word in message for word in [
        "stomach pain", "pet dard", "abdominal pain","period pain","period cramps"
    ]):
        return (
            "Stomach pain can have different causes. Seek medical "
            "attention if pain is severe, persistent or worsening."
        )

    # Diabetes
    elif any(word in message.split() for word in [
        "diabetes", "sugar"
    ]) or "blood sugar" in message:
        return (
            "Diabetes is a condition in which blood glucose levels "
            "remain higher than normal. Blood sugar testing and "
            "medical guidance are important. Consult a healthcare "
            "professional for diagnosis and treatment."
        )

    # Blood Pressure
    elif any(word in message for word in [
        "blood pressure", "high bp", "low bp", "bp problem"
    ]):
        return (
            "Blood pressure measures the force of blood against "
            "artery walls. Both high and low BP may need medical "
            "attention. Monitor it and consult a doctor for guidance."
        )

    # Vomiting
    elif any(word in message for word in [
        "vomiting", "vomit", "ulti", "ultee"
    ]):
        return (
            "Vomiting can happen due to infections, food-related "
            "problems or other causes. Take small sips of fluids. "
            "Seek medical help if vomiting continues, you cannot "
            "keep fluids down or show signs of dehydration."
        )

    # Diarrhea
    elif any(word in message for word in [
        "diarrhea", "loose motion", "loose motions", "dast"
    ]):
        return (
            "Diarrhea can cause dehydration. Drink safe fluids and "
            "use ORS prepared according to packet instructions. "
            "Seek medical help if there is blood in stool, severe "
            "dehydration or persistent symptoms."
        )

    # Weakness
    elif any(word in message for word in [
        "weakness", "weak", "kamzori", "tired", "fatigue"
    ]):
        return (
            "Weakness can have many causes, including lack of sleep, "
            "dehydration or nutritional problems. Eat balanced meals "
            "and stay hydrated. Consult a doctor if it persists "
            "or is unexplained."
        )

    # Sleep problems
    elif any(word in message for word in [
        "sleep problem", "insomnia", "neend nahi aati", "sleep"
    ]):
        return (
            "A regular sleep schedule, a comfortable sleeping "
            "environment and limiting caffeine late in the day "
            "may help. Consult a doctor if sleep problems continue."
        )

    # Goodbye
    elif any(word in message.split() for word in [
        "bye","byy", "goodbye"
    ]):
        return "Goodbye!😊 Take care of your health."

    else:
        return (
            "I'm still learning. Please describe your health problem "
            "in simple words. I can provide general health information, "
            "not a medical diagnosis."
        )


MEDICINE_WORDS = [
    "price", "cost", "kimat", "keemat", "medicine", "tablet", "syrup",
    "capsule", "dawa", "dawai", "alternative", "generic", "substitute",
]
MEDICINE_WORDS += [
    "medicines", "tablets", "dawai", "davai", "goli", "brand", "brands",
    "mrp", "rate", "rs", "rupees",
]
STOP_WORDS = set(MEDICINE_WORDS) | {
    "what", "is", "the", "of", "for", "a", "an", "kya", "hai", "ki", "ka",
    "ke", "me", "mein", "batao", "tell", "about", "cheaper", "cheap",
    "sasta", "please", "show", "find", "give", "do", "does", "you", "your",
    "any", "some", "i", "my", "can", "could", "should", "would", "will",
    "take", "use", "need", "want", "get", "buy", "how", "much", "many",
    "and", "or", "to", "in", "on", "with", "it", "this", "that", "are",
    "there", "is", "mujhe", "muje", "koi", "kuch", "kaise", "kitna",
    "kitni", "hain", "ho", "se", "ko", "liye", "lena", "chahiye", "de",
    "do", "dijiye", "sir", "mam", "ji", "hello", "hi", "pls", "plz",
    "name", "names", "list", "information", "info", "details",
}
# Asking the bot to choose a medicine: never answer with a list of drugs.
RECOMMEND_WORDS = [
    "recommend", "suggest", "prescribe", "which medicine", "best medicine",
    "kaun si", "kaunsi", "konsi", "kon si", "konsa", "kaunsa",
    "kya lu", "kya lun", "kya khau", "kya khaun",
]


def medicine_lookup_response(user_message):
    """Offline medicine price/composition lookup for messages like
    'price of dolo 650' or 'crocin ki kimat'.

    Only answers when the message names a real brand or salt; it never
    picks a medicine for the user.
    """
    message = user_message.lower()
    if not any(word in message for word in MEDICINE_WORDS):
        return None
    if any(word in message for word in RECOMMEND_WORDS):
        return (
            "I can't recommend or prescribe medicines. Please consult a "
            "doctor or pharmacist, who can check your symptoms and "
            "history. If you already know a medicine's name, ask me its "
            "price or composition, e.g. *dolo 650 ki kimat*."
        )
    words = [w for w in re.findall(r"[a-z0-9]+", message)
             if w not in STOP_WORDS]
    # The first real word must be a name (3+ letters), not a number.
    names = [w for w in words if len(w) >= 3 and not w.isdigit()]
    if not names:
        return None
    term = names[0]
    query = " ".join(words[words.index(term):])
    try:
        results = medicine_data.search_medicines(query, limit=5)
        if not results and query != term:
            results = medicine_data.search_medicines(term, limit=5)
    except Exception:
        return None
    # Keep only results that really match: brand starts with the term,
    # or the term is part of the salt name.
    results = [
        m for m in results
        if m["name"].lower().startswith(term)
        or term in m["composition"].lower()
    ]
    if not results:
        return None
    lines = ["Here is what I found in the Indian medicine database:"]
    for m in results:
        lines.append(
            f"- **{m['name']}**: ₹{m['price']} ({m['pack_size']}) by "
            f"{m['manufacturer']}. Contains {m['composition']}"
        )
    lines.append(
        "\nOpen *Medicine Information* in the menu to see cheaper "
        "alternatives and safety details. Always take medicines as "
        "advised by a doctor or pharmacist."
    )
    return "\n".join(lines)


def is_emergency(user_message):
    reply = rule_based_response(user_message)
    return reply.startswith("EMERGENCY ALERT")


def get_bot_response(user_message, chat_history=None):
    """Returns (reply, source), where source is 'gemini', 'rules' or 'emergency'.

    Emergencies are always answered by the fixed rule, so the 112 advice
    never depends on the network or the model.
    """
    if is_emergency(user_message):
        return rule_based_response(user_message), "emergency"

    if gemini_bot.is_configured():
        try:
            return gemini_bot.ask_gemini(user_message, chat_history), "gemini"
        except Exception as exc:  # network, quota, bad key...
            fallback = (medicine_lookup_response(user_message)
                        or rule_based_response(user_message))
            return (f"{fallback}\n\n_(Gemini is unavailable right now: "
                    f"{type(exc).__name__}. Showing a basic answer.)_",
                    "rules")

    return (medicine_lookup_response(user_message)
            or rule_based_response(user_message)), "rules"
