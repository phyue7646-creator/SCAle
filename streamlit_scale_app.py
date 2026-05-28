import streamlit as st
from PIL import Image
import google.generativeai as genai
import re

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

model = genai.GenerativeModel("gemini-1.5-flash")

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
    font-size: 48px;
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
PAGE TITLE
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
QUESTION
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
GREEN BUTTON
========================================================= */

div.stButton > button {
    background-color: #1F6F43 !important;

    color: white !important;

    border: none !important;

    border-radius: 18px !important;

    font-size: 18px !important;

    font-weight: 600 !important;

    height: 58px !important;

    min-width: 260px !important;

    box-shadow: none !important;
}

div.stButton > button:hover {
    background-color: #1F6F43 !important;
    color: white !important;
}

div.stButton > button:active {
    background-color: #1F6F43 !important;
    color: white !important;
}

div.stButton > button:focus {
    background-color: #1F6F43 !important;
    color: white !important;
    border: none !important;
    box-shadow: none !important;
}

/* =========================================================
BACK ARROW
========================================================= */

.back-arrow button {
    background-color: transparent !important;

    color: black !important;

    border: none !important;

    box-shadow: none !important;

    min-width: auto !important;

    width: auto !important;

    height: auto !important;

    padding: 0 !important;

    font-size: 72px !important;

    font-weight: 300 !important;
}

.back-arrow button:hover {
    background-color: transparent !important;
    color: black !important;
}

.back-arrow button:active {
    background-color: transparent !important;
    color: black !important;
}

.back-arrow button:focus {
    background-color: transparent !important;
    color: black !important;
    box-shadow: none !important;
}

.back-arrow p {
    font-size: 72px !important;
    color: black !important;
}

/* =========================================================
SELECT BOX
========================================================= */

div[data-baseweb="select"] > div {
    background-color: white !important;

    border: 1px solid #D9D9D9 !important;

    border-radius: 0px !important;

    min-height: 62px !important;

    box-shadow: none !important;

    display: flex !important;

    align-items: center !important;
}

/* selected value */

div[data-baseweb="select"] span {
    color: black !important;

    font-size: 18px !important;

    text-align: center !important;

    width: 100% !important;
}

/* dropdown popup */

ul {
    background-color: white !important;
}

/* options */

ul li {
    background-color: white !important;

    color: black !important;

    font-size: 18px !important;
}

/* hover */

ul li:hover {
    background-color: #DDEEE3 !important;

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
    background-color: white !important;

    color: black !important;

    font-size: 18px !important;

    border-radius: 0px !important;

    border: 1px solid #D9D9D9 !important;
}

/* =========================================================
IDEA CARD
========================================================= */

.idea-card {
    background-color: white;

    border: 1px solid #E5E7EB;

    border-radius: 22px;

    padding: 50px;

    min-height: 420px;

    position: relative;
}

.idea-text {
    font-size: 22px;

    line-height: 1.9;

    color: black;

    margin-top: 20px;
}

.idea-counter {
    text-align: center;

    font-size: 18px;

    color: #6B7280;

    margin-top: 25px;
}

/* =========================================================
RESULT ARROW
========================================================= */

.arrow-btn button {
    background-color: white !important;

    color: black !important;

    border: none !important;

    box-shadow: none !important;

    min-width: auto !important;

    width: 50px !important;

    height: 50px !important;

    padding: 0 !important;

    font-size: 38px !important;

    border-radius: 50% !important;
}

.arrow-btn button:hover {
    background-color: white !important;
    color: black !important;
}

.arrow-btn button:focus {
    background-color: white !important;
    color: black !important;
    box-shadow: none !important;
}

.arrow-btn button:active {
    background-color: white !important;
    color: black !important;
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

categories = [
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
        """
        <div style="text-align:center;">
            <div class="page-title">
                Hi! I'm SCAle.
            </div>

            <br>

            <div class="page-subtitle">
                I will help you to explore sustainability project ideas tailored to your diploma and interests. Let's get started.
            </div>
        </div>
        """,
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

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back1"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="question-title">What is your diploma?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-subtitle">This helps me to tailor sustainability project ideas to your field of study.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-label">Select your diploma</div>',
        unsafe_allow_html=True
    )

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
Generate EXACTLY 3 sustainability project ideas.

Diploma:
{st.session_state.diploma}

Category:
{st.session_state.category}

Concern:
{st.session_state.concern}

Solution Type:
{st.session_state.solution}

Rules:
- Generate exactly 3 ideas only.
- Each idea must be practical and achievable for diploma students.
- Use simple paragraph format.
- Do not use markdown.
- Do not use bullet points.
- Separate each idea using ###.
"""

            response = model.generate_content(prompt)

            text = response.text.strip()

            ideas = [x.strip() for x in text.split("###") if x.strip()]

            st.session_state.ideas = ideas[:3]

            st.session_state.idea_index = 0

            st.session_state.page = "results"

            st.rerun()

# =========================================================
# RESULTS PAGE
# =========================================================

elif st.session_state.page == "results":

    current = st.session_state.idea_index

    st.markdown(
        """
        <div style="text-align:center;">
            <div style="font-size:22px;font-weight:600;color:black;">
                Here are your
            </div>

            <div class="page-title">
                <span style="color:#14532D;">
                    Project Ideas!
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5,9,0.5])

    with col2:

        idea = st.session_state.ideas[current]

        st.markdown(
            f"""
            <div class="idea-card">

                <div class="idea-text">
                    {idea}
                </div>

                <div class="idea-counter">
                    Idea {current + 1} of {len(st.session_state.ideas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        inner1, inner2, inner3 = st.columns([1,8,1])

        with inner1:

            st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

            if current > 0:
                if st.button("←", key="prev"):
                    st.session_state.idea_index -= 1
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        with inner3:

            st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

            if current < len(st.session_state.ideas) - 1:
                if st.button("→", key="next"):
                    st.session_state.idea_index += 1
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2,1,1.2])

    with c2:
        if st.button("Start Over"):

            st.session_state.page = "welcome"

            st.session_state.idea_index = 0

            st.rerun()
