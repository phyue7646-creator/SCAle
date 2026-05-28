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

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

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
    background-color: #F5F5F5;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 100%;
}

/* =========================================================
LAYOUT
========================================================= */

.page-wrapper {
    padding-left: 16%;
    padding-right: 16%;
    padding-top: 20px;
    padding-bottom: 60px;
}

/* =========================================================
SCALE LOGO
========================================================= */

.scale-logo {
    font-size: 52px;
    font-weight: 800;
    margin-bottom: 25px;
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
    margin-top: 30px;
}

.hero-subtitle {
    text-align: center;
    font-size: 22px;
    line-height: 1.8;
    color: #666666;
    margin-top: 18px;
}

.hero-image {
    display: flex;
    justify-content: center;
    margin-top: 45px;
    margin-bottom: 45px;
}

.hero-image img {
    width: 320px;
}

/* =========================================================
PAGE TITLES
========================================================= */

.page-title {
    font-size: 48px;
    font-weight: 700;
    color: #1A1A1A;
    margin-top: 10px;
}

.page-subtitle {
    font-size: 20px;
    color: #666666;
    margin-top: 10px;
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
SELECTBOX
========================================================= */

div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 8px !important;
    min-height: 58px !important;
    color: black !important;
}

div[data-baseweb="select"] * {
    color: black !important;
}

/* =========================================================
TEXT AREA
========================================================= */

.stTextArea textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 8px !important;
    font-size: 18px !important;
    min-height: 240px !important;
    padding: 16px !important;

    -webkit-text-fill-color: black !important;
    caret-color: black !important;
}

.stTextArea textarea:focus {
    border: 1px solid #14532D !important;
    box-shadow: none !important;
    outline: none !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {
    background: #14532D !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    height: 56px !important;
    width: 320px !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #0F3F22 !important;
    color: white !important;
}

/* =========================================================
BACK BUTTON
========================================================= */

.back-btn button {
    background: transparent !important;
    color: black !important;
    border: none !important;
    box-shadow: none !important;
    width: 70px !important;
    height: 70px !important;
    font-size: 50px !important;
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
    font-weight: 800;
    margin-bottom: 30px;
}

.result-card {
    background: white;
    border: 1px solid #DDDDDD;
    border-radius: 22px;
    padding: 45px 55px;
    min-height: 430px;
}

.idea-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 30px;
    color: #1A1A1A;
}

.idea-text {
    font-size: 21px;
    line-height: 2;
    color: #333333;
}

.idea-counter {
    text-align: center;
    margin-top: 30px;
    font-size: 18px;
    color: #666666;
}

/* =========================================================
ARROWS
========================================================= */

.arrow-btn button {
    background: transparent !important;
    border: none !important;
    color: #14532D !important;
    box-shadow: none !important;
    font-size: 55px !important;
    width: 60px !important;
    height: 60px !important;
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
    font-size: 42px;
}

.page-title {
    font-size: 34px;
}

.result-big {
    font-size: 42px;
}

.hero-image img {
    width: 220px;
}

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCTIONS
# =========================================================

def scale_logo():
    st.markdown(
        """
        <div class="scale-logo">
            <span class="scale-sca">SCA</span><span class="scale-le">le</span>
        </div>
        """,
        unsafe_allow_html=True
    )

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

Return ONLY valid JSON.

Format:
[
  {{
    "title": "Project Title",
    "idea": "Project description"
  }}
]

Generate exactly 3 ideas.
"""

    final_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    response = model.generate_content(final_prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:

        ideas = json.loads(text)

        if isinstance(ideas, dict):
            ideas = [ideas]

        return ideas

    except Exception:

        return [
            {
                "title": "Error Generating Ideas",
                "idea": "Gemini returned invalid JSON format."
            }
        ]

# =========================================================
# WRAPPER
# =========================================================

st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    scale_logo()

    st.markdown(
        "<div class='hero-title'>Hi! I'm SCAle.</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='hero-subtitle'>
        I will help you explore sustainability project ideas
        tailored to your diploma and interests.
        Let's get started.
        </div>
        """,
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

# =========================================================
# PAGE 1
# =========================================================

elif st.session_state.page == 1:

    scale_logo()

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
        '<div class="page-subtitle">This helps me tailor ideas to your field of study.</div>',
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

    scale_logo()

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
        '<div class="page-subtitle">Choose the sustainability focus area you care about.</div>',
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

    scale_logo()

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
        '<div class="page-subtitle">Share a problem or challenge you noticed in school, community, or daily life.</div>',
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

    scale_logo()

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
        '<div class="page-subtitle">Choose your preferred project format.</div>',
        unsafe_allow_html=True
    )

    solution_type = st.selectbox(
        "Select solution type",
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
# PAGE 5
# =========================================================

elif st.session_state.page == 5:

    ideas = st.session_state.ideas
    current = st.session_state.current_idea

    idea = ideas[current]

    scale_logo()

    st.markdown(
        '<div class="result-small">Here are your</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="result-big">
            <span class="scale-sca">Project</span>
            <span class="scale-le">Ideas!</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,10,1])

    with col1:

        st.markdown('<div class="arrow-btn">', unsafe_allow_html=True)

        if st.button("◀", key="left_arrow"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

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
