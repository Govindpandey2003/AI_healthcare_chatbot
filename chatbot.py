
def get_bot_response(user_message, chat_history= None
):
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
