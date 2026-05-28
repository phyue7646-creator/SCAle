import streamlit as st
import google.generativeai as genai
import json
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# API KEY
# =========================================================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# =========================================================
# GEMINI CONFIG
# =========================================================

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)

# =========================================================
# LOAD SYSTEM PROMPT
# =========================================================

PROMPTS_DIR = Path(__file__).parent / "prompts"

SYSTEM_PROMPT_FILE = PROMPTS_DIR / "system_prompt.md"

with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# =========================================================
# IMAGE
# =========================================================

robot_image = "https://raw.githubusercontent.com/phuye7646-creator/SCAle/main/d06d65c5-67c9-4a99-b853-40525a2c4d2c.png"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
GLOBAL
========================================================= */

#MainMenu,
header,
footer {
    visibility: hidden;
}

.stApp {
    background-color: #F6F6F6;
}

.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    max-width: 100%;
}

/* =========================================================
TOP BAR
========================================================= */

.topbar {
    background: #742774;
    height: 54px;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
}

/* =========================================================
LAYOUT
========================================================= */

.page-wrapper {
    margin-top: 90px;
    padding-left: 17%;
    padding-right: 17%;
}

/* =========================================================
LOGO
========================================================= */

.logo {
    font-size: 48px;
    font-weight: 700;
    color: #4C7A46;
    margin-bottom: 50px;
}

/* =========================================================
WELCOME PAGE
========================================================= */

.hero-title {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 10px;
}

.hero-subtitle {
    text-align: center;
    font-size: 20px;
    color: #666666;
    line-height: 1.7;
    margin-top: 18px;
}

.hero-image {
    display: flex;
    justify-content: center;
    margin-top: 40px;
    margin-bottom: 40px;
}

.hero-image img {
    width: 360px;
}

/* =========================================================
PAGE TITLES
========================================================= */

.page-title {
    font-size: 42px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 40px;
}

.page-subtitle {
    font-size: 20px;
    color: #666666;
    margin-top: 12px;
    margin-bottom: 35px;
}

/* =========================================================
LABELS
========================================================= */

label {
    color: black !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* =========================================================
TEXT AREA
========================================================= */

textarea {
    background: white !important;
    color: black !important;
    border: 1px solid #D3D3D3 !important;
    border-radius: 0px !important;
    font-size: 18px !important;
    min-height: 180px !important;
}

/* =========================================================
SELECTBOX
========================================================= */

div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
    border: 1px solid #D3D3D3 !important;
    border-radius: 0px !important;
    min-height: 50px;
    font-size: 18px !important;
}

div[data-baseweb="select"] * {
    color: black !important;
}

/* =========================================================
NORMAL BUTTONS
========================================================= */

.stButton > button {
    background: #4C7A46;
    color: white;
    border: none;
    border-radius: 12px;
    height: 52px;
    width: 320px;
    font-size: 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #3D6439;
    color: white;
}

/* =========================================================
BACK BUTTON
========================================================= */

.back-btn button {
    background: transparent !important;
    border: none !important;
    color: black !important;
    font-size: 44px !important;
    width: 70px !important;
    height: 70px !important;
    box-shadow: none !important;
}

/* =========================================================
RESULT PAGE
========================================================= */

.result-small {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
}

.result-big {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: #4C7A46;
    margin-bottom: 30px;
}

.result-card {
    background: white;
    border: 1px solid #DADADA;
    border-radius: 18px;
    padding: 50px;
    min-height: 360px;
}

.idea-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 30px;
    color: #1A1A1A;
}

.idea-text {
    font-size: 20px;
    line-height: 2;
    color: #333333;
}

.idea-counter {
    text-align: center;
    margin-top: 25px;
    font-size: 18px;
}

/* =========================================================
ARROW BUTTONS
========================================================= */

.arrow-btn button {
    background: transparent !important;
    border: none !important;
    color: black !important;
    font-size: 42px !important;
    width: 70px !important;
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

DIPLOMAS = [
    "Diploma in Chemical Engineering",
    "Diploma in Big Data & Analytics",
    "Diploma in Information Technology",
    "Diploma in Accountancy & Finance",
    "Diploma in Marketing"
]

CATEGORIES = [
    "Circular Economy",
    "Renewable Energy",
    "Waste Management & Recycling",
    "Green Transportation",
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
    st.session_state.page = "welcome"

if "diploma" not in st.session_state:
    st.session_state.diploma = ""

if "category" not in st.session_state:
    st.session_state.category = ""

if "concern" not in st.session_state:
    st.session_state.concern = ""

if "solution_type" not in st.session_state:
    st.session_state.solution_type = ""

if "ideas" not in st.session_state:
    st.session_state.ideas = []

if "current_idea" not in st.session_state:
    st.session_state.current_idea = 0

# =========================================================
# TOP BAR
# =========================================================

st.markdown(
    "<div class='topbar'></div>",
    unsafe_allow_html=True
)

# =========================================================
# WELCOME PAGE
# =========================================================

if st.session_state.page == "welcome":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='logo'>
        🌱 SCAle
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='hero-title'>
        Hi! I'm SCAle.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='hero-subtitle'>
        I will help you explore sustainability project ideas tailored to your diploma and interests. Let's get started.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='hero-image'>
        <img src="{robot_image}">
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Your Project Ideas"):

            st.session_state.page = "diploma"
            st.rerun()

# =========================================================
# DIPLOMA PAGE
# =========================================================

elif st.session_state.page == "diploma":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='page-title'>
        What is your diploma?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='page-subtitle'>
        This helps me to tailor sustainability project ideas to your field of study.
    </div>
    """, unsafe_allow_html=True)

    diploma = st.selectbox(
        "Select your diploma",
        DIPLOMAS
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Continue →"):

            st.session_state.diploma = diploma
            st.session_state.page = "category"
            st.rerun()

# =========================================================
# CATEGORY PAGE
# =========================================================

elif st.session_state.page == "category":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←"):
        st.session_state.page = "diploma"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='page-title'>
        What sustainability category interests you?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='page-subtitle'>
        This allows sustainability project ideas align to your focus areas.
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Select sustainability category",
        CATEGORIES
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Continue →"):

            st.session_state.category = category
            st.session_state.page = "concern"
            st.rerun()

# =========================================================
# CONCERN PAGE
# =========================================================

elif st.session_state.page == "concern":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←"):
        st.session_state.page = "category"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='page-title'>
        What sustainability problem would you like to solve?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='page-subtitle'>
        Share a problem or challenge you have noticed in school, community, or daily life.
    </div>
    """, unsafe_allow_html=True)

    concern = st.text_area(
        "Sustainability concern",
        max_chars=200
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Continue →"):

            st.session_state.concern = concern
            st.session_state.page = "solution"
            st.rerun()

# =========================================================
# SOLUTION PAGE
# =========================================================

elif st.session_state.page == "solution":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←"):
        st.session_state.page = "concern"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class='page-title'>
        Which solution format are you interested in developing?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='page-subtitle'>
        This helps me to suggest the right type of project for you.
    </div>
    """, unsafe_allow_html=True)

    solution_type = st.selectbox(
        "Select Solution Type",
        SOLUTION_TYPES
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Submit"):

            st.session_state.solution_type = solution_type

            final_prompt = f"""
{SYSTEM_PROMPT}

Diploma:
{st.session_state.diploma}

Sustainability Category:
{st.session_state.category}

Sustainability Concern:
{st.session_state.concern}

Preferred Solution Type:
{st.session_state.solution_type}
"""

            with st.spinner("Generating ideas..."):

                response = model.generate_content(
                    final_prompt
                )

                cleaned = response.text.strip()

                cleaned = cleaned.replace("```json", "")
                cleaned = cleaned.replace("```", "")

                ideas = json.loads(cleaned)

                st.session_state.ideas = ideas
                st.session_state.current_idea = 0
                st.session_state.page = "results"

                st.rerun()

# =========================================================
# RESULTS PAGE
# =========================================================

elif st.session_state.page == "results":

    st.markdown("<div class='page-wrapper'>", unsafe_allow_html=True)

    ideas = st.session_state.ideas

    current = st.session_state.current_idea

    idea = ideas[current]

    st.markdown("""
    <div class='result-small'>
        Here are your
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='result-big'>
        Project Ideas!
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,8,1])

    with col1:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("←"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown(
            f"""
<div class="result-card">

<div class="idea-title">
{idea["title"]}
</div>

<div class="idea-text">
{idea["idea"]}
</div>

<div class="idea-counter">
{current + 1} / {len(ideas)}
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("→"):

            if current < len(ideas) - 1:
                st.session_state.current_idea += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Over"):

            st.session_state.page = "welcome"
            st.session_state.ideas = []
            st.session_state.current_idea = 0

            st.rerun()
