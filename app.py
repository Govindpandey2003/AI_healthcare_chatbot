
import pandas as pd
import streamlit as st

import gemini_bot
import medicine_data
import openfda
from chatbot import get_bot_response
from database import (
    create_database,
    save_chat,
    get_chat_history,
    clear_chat_history
)
# DATABASE SETUP
create_database()
# PAGE CONFIGURATION
st.set_page_config(
    page_title="🤖 GoviCare AI",
    page_icon="🏥",
    layout="wide"
)

# ==================================
# SIDEBAR PROFESSIONAL DESIGN
# ==================================

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102D4F, #174D75);
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    padding: 10px 12px;
    border-radius: 9px;
    margin-bottom: 7px;
    transition: 0.2s;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.20);
}

[data-testid="stSidebar"] .stButton button {
    background: #1769AA;
    color: white;
    border: 1px solid #69B9F5;
    border-radius: 12px;
    height: 48px;
    font-weight: bold;
    width: 100%;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: #2388D1;
    border-color: white;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# DASHBOARD HEADER FUNCTION
# ==================================

def dashboard_header(icon, title, subtitle):

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, #12345a, #1976ad);
            padding: 28px;
            border-radius: 18px;
            margin-bottom: 22px;
            color: white;
        ">
            <h1 style="color:white !important; margin:0;">
                {icon} {title}
            </h1>
            <p style="color:#e5f3ff; font-size:16px;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================
# DASHBOARD CARD FUNCTION
# ==================================

def dashboard_card(icon, title, description):

    with st.container(border=True):

        st.markdown(
            f"<h2 style='text-align:center'>{icon}</h2>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {title}")

        st.write(description)
# ==================================
# SIDEBAR NAVIGATION
# ==================================

def set_main_page():
    st.session_state.active_page = st.session_state.main_menu


def open_chatbot():
    st.session_state.active_page = "Chatbot"


if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"


# Sidebar Logo
st.sidebar.markdown("""
<div style="text-align:center; padding:15px 0;">
    <div style="font-size:48px;">🏥</div>
    <h2 style="color:white; margin:0;">🤖 GOVICARE AI</h2>
    <p style="color:#c9e5ff; font-size:12px;">
        Your Personal Health Assistant
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

# Main Menu
st.sidebar.markdown("### 📋 Main Menu")

st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Healthcare Tools",
        "Symptom Checker",
        "Diet & Nutrition",
        "Medicine Information",
        "First Aid",
        "Health Information"
    ],
    key="main_menu",
    on_change=set_main_page,
    label_visibility="collapsed"
)

st.sidebar.divider()

# Separate Chatbot Section
st.sidebar.markdown("### 🤖 AI Assistant")

st.sidebar.button(
    "🤖  Open Healthcare Chatbot",
    use_container_width=True,
    type="primary",
    on_click=open_chatbot
)

# Current Selected Page
menu = st.session_state.active_page

st.sidebar.divider()
st.sidebar.caption("AI Healthcare Project | Govind Pandey")

# ==================================
# HOME DASHBOARD
# ==================================

if menu == "Home":

    dashboard_header(
        "🏥",
        "AI Healthcare Assistant",
        "Your Personal Healthcare Support System"
    )

    st.markdown("## 👋 Welcome to Your Health Dashboard")

    st.write(
        "Explore healthcare information, symptom guidance, "
        "nutrition support and useful health tracking tools."
    )

    st.divider()

    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Healthcare Modules", "8")
    col2.metric("Health Tools", "12")
    col3.metric("Chatbot Support", "Available")
    col4.metric("Languages", "Hindi / English")

    st.divider()

    st.markdown("## 🩺 Explore Healthcare Services")

    col1, col2, col3 = st.columns(3)

    with col1:
        dashboard_card(
            "🩺",
            "Symptom Checker",
            "Select symptoms and receive general health guidance."
        )
    with col2:
        dashboard_card(
            "🥗",
            "Diet & Nutrition",
            "Explore balanced diet and nutrition information."
        )
    with col3:
        dashboard_card(
            "💊",
            "Medicine Information",
            "Learn about common medicines and precautions."
        )
    col1, col2, col3 = st.columns(3)
    with col1:
        dashboard_card(
            "🚑",
            "First Aid",
            "Learn basic first-aid steps for common emergencies."
        )
    with col2:
        dashboard_card(
            "🤖",
            "Healthcare Chatbot",
            "Ask general healthcare-related questions."
        )
    with col3:
        dashboard_card(
            "📚",
            "Health Information",
            "Explore useful health and wellness topics."
        )

    st.divider()

    st.markdown("## ✨ About This Project")

    with st.container(border=True):
        st.write(
            "It provides general health information, symptom guidance, "
            "nutrition information, first-aid guidance and chatbot support."
        )

    st.warning(
        "It is not a substitute for professional medical diagnosis or treatment."
    )

# ==================================
# ADVANCED SYMPTOM CHECKER
# ==================================

elif menu == "Symptom Checker":

    st.title("🩺 Advanced Symptom Checker")

    st.write(
        "Select your symptoms to receive possible explanations "
        "and general health guidance."
    )

    st.warning(
        "This tool cannot diagnose diseases. Its suggestions are "
        "educational and should not replace medical evaluation."
    )

    symptoms = st.multiselect(
        "Select all symptoms you are experiencing",
        [
            "Fever",
            "Headache",
            "Cough",
            "Cold",
            "Sore Throat",
            "Stomach Pain",
            "Vomiting",
            "Diarrhea",
            "Weakness",
            "Body Pain",
            "Dizziness",
            "Skin Rash",
            "Chest Pain",
            "Difficulty Breathing",
            "Severe Bleeding",
            "Fainting",
            "Confusion"
        ]
    )

    severity = st.selectbox(
        "Select symptom severity",
        ["Mild", "Moderate", "Severe"]
    )

    duration = st.selectbox(
        "How long have you had these symptoms?",
        [
            "Less than 24 hours",
            "1-3 days",
            "4-7 days",
            "More than 7 days"
        ]
    )

    age = st.number_input(
        "Enter your age",
        min_value=1,
        max_value=120,
        value=24
    )

    if st.button("Analyze Symptoms"):

        if not symptoms:
            st.error("Please select at least one symptom.")

        else:

            emergency_symptoms = [
                "Chest Pain",
                "Difficulty Breathing",
                "Severe Bleeding",
                "Fainting",
                "Confusion"
            ]

            emergency_found = [
                s for s in symptoms
                if s in emergency_symptoms
            ]

            st.divider()
            st.subheader("🔍 Symptom Analysis")

            # Emergency assessment
            if emergency_found:

                st.error(
                    "🚨 WARNING: You have selected one or more "
                    "potentially serious symptoms."
                )

                st.write(
                    "Selected warning signs: "
                    + ", ".join(emergency_found)
                )

                st.write(
                    "Seek immediate medical assessment. "
                    "Call 112 in India if you need emergency assistance. "
                    "Do not wait for this tool to assess your condition."
                )

            else:
                # Possible explanations
                possible_causes = []

                if "Fever" in symptoms:
                    possible_causes.append(
                        "Fever may occur with viral infections, "
                        "other infections or inflammatory conditions."
                    )

                if "Headache" in symptoms:
                    possible_causes.append(
                        "Headache can be associated with dehydration, "
                        "stress, lack of sleep or migraine."
                    )

                if "Cough" in symptoms or "Cold" in symptoms:
                    possible_causes.append(
                        "Cough or cold symptoms can occur with "
                        "common respiratory infections or allergies."
                    )

                if "Sore Throat" in symptoms:
                    possible_causes.append(
                        "A sore throat may be caused by viral infections, "
                        "irritation or other throat conditions."
                    )

                if "Stomach Pain" in symptoms:
                    possible_causes.append(
                        "Stomach pain can have several causes, including "
                        "indigestion, infection or digestive problems."
                    )

                if "Vomiting" in symptoms:
                    possible_causes.append(
                        "Vomiting may occur due to stomach infections, "
                        "food-related illness or other conditions."
                    )

                if "Diarrhea" in symptoms:
                    possible_causes.append(
                        "Diarrhea can occur due to infections, "
                        "food intolerance or digestive conditions."
                    )

                if "Weakness" in symptoms:
                    possible_causes.append(
                        "Weakness may be associated with dehydration, "
                        "poor sleep, infection or nutritional problems."
                    )

                if "Body Pain" in symptoms:
                    possible_causes.append(
                        "Body pain may accompany viral illnesses, "
                        "muscle strain or physical exertion."
                    )

                if "Dizziness" in symptoms:
                    possible_causes.append(
                        "Dizziness can be associated with dehydration, "
                        "low blood pressure or inner-ear problems."
                    )

                if "Skin Rash" in symptoms:
                    possible_causes.append(
                        "Skin rashes can occur due to allergies, "
                        "irritation or skin infections."
                    )

                st.subheader("Possible Explanations")

                for cause in possible_causes:
                    st.write("• " + cause)

                # Severity assessment
                st.subheader("Severity Assessment")

                if severity == "Severe":
                    st.error(
                        "Severe symptoms require prompt medical "
                        "assessment. Seek urgent care, especially "
                        "if symptoms are worsening."
                    )

                elif severity == "Moderate":
                    st.warning(
                        "Consider consulting a healthcare professional, "
                        "particularly if symptoms persist or worsen."
                    )

                else:
                    st.info(
                        "If symptoms are mild, monitor them and "
                        "maintain adequate rest and hydration."
                    )

                # Duration assessment
                st.subheader("Duration Assessment")

                if duration == "More than 7 days":
                    st.warning(
                        "Symptoms lasting more than 7 days should "
                        "be evaluated by a healthcare professional."
                    )

                elif duration == "4-7 days":
                    st.info(
                        "If symptoms are not improving, arrange "
                        "a medical consultation."
                    )

                else:
                    st.write(
                        "Continue monitoring your symptoms. "
                        "Seek medical advice if they worsen."
                    )

                # General recommendations
                st.subheader("General Recommendations")

                st.write("• Drink adequate fluids.")
                st.write("• Get sufficient rest.")
                st.write("• Maintain proper hygiene.")
                st.write("• Avoid self-medication.")
                st.write(
                    "• Consult a doctor if symptoms persist "
                    "or become worse."
                )

            # Patient summary
            st.divider()
            st.subheader("Patient Summary")

            st.write("**Age:**", age)
            st.write("**Selected Symptoms:**", ", ".join(symptoms))
            st.write("**Severity:**", severity)
            st.write("**Duration:**", duration)

            st.caption(
                "Educational guidance only. This application "
                "does not identify or confirm any disease. "
                "A qualified healthcare professional must "
                "evaluate medical conditions."
            )        
# ==================================
# DIET AND NUTRITION
# ==================================

elif menu == "Diet & Nutrition":

    st.title("🥗 Diet & Nutrition")

    goal = st.selectbox(
        "Select your health goal",
        [
            "General Healthy Diet",
            "Weight Gain",
            "Weight Management",
            "Improve Energy"
        ]
    )

    if st.button("Get Diet Plan"):

        if goal == "General Healthy Diet":

            st.subheader("Daily Healthy Diet")

            st.write("🌅 Breakfast: Poha or oats with milk")
            st.write("🍎 Mid-morning: Seasonal fruit")
            st.write("🍛 Lunch: Roti, dal, vegetables and curd")
            st.write("☕ Evening: Roasted chana")
            st.write("🌙 Dinner: Roti, vegetables and dal")

            st.divider()
            st.write("thank you for using this application.😊")

        elif goal == "Weight Gain":

            st.subheader("General Weight Gain Diet")

            st.write("🌅 Breakfast: Milk, banana and oats")
            st.write("🍎 Mid-morning: Peanuts or seasonal fruit")
            st.write("🍛 Lunch: Roti, rice, dal and vegetables")
            st.write("☕ Evening: Milk and roasted chana")
            st.write("🌙 Dinner: Roti, paneer or dal and vegetables")
            st.divider()
            st.write("thank you for using this application.😊")

        elif goal == "Weight Management":

            st.subheader("Balanced Diet")

            st.write("🌅 Breakfast: Vegetable poha")
            st.write("🍎 Mid-morning: Seasonal fruit")
            st.write("🍛 Lunch: Roti, dal, vegetables and salad")
            st.write("☕ Evening: Roasted chana")
            st.write("🌙 Dinner: Roti, vegetables and curd")

            st.divider()
            st.write("thank you for using this application.😊")

        elif goal == "Improve Energy":

            st.subheader("Energy Supporting Diet")

            st.write("🌅 Breakfast: Milk and banana")
            st.write("🍎 Mid-morning: Seasonal fruit")
            st.write("🍛 Lunch: Rice, dal and vegetables")
            st.write("☕ Evening: Nuts or roasted chana")
            st.write("🌙 Dinner: Roti, dal and vegetables")
            st.divider()
            st.write("thank you for using this application.😊")

        st.info(
            "This is general educational information, "
            "not a personalized medical diet plan."
        )


# ==================================
# MEDICINE INFORMATION
# ==================================

elif menu == "Medicine Information":

    st.title("💊 Medicine Information")

    search_tab, basics_tab = st.tabs(
        ["🔎 Search Indian Medicines", "📘 Common Medicines"]
    )

    with search_tab:
        st.write(
            "Search 2.5 lakh+ medicines sold in India by brand or salt "
            "name. See price, manufacturer, composition, cheaper "
            "alternatives with the same composition, and safety "
            "information."
        )

        if not medicine_data.is_ready():
            with st.status("Setting up medicine database (one time)...") as s:
                medicine_data.ensure_database(progress=s.write)
                s.update(label="Medicine database ready", state="complete")

        query = st.text_input(
            "Medicine or salt name",
            placeholder="e.g. Dolo 650, Pan 40, cetirizine"
        )

        if query and len(query.strip()) >= 2:
            results = medicine_data.search_medicines(query, limit=20)

            if not results:
                st.warning("No medicines found. Check the spelling.")
            else:
                options = {
                    f"{m['name']} | ₹{m['price']} | {m['manufacturer']}": m
                    for m in results
                }
                choice = st.selectbox(
                    f"{len(results)} matches", list(options.keys())
                )
                med = options[choice]

                st.subheader(med["name"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Price", f"₹{med['price']}")
                c2.metric("Pack", med["pack_size"] or "-")
                c3.metric("Type", (med["type"] or "-").title())
                st.write(f"**Manufacturer:** {med['manufacturer']}")
                st.write(f"**Composition:** {med['composition'] or '-'}")

                alternatives = medicine_data.find_alternatives(med)
                st.markdown("#### 💰 Cheaper alternatives (same composition)")
                cheaper = [
                    a for a in alternatives
                    if med["price"] and a["price"] < med["price"]
                ]
                if cheaper:
                    saving = med["price"] - cheaper[0]["price"]
                    st.success(
                        f"Lowest price found: ₹{cheaper[0]['price']} "
                        f"(₹{saving:.2f} less). Compare pack sizes, and "
                        "ask your doctor or pharmacist before switching."
                    )
                    st.dataframe(
                        pd.DataFrame(cheaper)[
                            ["name", "price", "pack_size", "manufacturer"]
                        ].rename(columns={
                            "name": "Brand", "price": "Price (₹)",
                            "pack_size": "Pack", "manufacturer": "Manufacturer"
                        }),
                        hide_index=True,
                        use_container_width=True,
                    )
                else:
                    st.info("No cheaper brand with the same composition found.")
                st.caption(
                    "Tip: Pradhan Mantri Bhartiya Janaushadhi Kendras sell "
                    "quality generic medicines at much lower prices."
                )

                st.markdown("#### 🛡️ Safety information")
                for salt in medicine_data.salt_names(med):
                    with st.spinner(f"Looking up {salt}..."):
                        label = openfda.get_drug_label(salt)
                    with st.expander(f"{salt}", expanded=True):
                        if not label or not label["sections"]:
                            st.write("No FDA label found for this salt.")
                            continue
                        for title, text in label["sections"].items():
                            st.markdown(f"**{title}:** {text}")
                st.caption(
                    "Safety text comes from U.S. FDA drug labels (openFDA), "
                    "looked up by generic name; Indian labelling may differ. "
                    f"Prices and brands: {medicine_data.SOURCE_NAME}; "
                    "prices may be outdated."
                )

        st.info(
            "This module provides general educational information. "
            "It does not recommend a medicine or dosage. "
            "Consult a qualified doctor or pharmacist."
        )

    medicines = {

        "Paracetamol": {
            "use": (
                "Generally used for fever and mild to moderate pain."
            ),
            "caution": (
                "Liver disease or other medicines containing "
                "paracetamol require medical advice."
            )
        },

        "Cetirizine": {
            "use": (
                "An antihistamine commonly used for allergy symptoms."
            ),
            "caution": (
                "It may cause sleepiness. Avoid driving if you feel drowsy."
            )
        },

        "ORS": {
            "use": (
                "Helps replace fluids and salts lost during dehydration."
            ),
            "caution": (
                "Prepare it according to the packet instructions."
            )
        },

        "Antacid": {
            "use": (
                "Used for temporary relief from acidity and heartburn."
            ),
            "caution": (
                "Persistent symptoms need medical evaluation."
            )
        }
    }

    with basics_tab:

        selected = st.selectbox(
            "Select Medicine",
            list(medicines.keys())
        )

        if st.button("Get Medicine Information"):

            details = medicines[selected]

            st.subheader(selected)

            st.success("General Use: " + details["use"])

            st.warning("Precaution: " + details["caution"])

            st.info(
                "This module provides general educational information. "
                "It does not recommend a medicine or dosage. "
                "Consult a qualified doctor or pharmacist."
            )


# ==================================
# FIRST AID
# ==================================

elif menu == "First Aid":

    st.title("🚑 First Aid Information")

    first_aid = {

        "Minor Burns": (
            "Cool the burn under cool running water for 20 minutes. "
            "Do not apply ice or toothpaste. "
            "Seek medical help for serious burns."
        ),

        "Minor Cuts": (
            "Apply gentle pressure with clean gauze or cloth. "
            "Once bleeding stops, rinse the wound with clean water "
            "and cover it with a sterile dressing."
        ),

        "Nose Bleeding": (
            "Sit upright, lean forward and pinch the soft part of "
            "your nose continuously for 10–15 minutes. "
            "Seek medical help if bleeding is severe or does not stop."
        ),

        "Choking": (
            "If a person cannot breathe, speak or cough, "
            "call emergency services (112 in India) and get immediate help. "
            "Use age-appropriate choking first aid."
        )
    }

    selected_aid = st.selectbox(
        "Select First Aid Topic",
        list(first_aid.keys())
    )

    if st.button("Show First Aid Steps"):

        st.subheader(selected_aid)

        st.write(first_aid[selected_aid])

    st.error(
        "For serious injuries or emergencies, call 112 in India "
        "and seek immediate medical help."
    )


# ==================================
# CHATBOT
# ==================================

elif menu == "Chatbot":

    st.title("🤖 GoviCare AI")

    st.caption("Your Smart Health Information Companion")

    if gemini_bot.is_configured():
        st.success(
            f"🟢 AI mode: Google Gemini ({gemini_bot.model_name()}) with "
            "Indian medicine search and FDA drug safety lookup. "
            "Ask in English, Hindi or Hinglish."
        )
    else:
        st.info(
            "🟡 Basic mode: add GEMINI_API_KEY to a .env file to enable "
            "the AI assistant. You can still ask about common symptoms "
            "or medicine prices, e.g. *dolo 650 ki kimat*."
        )

    st.warning(
        "Disclaimer: This chatbot provides general health information "
        "only. It cannot diagnose diseases or replace a doctor."
    )

    # INITIALIZE CHAT HISTORY
    if "messages" not in st.session_state:

        st.session_state.messages = []

        history = get_chat_history()

        for chat in reversed(history):

            st.session_state.messages.append({
                "role": "user",
                "content": chat[1]
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": chat[2]
            })

    # CLEAR CHAT
    if st.button("🗑️ Clear Chat"):

        clear_chat_history()

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # DISPLAY MESSAGES
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # USER INPUT
    user_input = st.chat_input(
        "Type your health question here..."
    )

    if user_input:

        with st.spinner("Thinking..."):
            response, _source = get_bot_response(
                user_input, st.session_state.messages
            )

        save_chat(user_input, response)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    st.caption(
        "Educational information only. "
        "Consult a qualified healthcare professional for medical advice."
    )
# ==================================
# HEALTH INFORMATION
# ==================================

elif menu == "Health Information":

    st.title("📚 Health Information")

    st.write(
        "Learn basic information about common health topics."
    )

    topics = {

        "Fever": (
            "Fever is a temporary rise in body temperature. "
            "It can occur due to infections and other conditions. "
            "Rest, fluids and medical advice may help."
        ),

        "Diabetes": (
            "Diabetes is a condition that affects how the body "
            "regulates blood glucose. Regular monitoring and "
            "medical care are important."
        ),

        "Blood Pressure": (
            "Blood pressure measures the force of blood against "
            "artery walls. Regular monitoring helps identify "
            "high or low blood pressure."
        ),

        "Heart Health": (
            "A healthy lifestyle, balanced diet, physical activity "
            "and regular medical checkups support heart health."
        ),

        "Mental Health": (
            "Mental health includes emotional, psychological "
            "and social well-being. Seek professional support "
            "when you are struggling."
        ),

        "Dehydration": (
            "Dehydration occurs when the body loses more fluids "
            "than it takes in. Drinking fluids and using ORS "
            "when appropriate can help."
        )
    }

    selected_topic = st.selectbox(
        "Select a Health Topic",
        list(topics.keys())
    )

    if st.button("Learn More"):

        st.subheader(selected_topic)

        st.info(topics[selected_topic])

    st.warning(
        "This information is for educational purposes only. "
        "Consult a healthcare professional for medical advice."
    )


# ==================================
# HEALTHCARE TOOLS - 12 TOOLS DASHBOARD
# ==================================

elif menu == "Healthcare Tools":

    from datetime import datetime, timedelta

    st.title("🛠️ Healthcare Tools")
    st.write("Your personal health and wellness dashboard.")

    st.warning(
        "These tools provide educational estimates and record keeping only. "
        "They do not diagnose or treat medical conditions."
    )

    # Initialize session data
    if "selected_health_tool" not in st.session_state:
        st.session_state.selected_health_tool = None

    tool_records = [
        "medicine_list",
        "health_records",
        "bp_records",
        "heart_records",
        "sleep_records",
        "step_records",
        "nutrition_records",
        "stress_records"
    ]

    for record_key in tool_records:
        if record_key not in st.session_state:
            st.session_state[record_key] = []

    # Tool information
    tools_list = [
        ("⚖️", "BMI Calculator", "Calculate Body Mass Index"),
        ("💧", "Water Intake", "Estimate daily fluid needs"),
        ("🔥", "Calorie Calculator", "Estimate daily calories"),
        ("⚡", "BMR Calculator", "Calculate resting energy"),
        ("💊", "Medicine Reminder", "Plan medicine timings"),
        ("❤️", "Health Tracker", "Track daily health records"),
        ("🩸", "Blood Pressure Tracker", "Record BP readings"),
        ("🫀", "Heart Rate Tracker", "Record pulse readings"),
        ("😴", "Sleep Calculator", "Track sleep duration"),
        ("👣", "Step & Activity Tracker", "Track daily steps"),
        ("🥗", "Nutrition Calculator", "Calculate food macros"),
        ("🧘", "Stress & Wellness Tracker", "Track mood and wellness")
    ]

    selected_tool = st.session_state.selected_health_tool

    # ==================================
    # DASHBOARD - 12 TOOL CARDS
    # ==================================

    if selected_tool is None:

        st.subheader("Explore Healthcare Tools")

        for i in range(0, len(tools_list), 3):

            cols = st.columns(3)

            for j, col in enumerate(cols):

                index = i + j

                if index < len(tools_list):

                    icon, name, description = tools_list[index]

                    with col:

                        with st.container(border=True):

                            st.markdown(
                                f"<h1 style='text-align:center'>{icon}</h1>",
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f"<h4 style='text-align:center'>{name}</h4>",
                                unsafe_allow_html=True
                            )

                            st.caption(description)

                            if st.button(
                                "Open Tool",
                                key=f"open_tool_{index}",
                                use_container_width=True
                            ):

                                st.session_state.selected_health_tool = name
                                st.rerun()

    # ==================================
    # INDIVIDUAL TOOL PAGE
    # ==================================

    else:

        if st.button("⬅️ Back to Healthcare Tools"):

            st.session_state.selected_health_tool = None
            st.rerun()

        st.divider()

        st.header(selected_tool)

        # ==================================
        # 1. BMI CALCULATOR
        # ==================================

        if selected_tool == "BMI Calculator":

            weight = st.number_input(
                "Weight (kg)", 1.0, 300.0, 60.0,
                key="tool_bmi_weight"
            )

            height = st.number_input(
                "Height (cm)", 50.0, 250.0, 170.0,
                key="tool_bmi_height"
            )

            if st.button("Calculate BMI"):

                bmi = weight / ((height / 100) ** 2)

                st.metric("Your BMI", f"{bmi:.2f}")

                if bmi < 18.5:
                    st.info("Adult BMI category: Underweight")
                elif bmi < 25:
                    st.success("Adult BMI category: Healthy weight range")
                elif bmi < 30:
                    st.warning("Adult BMI category: Overweight")
                else:
                    st.error("Adult BMI category: Obesity range")

            st.caption("BMI is a screening measure, not a diagnosis.")

        # ==================================
        # 2. WATER INTAKE
        # ==================================

        elif selected_tool == "Water Intake":

            weight = st.number_input(
                "Your Weight (kg)", 1.0, 300.0, 60.0,
                key="tool_water_weight"
            )

            activity = st.selectbox(
                "Activity Level",
                ["Low", "Moderate", "High"]
            )

            if st.button("Calculate Water Intake"):

                water = weight * 0.033

                if activity == "Moderate":
                    water += 0.3
                elif activity == "High":
                    water += 0.6

                st.success(
                    f"Estimated daily fluid guide: {water:.1f} litres"
                )

            st.caption(
                "Fluid requirements vary with climate, activity and health. "
                "This estimate is not suitable for everyone."
            )

        # ==================================
        # 3. CALORIE CALCULATOR
        # ==================================

        elif selected_tool == "Calorie Calculator":

            age = st.number_input(
                "Age", 18, 100, 24, key="tool_cal_age"
            )

            gender = st.selectbox(
                "Formula Setting",
                ["Male", "Female"],
                key="tool_cal_gender"
            )

            weight = st.number_input(
                "Weight (kg)", 20.0, 300.0, 60.0,
                key="tool_cal_weight"
            )

            height = st.number_input(
                "Height (cm)", 100.0, 250.0, 170.0,
                key="tool_cal_height"
            )

            activity = st.selectbox(
                "Activity Level",
                [
                    "Sedentary",
                    "Light",
                    "Moderate",
                    "Active",
                    "Very Active"
                ],
                key="tool_cal_activity"
            )

            if st.button("Calculate Calories"):

                if gender == "Male":
                    bmr = 10 * weight + 6.25 * height - 5 * age + 5
                else:
                    bmr = 10 * weight + 6.25 * height - 5 * age - 161

                factors = {
                    "Sedentary": 1.2,
                    "Light": 1.375,
                    "Moderate": 1.55,
                    "Active": 1.725,
                    "Very Active": 1.9
                }

                calories = bmr * factors[activity]

                st.metric(
                    "Estimated Maintenance Calories",
                    f"{calories:.0f} kcal/day"
                )

            st.caption("This is an estimate, not a diet prescription.")

        # ==================================
        # 4. BMR CALCULATOR
        # ==================================

        elif selected_tool == "BMR Calculator":

            age = st.number_input(
                "Age", 18, 100, 24, key="tool_bmr_age"
            )

            gender = st.selectbox(
                "Formula Setting",
                ["Male", "Female"],
                key="tool_bmr_gender"
            )

            weight = st.number_input(
                "Weight (kg)", 20.0, 300.0, 60.0,
                key="tool_bmr_weight"
            )

            height = st.number_input(
                "Height (cm)", 100.0, 250.0, 170.0,
                key="tool_bmr_height"
            )

            if st.button("Calculate BMR"):

                if gender == "Male":
                    bmr = 10 * weight + 6.25 * height - 5 * age + 5
                else:
                    bmr = 10 * weight + 6.25 * height - 5 * age - 161

                st.success(f"Estimated BMR: {bmr:.0f} kcal/day")

            st.caption("BMR estimates energy used by the body at rest.")

        # ==================================
        # 5. MEDICINE REMINDER
        # ==================================

        elif selected_tool == "Medicine Reminder":

            with st.form("tool_medicine_form"):

                medicine = st.text_input("Medicine Name")
                medicine_time = st.time_input("Medicine Time")
                note = st.text_input("Additional Note")

                submit = st.form_submit_button("Add Reminder")

            if submit:

                if medicine.strip():

                    st.session_state.medicine_list.append({
                        "Medicine": medicine,
                        "Time": medicine_time.strftime("%I:%M %p"),
                        "Note": note
                    })

                    st.success("Medicine reminder added!")

                else:
                    st.error("Enter medicine name.")

            st.subheader("Your Medicine Schedule")

            for item in st.session_state.medicine_list:

                st.markdown(
                    f"💊 **{item['Medicine']}** | "
                    f"{item['Time']} | {item['Note']}"
                )

            if st.button("Clear Medicine Reminders"):
                st.session_state.medicine_list = []
                st.rerun()

            st.info(
                "This is a schedule planner only. It does not send "
                "notifications. Follow your prescribed medicine schedule."
            )

        # ==================================
        # 6. HEALTH TRACKER
        # ==================================

        elif selected_tool == "Health Tracker":

            with st.form("tool_health_form"):

                date = st.date_input("Date")
                weight = st.number_input("Weight (kg)", 0.0, 300.0)
                water = st.number_input("Water Consumed (L)", 0.0, 20.0)
                sleep = st.number_input("Sleep Hours", 0.0, 24.0)
                steps = st.number_input("Daily Steps", 0, 100000)
                notes = st.text_area("Health Notes")

                submit = st.form_submit_button("Save Health Record")

            if submit:

                st.session_state.health_records.append({
                    "Date": str(date),
                    "Weight": weight,
                    "Water": water,
                    "Sleep": sleep,
                    "Steps": steps,
                    "Notes": notes
                })

                st.success("Health record saved!")

            st.subheader("Saved Health Records")

            for record in st.session_state.health_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

            if st.button("Clear Health Records"):
                st.session_state.health_records = []
                st.rerun()

        # ==================================
        # 7. BLOOD PRESSURE TRACKER
        # ==================================

        elif selected_tool == "Blood Pressure Tracker":

            with st.form("tool_bp_form"):

                date = st.date_input("Reading Date", key="bp_date")

                systolic = st.number_input(
                    "Systolic (upper)", 50, 250, 120
                )

                diastolic = st.number_input(
                    "Diastolic (lower)", 30, 150, 80
                )

                submit = st.form_submit_button("Save BP Reading")

            if submit:

                st.session_state.bp_records.append({
                    "Date": str(date),
                    "Systolic": systolic,
                    "Diastolic": diastolic
                })

                st.success("BP reading saved!")

            st.subheader("BP History")

            for record in st.session_state.bp_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

            st.caption(
                "A single reading cannot diagnose hypertension. "
                "Discuss repeated unusual readings with a healthcare professional."
            )

        # ==================================
        # 8. HEART RATE TRACKER
        # ==================================

        elif selected_tool == "Heart Rate Tracker":

            with st.form("tool_heart_form"):

                date = st.date_input("Reading Date", key="heart_date")

                pulse = st.number_input(
                    "Heart Rate (beats per minute)",
                    20, 250, 72
                )

                submit = st.form_submit_button("Save Heart Rate")

            if submit:

                st.session_state.heart_records.append({
                    "Date": str(date),
                    "Heart Rate": pulse
                })

                st.success("Heart rate reading saved!")

            st.subheader("Heart Rate History")

            for record in st.session_state.heart_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

            st.caption(
                "Heart rate varies with age, activity and health. "
                "Seek medical advice for concerning symptoms."
            )

        # ==================================
        # 9. SLEEP CALCULATOR
        # ==================================

        elif selected_tool == "Sleep Calculator":

            wake_time = st.time_input(
                "What time do you want to wake up?",
                key="sleep_wake"
            )

            sleep_hours = st.number_input(
                "Desired sleep duration (hours)",
                1.0, 16.0, 8.0, 0.5
            )

            if st.button("Calculate Bedtime"):

                wake_datetime = datetime.combine(
                    datetime.today().date(),
                    wake_time
                )

                bedtime = wake_datetime - timedelta(
                    hours=sleep_hours
                )

                st.success(
                    "Suggested bedtime: "
                    + bedtime.strftime("%I:%M %p")
                )

            st.caption(
                "Most adults generally need at least 7 hours of sleep."
            )

            with st.form("tool_sleep_form"):

                date = st.date_input("Sleep Record Date")

                actual_sleep = st.number_input(
                    "Actual Sleep Hours", 0.0, 24.0, 8.0
                )

                submit = st.form_submit_button("Save Sleep Record")

            if submit:

                st.session_state.sleep_records.append({
                    "Date": str(date),
                    "Sleep Hours": actual_sleep
                })

                st.success("Sleep record saved!")

            for record in st.session_state.sleep_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

        # ==================================
        # 10. STEP & ACTIVITY TRACKER
        # ==================================

        elif selected_tool == "Step & Activity Tracker":

            with st.form("tool_steps_form"):

                date = st.date_input("Activity Date")

                steps = st.number_input(
                    "Number of Steps", 0, 100000, 5000
                )

                activity = st.selectbox(
                    "Activity Type",
                    ["Walking", "Running", "Cycling", "Exercise", "Other"]
                )

                submit = st.form_submit_button("Save Activity")

            if submit:

                st.session_state.step_records.append({
                    "Date": str(date),
                    "Steps": steps,
                    "Activity": activity
                })

                st.success("Activity saved!")

            st.subheader("Activity History")

            for record in st.session_state.step_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

        # ==================================
        # 11. NUTRITION CALCULATOR
        # ==================================

        elif selected_tool == "Nutrition Calculator":

            st.write("Enter the macronutrients in your food.")

            protein = st.number_input(
                "Protein (grams)", 0.0, 1000.0, 50.0
            )

            carbs = st.number_input(
                "Carbohydrates (grams)", 0.0, 1000.0, 100.0
            )

            fat = st.number_input(
                "Fat (grams)", 0.0, 1000.0, 40.0
            )

            if st.button("Calculate Nutrition"):

                protein_cal = protein * 4
                carbs_cal = carbs * 4
                fat_cal = fat * 9

                total = protein_cal + carbs_cal + fat_cal

                st.metric("Estimated Total Calories", f"{total:.0f} kcal")

                col1, col2, col3 = st.columns(3)

                col1.metric("Protein", f"{protein_cal:.0f} kcal")
                col2.metric("Carbs", f"{carbs_cal:.0f} kcal")
                col3.metric("Fat", f"{fat_cal:.0f} kcal")

            st.caption(
                "This is a macronutrient estimate, not a complete "
                "nutritional assessment."
            )

        # ==================================
        # 12. STRESS & WELLNESS TRACKER
        # ==================================

        elif selected_tool == "Stress & Wellness Tracker":

            with st.form("tool_stress_form"):

                date = st.date_input("Date", key="stress_date")

                mood = st.selectbox(
                    "How is your mood today?",
                    ["Very Good", "Good", "Okay", "Low", "Very Low"]
                )

                stress = st.slider(
                    "Stress Level",
                    min_value=0,
                    max_value=10,
                    value=5
                )

                notes = st.text_area("Personal Notes")

                submit = st.form_submit_button("Save Wellness Record")

            if submit:

                st.session_state.stress_records.append({
                    "Date": str(date),
                    "Mood": mood,
                    "Stress Level": stress,
                    "Notes": notes
                })

                st.success("Wellness record saved!")

            st.subheader("Wellness History")

            for record in st.session_state.stress_records:
                for key, value in record.items():
                    st.markdown(f"**{key}:** {value}")
                st.divider()

            st.info(
                "If stress or low mood is affecting daily life, "
                "consider speaking with a mental health professional."
            )

        st.divider()
        st.caption(
            "AI Healthcare Assistant | Healthcare Tools | "
        )
