import streamlit as st
from PIL import Image
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GEMINI
# =========================================================

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

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

if "solution" not in st.session_state:
    st.session_state.solution = ""

if "ideas" not in st.session_state:
    st.session_state.ideas = []

if "idea_index" not in st.session_state:
    st.session_state.idea_index = 0

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
HIDE STREAMLIT
========================================================= */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

.stApp {
    background-color: #F5F5F5;
}

/* =========================================================
LOGO
========================================================= */

.logo {
    font-size: 46px;
    font-weight: 700;
    margin-top: 10px;
    margin-left: 40px;
}

.logo-sca {
    color: #14532D;
}

.logo-le {
    color: #8BC34A;
}

/* =========================================================
PAGE TITLES
========================================================= */

.page-title {
    font-size: 54px;
    font-weight: 700;
    color: black;
    text-align: center;
    line-height: 1.2;
}

.page-subtitle {
    font-size: 22px;
    color: #6B7280;
    text-align: center;
    margin-top: 10px;
}

/* =========================================================
QUESTION SECTION
========================================================= */

.question-title {
    font-size: 52px;
    font-weight: 700;
    color: black;
    margin-bottom: 15px;
}

.question-subtitle {
    font-size: 22px;
    color: #6B7280;
    margin-bottom: 45px;
}

.question-label {
    font-size: 18px;
    font-weight: 600;
    color: black;
    margin-bottom: 10px;
}

/* =========================================================
GREEN BUTTONS
========================================================= */

div.stButton:not(.back-arrow) > button {
    background-color: #1F6F43 !important;

    color: white !important;

    border: none !important;

    border-radius: 18px !important;

    font-size: 18px !important;

    font-weight: 600 !important;

    padding: 14px 36px !important;

    height: 58px !important;

    min-width: 260px !important;

    box-shadow: none !important;
    transition: none !important; 
}

div.stButton > button:hover {
    background-color: #1F6F43  !important;
    color: white !important;                /* UPDATED */

    border: none !important; 
}

div.stButton > button:active {
    background-color: #1F6F43 !important;
    color: white !important;
    border: none !important;
}

div.stButton > button:focus {

    background-color: #1F6F43 !important;   /* UPDATED */

    color: white !important;                /* UPDATED */

    border: none !important;

    outline: none !important;

    box-shadow: none !important;}
/* =========================================================
BACK ARROW
========================================================= */

.back-arrow div.stButton > button {

    background-color: transparent !important;   /* UPDATED */

    background: transparent !important;         /* UPDATED */

    border: none !important;

    box-shadow: none !important;

    width: auto !important;
    min-width: auto !important;

    height: auto !important;
    min-height: auto !important;

    padding: 0 !important;
    margin: 0 !important;

    color: black !important;

    font-size: 70px !important;

    font-weight: 300 !important;

    border-radius: 0 !important;               /* UPDATED */
}

.back-arrow div.stButton > button:hover {

    background-color: transparent !important;  /* UPDATED */

    background: transparent !important;        /* UPDATED */

    color: black !important;
}

.back-arrow div.stButton > button:active {

    background-color: transparent !important;  /* UPDATED */

    background: transparent !important;        /* UPDATED */

    color: black !important;
}

.back-arrow div.stButton > button:focus {

    background-color: transparent !important;  /* UPDATED */

    background: transparent !important;        /* UPDATED */

    outline: none !important;

    box-shadow: none !important;

    color: black !important;
}

.back-arrow div.stButton > button p {

    font-size: 70px !important;

    color: black !important;

    margin: 0 !important;
}

/* =========================================================
SELECTBOX
========================================================= */

div[data-baseweb="select"] > div {
    background-color: white !important;

    border: 1px solid #D9D9D9 !important;

    border-radius: 0px !important;

    min-height: 58px !important;

    box-shadow: none !important;
}

div[data-baseweb="select"] span {
    color: black !important;
    font-size: 18px !important;
    opacity: 1 !important;
}

/* selected value shown in box */

div[data-baseweb="select"] input {

    color: black !important;          /* UPDATED */

    -webkit-text-fill-color: black !important;   /* UPDATED */

    font-size: 18px !important;       /* UPDATED */

    opacity: 1 !important;            /* UPDATED */
}

div[data-baseweb="select"] div[role="button"] {

    color: black !important;          /* UPDATED */

    opacity: 1 !important;            /* UPDATED */
}

div[data-baseweb="select"] > div:focus-within {

    border: 1px solid #D9D9D9 !important;

    box-shadow: none !important;
}

/* dropdown popup */

ul {
    background-color: white !important;
}

ul li {
    background-color: white !important;
    color: black !important;

    font-size: 18px !important;
}

/* hover */

ul li:hover {
    background-color: #E7F3EC !important;
    color: black !important;
}


/* selected */

[aria-selected="true"] {
    background-color: #1F6F43 !important;
}

[aria-selected="true"] * {
    color: white !important;
}

/* =========================================================
TEXT AREA
========================================================= */

textarea {
    font-size: 18px !important;

    border-radius: 0px !important;

    border: 1px solid #D9D9D9 !important;
}
textarea:focus {

    border: 1px solid #D9D9D9 !important;

    outline: none !important;

    box-shadow: none !important;
}
/* =========================================================
IDEA CARD
========================================================= */

.idea-card {
    background-color: white;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 40px;

    min-height: 420px;
}

.idea-title {
    font-size: 34px;
    font-weight: 700;
    text-align: center;
    color: black;

    margin-bottom: 25px;
}

.idea-text {
    font-size: 20px;
    line-height: 1.9;
    color: black;

    text-align: left;
}

.idea-counter {
    text-align: center;

    margin-top: 20px;

    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

diplomas = [
    "Diploma in Chemical Engineering",
    "Diploma in Food, Nutrition & Culinary Science",
    "Diploma in Medical Biotechnology",
    "Diploma in Pharmaceutical Science",
    "Diploma in Veterinary Technology",
    "Diploma in Communication Design",
    "Diploma in Digital Film & Television",
]

categories = [
    "Circular Economy",
    "Renewable Energy",
    "Waste Management and Recycling",
    "Green Transportation",
    "Sustainable Food Systems"
]

solutions = [
    "Digital Prototype",
    "Physical Prototype",
    "Social Campaign"
]

# =========================================================
# WELCOME PAGE
# =========================================================

if st.session_state.page == "welcome":

    st.markdown(
        '<div class="logo"><span class="logo-sca">SCA</span><span class="logo-le">le</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;"><div class="page-title">Hi! I\'m SCAle.</div><br><div class="page-subtitle">I will help you to explore sustainability project ideas tailored to your diploma and interests. Let\'s get started.</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    image = Image.open("d06d65c5-67c9-4a99-b853-40525a2c4d2c.png")

    c1, c2, c3 = st.columns([1,2,1])

    with c2:
        st.image(image, width=430)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Start Your Project Ideas"):
            st.session_state.page = "diploma"
            st.rerun()

# =========================================================
# DIPLOMA PAGE
# =========================================================

elif st.session_state.page == "diploma":

    with st.container():
        st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

        if st.button("←", key="back1"):
            st.session_state.page = "welcome"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div class="question-title">What is your diploma?</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="question-subtitle">This helps me to tailor sustainability project ideas to your field of study.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="question-label">Select your diploma</div>', unsafe_allow_html=True)

    st.session_state.diploma = st.selectbox(
        "",
        diplomas,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Continue →"):
            st.session_state.page = "category"
            st.rerun()

# =========================================================
# CATEGORY PAGE
# =========================================================

elif st.session_state.page == "category":

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back2"):
        st.session_state.page = "diploma"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="question-title">What sustainability category interests you?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-subtitle">This allows sustainability project ideas align to your focus areas.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-label">Select sustainability category</div>',
        unsafe_allow_html=True
    )

    st.session_state.category = st.selectbox(
        "",
        categories,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Continue →"):
            st.session_state.page = "concern"
            st.rerun()

# =========================================================
# CONCERN PAGE
# =========================================================

elif st.session_state.page == "concern":

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back3"):
        st.session_state.page = "category"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="question-title">What sustainability problem would you like to solve?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-subtitle">Share an problem or challenge you have noticed in school, community, or daily life.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-label">Sustainability concern</div>',
        unsafe_allow_html=True
    )

    st.session_state.concern = st.text_area(
        "",
        height=220,
        max_chars=200,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Continue →"):
            st.session_state.page = "solution"
            st.rerun()

# =========================================================
# SOLUTION PAGE
# =========================================================

elif st.session_state.page == "solution":

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back4"):
        st.session_state.page = "concern"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="question-title">Which solution format are you interested in developing?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-subtitle">This helps me to suggest the right type of project for you.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-label">Select Solution Type</div>',
        unsafe_allow_html=True
    )

    st.session_state.solution = st.selectbox(
        "",
        solutions,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Submit"):

            prompt = f"""
Generate 3 sustainability project ideas.

Diploma: {st.session_state.diploma}

Category: {st.session_state.category}

Concern: {st.session_state.concern}

Solution Type: {st.session_state.solution}

Return only 3 ideas in paragraph style.
"""

            response = model.generate_content(prompt)

            ideas = response.text.split("\n\n")

            st.session_state.ideas = ideas
            st.session_state.idea_index = 0
            st.session_state.page = "results"

            st.rerun()

# =========================================================
# RESULTS PAGE
# =========================================================

elif st.session_state.page == "results":

    current = st.session_state.idea_index

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:22px;font-weight:600;color:black;text-align:center;">Here are your</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-title"><span style="color:#14532D;">Project Ideas!</span></div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,8,1])

    with col1:
        if current > 0:
            if st.button("←", key="prev"):
                st.session_state.idea_index -= 1
                st.rerun()

    with col2:

        idea = st.session_state.ideas[current]

        st.markdown(
            f'''
            <div class="idea-card">
                <div class="idea-text">
                    {idea}
                </div>

                <div class="idea-counter">
                    {current + 1} / {len(st.session_state.ideas)}
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col3:
        if current < len(st.session_state.ideas) - 1:
            if st.button("→", key="next"):
                st.session_state.idea_index += 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Start Over"):

            st.session_state.page = "welcome"
            st.session_state.idea_index = 0

            st.rerun()
