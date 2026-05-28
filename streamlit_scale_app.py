````python
import streamlit as st
import google.generativeai as genai
import json
import base64
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
# LOAD IMAGE
# =========================================================

def load_base64_image(image_path):

    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

robot_image = load_base64_image(
    "d06d65c5-67c9-4a99-b853-40525a2c4d2c.png"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
<style>

/* =========================================================
GLOBAL
========================================================= */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

.stApp {{
    background-color: #F5F5F5;
}}

.block-container {{
    padding-top: 0rem;
    padding-bottom: 2rem;
    max-width: 100%;
}}

/* =========================================================
TOP BAR
========================================================= */

.topbar {{
    background: #742774;
    height: 58px;
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 999;
}}

/* =========================================================
PAGE WRAPPER
========================================================= */

.page-wrapper {{
    margin-top: 90px;
    padding-left: 8%;
    padding-right: 8%;
}}

/* =========================================================
LOGO
========================================================= */

.logo {{
    font-size: 42px;
    font-weight: 700;
    color: #5F8F42;
    margin-bottom: 40px;
}}

/* =========================================================
WELCOME PAGE
========================================================= */

.hero-title {{
    text-align: center;
    font-size: 60px;
    font-weight: 700;
    color: #1F1F1F;
    margin-top: 20px;
}}

.hero-subtitle {{
    text-align: center;
    font-size: 24px;
    color: #666666;
    margin-top: 18px;
    line-height: 1.7;
}}

.hero-image {{
    display: flex;
    justify-content: center;
    margin-top: 40px;
    margin-bottom: 40px;
}}

.hero-image img {{
    width: 520px;
}}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {{
    background: #46784D;
    color: white;
    border: none;
    border-radius: 14px;
    width: 340px;
    height: 64px;
    font-size: 28px;
    font-weight: 700;
}}

.stButton > button:hover {{
    background: #355E38;
    color: white;
}}

/* =========================================================
FORM PAGES
========================================================= */

.page-title {{
    font-size: 58px;
    font-weight: 700;
    color: #1F1F1F;
    margin-top: 70px;
}}

.page-subtitle {{
    font-size: 24px;
    color: #666666;
    margin-top: 15px;
    margin-bottom: 45px;
}}

label {{
    font-size: 26px !important;
    font-weight: 700 !important;
}}

textarea {{
    border-radius: 0px !important;
    border: 2px solid #D0D0D0 !important;
    min-height: 240px !important;
    font-size: 22px !important;
}}

div[data-baseweb="select"] > div {{
    border-radius: 0px !important;
    min-height: 62px;
    font-size: 22px !important;
}}

/* =========================================================
RESULT PAGE
========================================================= */

.result-header-small {{
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    margin-top: 20px;
}}

.result-header-large {{
    text-align: center;
    font-size: 64px;
    font-weight: 700;
    color: #2F5E36;
}}

.result-card {{
    background: white;
    border: 2px solid #DADADA;
    border-radius: 18px;
    padding: 40px;
    margin-top: 30px;
    min-height: 500px;
}}

.idea-title {{
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 30px;
}}

.idea-text {{
    font-size: 24px;
    line-height: 2;
    color: #333333;
}}

.idea-counter {{
    text-align: center;
    margin-top: 30px;
    font-size: 22px;
}}

</style>
""",
    unsafe_allow_html=True
)

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

    st.markdown(
        """
        <div class='logo'>
            🌱 SCAle
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='hero-title'>
            Hi! I'm SCAle.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='hero-subtitle'>
            I will help you explore sustainability project ideas tailored to your diploma and interests. Let's get started.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='hero-image'>
            <img src="data:image/png;base64,{robot_image}">
        </div>
        """,
        unsafe_allow_html=True
    )

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

    if st.button("←"):
        st.session_state.page = "welcome"
        st.rerun()

    st.markdown(
        """
        <div class='page-title'>
            What is your diploma?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='page-subtitle'>
            This helps me to tailor sustainability project ideas to your field of study.
        </div>
        """,
        unsafe_allow_html=True
    )

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

    if st.button("←"):
        st.session_state.page = "diploma"
        st.rerun()

    st.markdown(
        """
        <div class='page-title'>
            What sustainability category interests you?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='page-subtitle'>
            This allows sustainability project ideas align to your focus areas.
        </div>
        """,
        unsafe_allow_html=True
    )

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

    if st.button("←"):
        st.session_state.page = "category"
        st.rerun()

    st.markdown(
        """
        <div class='page-title'>
            What sustainability problem would you like to solve?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='page-subtitle'>
            Share a problem or challenge you have noticed in school, community, or daily life.
        </div>
        """,
        unsafe_allow_html=True
    )

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

    if st.button("←"):
        st.session_state.page = "concern"
        st.rerun()

    st.markdown(
        """
        <div class='page-title'>
            Which solution format are you interested in developing?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='page-subtitle'>
            This helps me to suggest the right type of project for you.
        </div>
        """,
        unsafe_allow_html=True
    )

    solution_type = st.selectbox(
        "Select Solution Type",
        SOLUTION_TYPES
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Submit"):

            st.session_state.solution_type = solution_type

            final_prompt = f'''
{SYSTEM_PROMPT}

Diploma:
{st.session_state.diploma}

Sustainability Category:
{st.session_state.category}

Sustainability Concern:
{st.session_state.concern}

Preferred Solution Type:
{st.session_state.solution_type}
'''

            with st.spinner("Generating ideas..."):

                response = model.generate_content(
                    final_prompt
                )

                cleaned = response.text.strip()

                cleaned = cleaned.replace(
                    "```json",
                    ""
                )

                cleaned = cleaned.replace(
                    "```",
                    ""
                )

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

    st.markdown(
        """
        <div class='result-header-small'>
            Here are your
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='result-header-large'>
            Project Ideas!
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,8,1])

    with col1:

        if st.button("◀"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

    with col2:

        st.markdown(
            f"""
            <div class='result-card'>

                <div class='idea-title'>
                    {idea['title']}
                </div>

                <div class='idea-text'>
                    {idea['idea']}
                </div>

                <div class='idea-counter'>
                    {current + 1} / {len(ideas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        if st.button("▶"):

            if current < len(ideas) - 1:
                st.session_state.current_idea += 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Over"):

            st.session_state.page = "welcome"
            st.session_state.ideas = []
            st.session_state.current_idea = 0

            st.rerun()
````
