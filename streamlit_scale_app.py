# streamlit_scale_app.py

import json
from pathlib import Path

import streamlit as st
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# API KEY
# =========================================================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# =========================================================
# GEMINI CONFIG
# =========================================================

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")

# =========================================================
# LOAD SYSTEM PROMPT
# =========================================================

PROMPTS_DIR = Path(__file__).parent / "prompts"

SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.md"

with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background-color: #f5f5f5;
}

/* Hide Streamlit Menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

/* Logo */

.logo-container {
    text-align: center;
    margin-bottom: 20px;
}

.logo-dark {
    color: #2F5E36;
    font-size: 62px;
    font-weight: 800;
}

.logo-light {
    color: #9CCB4A;
    font-size: 62px;
    font-weight: 800;
}

.tagline {
    text-align: center;
    font-size: 22px;
    color: #666666;
    margin-bottom: 40px;
}

/* Hero */

.hero-title {
    text-align: center;
    font-size: 56px;
    font-weight: 700;
    color: #1F1F1F;
    margin-top: 10px;
}

.hero-subtitle {
    text-align: center;
    font-size: 24px;
    color: #666666;
    margin-top: 20px;
    margin-bottom: 50px;
    line-height: 1.7;
}

/* Form Card */

.form-card {
    background: white;
    padding: 45px;
    border-radius: 24px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-top: 30px;
}

/* Inputs */

div[data-baseweb="select"] > div {
    border-radius: 14px;
    border: 2px solid #D9D9D9;
    min-height: 58px;
}

textarea {
    border-radius: 14px !important;
    border: 2px solid #D9D9D9 !important;
    font-size: 18px !important;
}

/* Buttons */

.stButton > button {
    background-color: #46784D;
    color: white;
    border-radius: 14px;
    height: 60px;
    width: 280px;
    border: none;
    font-size: 22px;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #355E38;
    color: white;
}

/* Results */

.result-title {
    text-align: center;
    font-size: 48px;
    font-weight: 700;
    color: #2F5E36;
    margin-top: 30px;
    margin-bottom: 35px;
}

.idea-card {
    background: white;
    padding: 35px;
    border-radius: 22px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    border-left: 8px solid #46784D;
}

.idea-title {
    font-size: 30px;
    font-weight: 700;
    color: #2F5E36;
    margin-bottom: 16px;
}

.idea-text {
    font-size: 20px;
    line-height: 1.9;
    color: #333333;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# DATA
# =========================================================

DIPLOMAS = [
    "Diploma in Chemical Engineering",
    "Diploma in Food, Nutrition & Culinary Science",
    "Diploma in Medical Biotechnology",
    "Diploma in Pharmaceutical Science",
    "Diploma in Veterinary Technology",
    "Diploma in Communication Design",
    "Diploma in Digital Film & Television",
    "Diploma in Interior Architecture & Design",
    "Diploma in Fashion Management & Design",
    "Diploma in Product Experience & Design",
    "Diploma in Aerospace Electronics",
    "Diploma in Aerospace Engineering",
    "Diploma in Aviation Management",
    "Diploma in Computer Engineering",
    "Diploma in Architectural Technology and Building Services",
    "Diploma in Electrical and Electronics Engineering",
    "Diploma in Business Process and System Engineering",
    "Diploma in Integrated Facility Management",
    "Diploma in Mechatronics",
    "Diploma in Big Data & Analytics",
    "Diploma in Cybersecurity & Digital Forensics",
    "Diploma in Information Technology",
    "Diploma in Applied Artificial Intelligence",
    "Diploma in Immersive Media and Game Development",
    "Diploma in Accountancy & Finance",
    "Diploma in Business",
    "Diploma in Communications & Media Management",
    "Diploma in Culinary Arts & Management",
    "Diploma in Hospitality & Tourism Management",
    "Diploma in International Trade & Logistics",
    "Diploma in Law & Management",
    "Diploma in Marketing",
    "Diploma in Early Childhood Development & Education",
    "Diploma in Psychology Studies",
    "Diploma in Social Science in Gerontology"
]

CATEGORIES = [
    "Circular Economy",
    "Liveable City and Community",
    "Green Buildings",
    "Renewable Energy",
    "Green Finance and Impact Investment",
    "Sustainable Food System / Food Security",
    "Sustainable Materials / Packaging",
    "Green Transportation",
    "Sustainable / Regenerative Tourism",
    "Green Economy Opportunities",
    "Waste Management & Recycling",
    "Biodiversity and Conservation"
]

SOLUTION_TYPES = [
    "Digital Prototype",
    "Physical Prototype",
    "Social Campaign"
]

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class='logo-container'>
        <span class='logo-dark'>SCA</span>
        <span class='logo-light'>le</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='tagline'>
        Suggests scaling sustainability impact and innovation
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class='hero-title'>
        Generate Sustainability Project Ideas
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='hero-subtitle'>
        Explore personalized sustainability project ideas tailored to your diploma, sustainability interests, and preferred project format.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FORM CARD
# =========================================================

st.markdown("<div class='form-card'>", unsafe_allow_html=True)

with st.form("project_form"):

    diploma = st.selectbox(
        "Select your diploma",
        DIPLOMAS
    )

    category = st.selectbox(
        "Sustainability Category",
        CATEGORIES
    )

    concern = st.text_area(
        "What sustainability problem would you like to solve?",
        height=180,
        max_chars=300,
        placeholder="Example: Excessive food waste in hawker centres"
    )

    solution_type = st.selectbox(
        "Preferred Solution Type",
        SOLUTION_TYPES
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        submitted = st.form_submit_button(
            "✨ Generate Ideas"
        )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# GENERATE
# =========================================================

if submitted:

    final_prompt = f"""
{SYSTEM_PROMPT}

Student Inputs:
Diploma: {diploma}
Sustainability Category: {category}
Sustainability Concern: {concern}
Preferred Solution Type: {solution_type}
"""

    with st.spinner("Generating sustainability project ideas..."):

        try:

            response = model.generate_content(final_prompt)

            response_text = response.text.strip()

            response_text = response_text.replace("```json", "")
            response_text = response_text.replace("```", "")

            ideas = json.loads(response_text)

            st.markdown(
                """
                <div class='result-title'>
                    💡 Your Project Ideas
                </div>
                """,
                unsafe_allow_html=True
            )

            for idea in ideas:

                st.markdown(
                    f"""
                    <div class='idea-card'>

                        <div class='idea-title'>
                            {idea['title']}
                        </div>

                        <div class='idea-text'>
                            {idea['idea']}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:

            st.error(
                f"Error generating ideas: {e}"
            )

# =========================================================
# FOOTER
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "These AI-generated sustainability ideas are intended as starting points for diploma student exploration and development."
)
