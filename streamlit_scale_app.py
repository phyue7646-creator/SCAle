# =========================================================
# IMPORTS
# =========================================================

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

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are SCAle, an AI sustainability project assistant.

Generate EXACTLY 3 sustainability project ideas.

Requirements:
- Tailored to the diploma
- Aligned to sustainability category
- Match the preferred solution type
- Practical for diploma students
- Innovative but achievable
- Professional and concise
- Around 120-180 words each

IMPORTANT:
Return ONLY valid JSON.
No markdown.
No explanation.

Format:

[
  {
    "title": "Project title",
    "idea": "Project paragraph"
  }
]
"""

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
    padding-top: 1rem;
    max-width: 100%;
}

.page-wrapper {
    padding-left: 15%;
    padding-right: 15%;
    padding-top: 10px;
}

/* =========================================================
LOGO
========================================================= */

.scale-logo {
    font-size: 52px;
    font-weight: 800;
}

.scale-sca {
    color: #14532D;
}

.scale-le {
    color: #8BC34A;
}

/* =========================================================
WELCOME
========================================================= */

.hero-title {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 20px;
}

.hero-subtitle {
    text-align: center;
    font-size: 21px;
    line-height: 1.8;
    color: #666666;
    margin-top: 20px;
}

.hero-image {
    display: flex;
    justify-content: center;
    margin-top: 35px;
    margin-bottom: 20px;
}

.hero-image img {
    width: 220px;
}

/* =========================================================
PAGE TITLES
========================================================= */

.page-title {
    font-size: 46px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 10px;
}

.page-subtitle {
    font-size: 20px;
    color: #666666;
    margin-top: 12px;
    margin-bottom: 35px;
    line-height: 1.8;
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

.stTextArea textarea {
    background-color: rgba(255,255,255,1) !important;
    color: black !important;
    border: 1px solid #D6D6D6 !important;
    border-radius: 10px !important;
    font-size: 18px !important;
    min-height: 240px !important;
    padding: 18px !important;

    -webkit-text-fill-color: black !important;
    caret-color: black !important;
}

.stTextArea textarea:focus {
    border: 1px solid #14532D !important;
    box-shadow: none !important;
}

/* =========================================================
SELECTBOX
========================================================= */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,1) !important;
    border: 1px solid #D6D6D6 !important;
    border-radius: 10px !important;
    min-height: 62px !important;

    display: flex !important;
    align-items: center !important;
}

div[data-baseweb="select"] span {
    color: black !important;
    font-size: 18px !important;
}

div[data-baseweb="select"] input {
    color: black !important;
}

div[role="listbox"] {
    background-color: white !important;
}

div[role="option"] {
    background-color: white !important;
    color: black !important;
}

div[role="option"]:hover {
    background-color: #E7F3EC !important;
    color: black !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {
    background-color: #14532D;
    color: white !important;
    border: none;
    border-radius: 14px;
    height: 58px;
    width: 320px;
    font-size: 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1F6F43 !important;
    color: white !important;
}

.stButton > button:focus {
    color: white !important;
}

/* =========================================================
BACK ARROW
========================================================= */

.back-arrow button {
    background: transparent !important;
    border: none !important;
    color: black !important;
    font-size: 60px !important;

    width: auto !important;
    height: auto !important;

    padding: 0 !important;
    margin: 0 !important;

    box-shadow: none !important;
}

.back-arrow button:hover {
    background: transparent !important;
    color: black !important;
}

/* =========================================================
RESULT PAGE
========================================================= */

.result-small {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #1A1A1A;
}

.result-big {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    margin-bottom: 35px;
}

.result-card {
    background: white;
    border: 1px solid #DDDDDD;
    border-radius: 18px;
    padding: 45px;
    min-height: 460px;
    box-shadow: 0px 1px 5px rgba(0,0,0,0.05);
}

.idea-title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: #1A1A1A;
    margin-bottom: 30px;
}

.idea-text {
    font-size: 21px;
    line-height: 2;
    color: #333333;
    white-space: pre-line;
}

.idea-counter {
    text-align: center;
    margin-top: 35px;
    font-size: 18px;
    color: #1A1A1A;
}

/* =========================================================
SIDE ARROWS
========================================================= */

.arrow-btn button {
    background: transparent !important;
    border: none !important;
    color: #14532D !important;
    font-size: 72px !important;

    width: auto !important;
    height: auto !important;

    padding: 0 !important;

    box-shadow: none !important;
}

.arrow-btn button:hover {
    background: transparent !important;
    color: #14532D !important;
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
    font-size: 36px;
}

.result-big {
    font-size: 42px;
}

.idea-title {
    font-size: 28px;
}

.idea-text {
    font-size: 18px;
}

.hero-image img {
    width: 180px;
}

}

</style>
""", unsafe_allow_html=True)

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

Category: {category}

Concern:
{concern}

Solution Type:
{solution_type}
"""

    response = model.generate_content(
        SYSTEM_PROMPT + "\n\n" + user_prompt
    )

    text = response.text.strip()

    # REMOVE MARKDOWN IF EXISTS
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    ideas = json.loads(text)

    return ideas

# =========================================================
# WRAPPER
# =========================================================

st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    st.markdown("""
    <div class="scale-logo">
        <span class="scale-sca">SCA</span><span class="scale-le">le</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-title">
        Hi! I'm <span class="scale-sca">SCA</span><span class="scale-le">le</span>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-subtitle">
        I will help you explore sustainability project ideas tailored to your diploma and interests.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-image">
        <img src="https://raw.githubusercontent.com/phyu7646-creator/SCAle/main/assets/robot.png">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:
        if st.button("Start Your Project Ideas"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 1
# =========================================================

elif st.session_state.page == 1:

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back1"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What is your diploma?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">This helps me tailor sustainability project ideas to your field of study.</div>',
        unsafe_allow_html=True
    )

    diploma = st.selectbox(
        "Select your diploma",
        DIPLOMAS
    )

    st.session_state.diploma = diploma

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:
        if st.button("Continue →"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 2
# =========================================================

elif st.session_state.page == 2:

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back2"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What sustainability category interests you?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Choose a sustainability category you want to focus on.</div>',
        unsafe_allow_html=True
    )

    category = st.selectbox(
        "Select sustainability category",
        CATEGORIES
    )

    st.session_state.category = category

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:
        if st.button("Continue →"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 3
# =========================================================

elif st.session_state.page == 3:

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back3"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">What sustainability problem would you like to solve?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Share a sustainability challenge you noticed in school, community, or daily life.</div>',
        unsafe_allow_html=True
    )

    concern = st.text_area(
        "Sustainability concern",
        max_chars=200,
        key="concern_box"
    )

    st.session_state.concern = concern

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

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

    st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

    if st.button("←", key="back4"):
        previous_page()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="page-title">Which solution format are you interested in developing?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Choose the type of sustainability solution you want to create.</div>',
        unsafe_allow_html=True
    )

    solution_type = st.selectbox(
        "Select solution type",
        SOLUTION_TYPES
    )

    st.session_state.solution_type = solution_type

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

        if st.button("Generate Ideas"):

            with st.spinner("Generating sustainability ideas..."):

                ideas = generate_ideas(
                    st.session_state.diploma,
                    st.session_state.category,
                    st.session_state.concern,
                    st.session_state.solution_type
                )

                st.session_state.ideas = ideas
                st.session_state.current_idea = 0

            next_page()
            st.rerun()

# =========================================================
# PAGE 5
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
        '<div class="result-big"><span class="scale-sca">Project</span> <span class="scale-le">Ideas!</span></div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1,8,1])

    # LEFT
    with left:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("‹", key="left_arrow"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # CARD
    with center:

        title = idea.get("title", "")
        paragraph = idea.get("idea", "")

        st.markdown(
            f"""
            <div class="result-card">

                <div class="idea-title">
                    {title}
                </div>

                <div class="idea-text">
                    {paragraph}
                </div>

                <div class="idea-counter">
                    {current + 1} / {len(ideas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # RIGHT
    with right:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("›", key="right_arrow"):

            if current < len(ideas) - 1:
                st.session_state.current_idea += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

        if st.button("Start Over"):

            st.session_state.page = 0
            st.session_state.current_idea = 0
            st.session_state.ideas = []

            st.rerun()

# =========================================================
# END WRAPPER
# =========================================================

st.markdown('</div>', unsafe_allow_html=True)
