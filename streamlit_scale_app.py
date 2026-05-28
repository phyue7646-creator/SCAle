import streamlit as st
import json
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    layout="wide"
)

# =========================================================
# GEMINI CONFIG
# =========================================================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================================================
# LOAD SYSTEM PROMPT
# =========================================================

with open("prompts/system_prompt.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

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
    "Green Finance and Impact Investing",
    "Sustainable Food Systems",
    "Sustainable Materials and Packaging",
    "Green Transportation",
    "Sustainable Tourism",
    "Green Economy Opportunities",
    "Waste Management and Recycling",
    "Biodiversity and Conservation"
]

SOLUTION_TYPES = [
    "Digital Prototype",
    "Physical Prototype",
    "Social Campaign"
]

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = 0

if "ideas" not in st.session_state:
    st.session_state.ideas = []

if "current_idea" not in st.session_state:
    st.session_state.current_idea = 0

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

#MainMenu,
header,
footer {
    visibility: hidden;
}

.stApp {
    background-color: #F3F3F3;
}

.block-container {
    padding-top: 0rem;
    max-width: 100%;
}

.topbar {
    background: #742774;
    height: 52px;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
}

.page-wrapper {
    margin-top: 110px;
    padding-left: 17%;
    padding-right: 17%;
}

.logo {
    font-size: 52px;
    font-weight: 700;
    color: #4C7A46;
}

.hero-title {
    text-align: center;
    font-size: 56px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 20px;
}

.hero-subtitle {
    text-align: center;
    font-size: 21px;
    color: #666666;
    line-height: 1.8;
    margin-top: 20px;
}

.hero-image {
    display: flex;
    justify-content: center;
    margin-top: 40px;
    margin-bottom: 40px;
}

.hero-image img {
    width: 350px;
}

.page-title {
    font-size: 44px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 30px;
}

.page-subtitle {
    font-size: 20px;
    color: #666666;
    margin-top: 12px;
    margin-bottom: 35px;
}

label {
    color: black !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

.stTextArea textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #BDBDBD !important;
    border-radius: 4px !important;
    font-size: 18px !important;
    min-height: 220px !important;
    padding: 18px !important;

    -webkit-text-fill-color: black !important;
    caret-color: black !important;
}

.stTextArea textarea:focus {
    border: 1px solid #BDBDBD !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
    border: 1px solid #BDBDBD !important;
    border-radius: 4px !important;
    min-height: 56px;
    font-size: 18px !important;
}

div[data-baseweb="select"] * {
    color: black !important;
}

.stButton > button {
    background: #4C7A46;
    color: white;
    border: none;
    border-radius: 12px;
    height: 56px;
    width: 320px;
    font-size: 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #3D6439;
    color: white;
}

.back-btn button {
    background: transparent !important;
    border: none !important;
    color: black !important;
    font-size: 56px !important;
    width: 80px !important;
    height: 80px !important;
    box-shadow: none !important;
}

.back-btn button:hover {
    background: transparent !important;
    color: black !important;
}

.result-small {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #222222;
}

.result-big {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: #4C7A46;
    margin-bottom: 25px;
}

.result-card {
    background: white;
    border: 1px solid #DDDDDD;
    border-radius: 18px;
    padding: 40px 55px;
    min-height: 430px;
    box-shadow: 0px 1px 4px rgba(0,0,0,0.06);
}

.idea-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 28px;
    color: #1A1A1A;
}

.idea-text {
    font-size: 20px;
    line-height: 2;
    color: #333333;
}

.idea-counter {
    text-align: center;
    margin-top: 28px;
    font-size: 18px;
}

.arrow-btn button {
    background: transparent !important;
    border: none !important;
    color: #4C7A46 !important;
    font-size: 62px !important;
    width: 70px !important;
    height: 70px !important;
    box-shadow: none !important;
}

.arrow-btn button:hover {
    background: transparent !important;
    color: #4C7A46 !important;
}

@media (max-width: 768px) {

.page-wrapper {
    padding-left: 7%;
    padding-right: 7%;
}

.hero-title {
    font-size: 40px;
}

.page-title {
    font-size: 34px;
}

.result-big {
    font-size: 40px;
}

.hero-image img {
    width: 250px;
}

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TOP BAR
# =========================================================

st.markdown('<div class="topbar"></div>', unsafe_allow_html=True)

# =========================================================
# FUNCTIONS
# =========================================================

def next_page():
    st.session_state.page += 1

def previous_page():
    st.session_state.page -= 1

def generate_ideas(diploma, category, concern, solution_type):

    user_prompt = f"""
Diploma: {diploma}

Sustainability Category: {category}

Sustainability Concern:
{concern}

Preferred Solution Type:
{solution_type}
"""

    final_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    response = model.generate_content(final_prompt)

    text = response.text

    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)

# =========================================================
# PAGE WRAPPER
# =========================================================

st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    st.markdown('<div class="logo">SCAle</div>', unsafe_allow_html=True)

    st.markdown(
        "<div class='hero-title'>Hi! I'm SCAle.</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='hero-subtitle'>I will help you explore sustainability project ideas tailored to your diploma and interests. Let's get started.</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="hero-image">
            <img src="https://raw.githubusercontent.com/phyu7646-creator/SCAle/main/assets/robot.png">
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Your Project Ideas"):
            next_page()
            st.rerun()
