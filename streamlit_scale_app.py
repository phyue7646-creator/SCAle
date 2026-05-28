import streamlit as st
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

model = genai.GenerativeModel("gemini-2.5-flash")

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
# FUNCTIONS
# =========================================================

def next_page():
    st.session_state.page += 1

def previous_page():
    st.session_state.page -= 1

def generate_ideas(diploma, category, concern, solution_type):

    prompt = f"""
Diploma:
{diploma}

Sustainability Category:
{category}

Sustainability Concern:
{concern}

Preferred Solution Type:
{solution_type}
"""

    response = model.generate_content(
        SYSTEM_PROMPT + "\n\n" + prompt
    )

    text = response.text.strip()

    ideas = []

    sections = text.split("TITLE:")

    for section in sections:

        section = section.strip()

        if not section:
            continue

        if "IDEA:" in section:

            title_part, idea_part = section.split("IDEA:", 1)

            title = title_part.strip()
            idea = idea_part.strip()

            ideas.append({
                "title": title,
                "idea": idea
            })

    return ideas

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }

    .stApp {
        background-color: #F5F5F5;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* =========================================================
    LOGO
    ========================================================= */

    .scale-logo {
        font-size: 42px;
        font-weight: 700;
    }

    /* =========================================================
    TEXT
    ========================================================= */

    .page-title {
        font-size: 56px;
        font-weight: 700;
        color: #161616;
        line-height: 1.2;
    }

    .page-subtitle {
        font-size: 24px;
        color: #666666;
        line-height: 1.7;
    }

    /* =========================================================
    LABELS
    ========================================================= */

    label,
    .stSelectbox label,
    .stTextArea label {
        color: black !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    /* =========================================================
    BUTTONS
    ========================================================= */

    .stButton > button {
        background: #1F6F43 !important;
        color: white !important;

        border: none !important;
        border-radius: 14px !important;

        min-height: 60px !important;
        width: 340px !important;

        font-size: 22px !important;
        font-weight: 700 !important;

        transition: 0.2s;
    }

    .stButton > button:hover {
        background: #1F6F43 !important;
        color: white !important;
    }

    .stButton > button:active {
        background: #1F6F43 !important;
        color: white !important;
    }

    /* =========================================================
    BACK ARROW
    ========================================================= */

    .back-arrow button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;

        color: black !important;

        width: auto !important;
        height: auto !important;

        padding: 0 !important;
        margin: 0 !important;

        min-height: unset !important;

        font-size: 72px !important;
        font-weight: 300 !important;
    }

    .back-arrow button:hover {
        background: transparent !important;
        color: black !important;
    }

    .back-arrow button:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    .back-arrow button p {
        font-size: 72px !important;
        margin: 0 !important;
        color: black !important;
    }

    /* =========================================================
    SELECT BOX
    ========================================================= */

    div[data-baseweb="select"] > div {
        background: white !important;

        border: 1px solid #D9D9D9 !important;

        border-radius: 0px !important;

        min-height: 60px !important;

        box-shadow: none !important;
    }

    div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    div[role="listbox"] {
        background: white !important;
        border: 1px solid #D9D9D9 !important;
    }

    div[role="option"] {
        background: white !important;
        color: black !important;

        font-size: 17px !important;
    }

    div[role="option"]:hover {
        background: #E7F3EC !important;
        color: black !important;
    }

    div[aria-selected="true"] {
        background: #1F6F43 !important;
    }

    div[aria-selected="true"] * {
        color: white !important;
    }

    /* =========================================================
    TEXT AREA
    ========================================================= */

    .stTextArea textarea {
        background: white !important;
        color: black !important;

        border: 1px solid #D9D9D9 !important;

        border-radius: 4px !important;

        font-size: 18px !important;

        min-height: 230px !important;

        padding: 18px !important;
    }

    /* =========================================================
    IDEA CARD
    ========================================================= */

    .idea-card {
        background: white;

        border: 1px solid #E1E1E1;

        border-radius: 18px;

        padding: 42px;
    }

    .idea-title {
        text-align: center;

        font-size: 32px;
        font-weight: 700;

        margin-bottom: 28px;

        color: #161616;
    }

    .idea-text {
        font-size: 20px;

        line-height: 2;

        color: #2B2B2B;

        text-align: left;
    }

    .idea-counter {
        text-align: center;

        margin-top: 28px;

        font-size: 18px;

        color: black;
    }

    /* =========================================================
    ARROWS
    ========================================================= */

    .arrow-button button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;

        color: #1F6F43 !important;

        width: auto !important;
        height: auto !important;

        min-height: unset !important;

        font-size: 70px !important;

        padding-top: 150px !important;
    }

    .arrow-button button:hover {
        background: transparent !important;
    }

    .arrow-button button p {
        font-size: 70px !important;
        color: #1F6F43 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    st.markdown(
        """
        <div class="scale-logo">
            <span style="color:#14532D;">SCA</span><span style="color:#8BC34A;">le</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center;">

            <div class="page-title">
                Hi! I'm
                <span style="color:#14532D;">SCA</span><span style="color:#8BC34A;">le</span>.
            </div>

            <br>

            <div class="page-subtitle">
                I will help you to explore sustainability project ideas tailored to your diploma and interests. Let's get started.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.image(
        "d06d65c5-67c9-4a99-b853-40525a2c4d2c.png",
        width=420
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Your Project Ideas"):
            next_page()
            st.rerun()

# =========================================================
# PAGE 1
# =========================================================

elif st.session_state.page == 1:

    st.write("Page 1")
