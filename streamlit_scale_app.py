import streamlit as st
import json
import os
from openai import OpenAI

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    layout="wide"
)

# =========================================================
# OPENAI CLIENT
# =========================================================

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

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
# SESSION STATES
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

/* =========================================================
HIDE STREAMLIT
========================================================= */

#MainMenu,
header,
footer {
    visibility: hidden;
}

/* =========================================================
APP
========================================================= */

.stApp {
    background-color: #F3F3F3;
}

.block-container {
    padding-top: 0rem;
    max-width: 100%;
}

/* =========================================================
TOP BAR
========================================================= */

.topbar {
    background: #742774;
    height: 52px;
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
    margin-top: 110px;
    padding-left: 17%;
    padding-right: 17%;
}

/* =========================================================
WELCOME
========================================================= */

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

/* =========================================================
PAGE TITLES
========================================================= */

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

/* =========================================================
INPUT LABELS
========================================================= */

label {
    color: black !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* =========================================================
TEXT AREA
========================================================= */

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

/* =========================================================
SELECT BOX
========================================================= */

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

/* =========================================================
BUTTONS
========================================================= */

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

/* =========================================================
BACK BUTTON
========================================================= */

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

/* =========================================================
RESULT
========================================================= */

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

/* =========================================================
RESULT ARROWS
========================================================= */

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

/* =========================================================
MOBILE
========================================================= */

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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=1,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    text = response.choices[0].message.content

    return json.loads(text)

# =========================================================
# PAGE WRAPPER
# =========================================================

st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# =========================================================
# PAGE 0 - WELCOME
# =========================================================

if st.session_state.page == 0:

    st.markdown('<div class="logo">SCAle</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="hero-title">Hi! I\\'m SCAle.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">I will help you explore sustainability project ideas tailored to your diploma and interests. Let\\'s get started.</div>',
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

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Your Project Ideas"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 1
# =========================================================

elif st.session_state.page == 1:

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←", key="back1"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What is your diploma?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">This helps me to tailor sustainability project ideas to your field of study.</div>',
        unsafe_allow_html=True
    )

    diploma = st.selectbox(
        "Select your diploma",
        DIPLOMAS
    )

    st.session_state.diploma = diploma

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 2
# =========================================================

elif st.session_state.page == 2:

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←", key="back2"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What sustainability category interests you?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">This allows sustainability project ideas align to your focus areas.</div>',
        unsafe_allow_html=True
    )

    category = st.selectbox(
        "Select sustainability category",
        CATEGORIES
    )

    st.session_state.category = category

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 3
# =========================================================

elif st.session_state.page == 3:

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←", key="back3"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What sustainability problem would you like to solve?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Share a problem or challenge you have noticed in school, community, or daily life.</div>',
        unsafe_allow_html=True
    )

    concern = st.text_area(
        "Sustainability concern",
        height=250,
        max_chars=200,
        key="concern_box"
    )

    st.session_state.concern = concern

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):

            if concern.strip() == "":
                st.warning("Please enter your sustainability concern.")
            else:
                next_page()
                st.rerun()

# =========================================================
# PAGE 4
# =========================================================

elif st.session_state.page == 4:

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)

    if st.button("←", key="back4"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">Which solution format are you interested in developing?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">This helps me to suggest the right type of project for you.</div>',
        unsafe_allow_html=True
    )

    solution_type = st.selectbox(
        "Select Solution Type",
        SOLUTION_TYPES
    )

    st.session_state.solution_type = solution_type

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Submit"):

            with st.spinner("Generating sustainability ideas..."):

                ideas = generate_ideas(
                    st.session_state.diploma,
                    st.session_state.category,
                    st.session_state.concern,
                    solution_type
                )

                st.session_state.ideas = ideas
                st.session_state.current_idea = 0

            next_page()
            st.rerun()

# =========================================================
# PAGE 5 - RESULT
# =========================================================

elif st.session_state.page == 5:

    ideas = st.session_state.ideas
    current = st.session_state.current_idea

    idea = ideas[current]

    st.markdown(
        '<div class="result-small">Here are your</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-big">Project Ideas!</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,10,1])

    # LEFT
    with col1:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("◀", key="left_arrow"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # CARD
    with col2:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="idea-title">
                    {idea['title']}
                </div>

                <div class="idea-text">
                    {idea['idea']}
                </div>

                <div class="idea-counter">
                    {current + 1} / {len(ideas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # RIGHT
    with col3:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("▶", key="right_arrow"):

            if current < len(ideas) - 1:
                st.session_state.current_idea += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Over"):

            st.session_state.page = 0
            st.session_state.current_idea = 0
            st.session_state.ideas = []

            st.rerun()

# =========================================================
# END WRAPPER
# =========================================================

st.markdown('</div>', unsafe_allow_html=True)
