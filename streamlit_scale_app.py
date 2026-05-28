
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
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are SCAle, an AI sustainability project assistant.

Generate EXACTLY 3 sustainability project ideas.

Requirements:
- Tailored to the diploma
- Aligned to the sustainability category
- Match the preferred solution type
- Innovative but achievable for diploma students
- Realistic and practical
- Clear and professional
- Each idea should be around 120-180 words
- Write in ONE clear paragraph

IMPORTANT:

Return ONLY plain text.

DO NOT return:
- JSON
- Markdown
- Bullet points
- Numbering
- Symbols

Use EXACTLY this format:

TITLE: Idea title

IDEA:
Paragraph


TITLE: Idea title

IDEA:
Paragraph


TITLE: Idea title

IDEA:
Paragraph
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

st.markdown("""
<style>

#MainMenu,
header,
footer {
    visibility: hidden;
}

.stApp {
    background: #F5F5F5;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* =========================================================
SCALE LOGO
========================================================= */

.scale-logo {
    font-size: 44px;
    font-weight: 700;
}

.scale-dark {
    color: #14532D;
}

.scale-light {
    color: #8BC34A;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {
    background: #14532D !important;
    color: white !important;

    border: none !important;
    border-radius: 14px !important;

    height: 58px !important;
    width: 320px !important;

    font-size: 22px !important;
    font-weight: 600 !important;

    transition: 0.2s;
}

.stButton > button:hover {
    background: #1F6F43 !important;
    color: white !important;
}

.stButton > button:active {
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

    font-size: 62px !important;
    font-weight: 300 !important;

    width: auto !important;
    height: auto !important;

    padding: 0 !important;
    margin: 0 !important;
}

.back-arrow button:hover {
    background: transparent !important;
    color: black !important;
}

/* =========================================================
TEXT
========================================================= */

.page-title {
    font-size: 58px;
    font-weight: 700;
    color: #1A1A1A;
}

.page-subtitle {
    font-size: 24px;
    color: #666666;
}

/* =========================================================
SELECT BOX
========================================================= */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,1) !important;

    border: 1px solid #D6D6D6 !important;

    border-radius: 12px !important;

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
    background: white !important;
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
    background: #14532D !important;
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

    border-radius: 12px !important;

    font-size: 18px !important;

    min-height: 220px !important;
}

/* =========================================================
IDEA CARD
========================================================= */

.idea-card {
    background: white;

    border-radius: 18px;

    padding: 50px;

    border: 1px solid #E0E0E0;
}

.idea-title {
    text-align: center;

    font-size: 34px;
    font-weight: 700;

    margin-bottom: 35px;

    color: #1A1A1A;
}

.idea-text {
    font-size: 24px;

    line-height: 2;

    color: #333333;
}

.idea-counter {
    text-align: center;

    margin-top: 40px;

    font-size: 18px;
}

.idea-arrow {
    font-size: 62px;

    color: black;

    cursor: pointer;

    text-align: center;

    margin-top: 140px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    st.markdown("""
    <div class="scale-logo">
        <span class="scale-dark">SCA</span><span class="scale-light">le</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;">
        <div class="page-title">
            Hi! I'm <span class="scale-dark">SCA</span><span class="scale-light">le</span>.
        </div>

        <br>

        <div class="page-subtitle">
            I help students generate sustainability project ideas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

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

    st.markdown("""
    <div class="page-title">
        What is your diploma?
    </div>

    <br>

    <div class="page-subtitle">
        This helps me tailor sustainability ideas to your field of study.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    diploma = st.selectbox(
        "Select your diploma",
        DIPLOMAS
    )

    st.session_state.diploma = diploma

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

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

    st.markdown("""
    <div class="page-title">
        Which sustainability category interests you?
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Select category",
        CATEGORIES
    )

    st.session_state.category = category

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

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

    st.markdown("""
    <div class="page-title">
        What sustainability problem would you like to solve?
    </div>
    """, unsafe_allow_html=True)

    concern = st.text_area(
        "Sustainability concern",
        max_chars=250
    )

    st.session_state.concern = concern

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Continue →"):

            if concern.strip() == "":
                st.warning("Please enter a concern.")

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

    st.markdown("""
    <div class="page-title">
        Which solution type do you prefer?
    </div>
    """, unsafe_allow_html=True)

    solution_type = st.selectbox(
        "Select solution type",
        SOLUTION_TYPES
    )

    st.session_state.solution_type = solution_type

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Generate Ideas"):

            with st.spinner("Generating ideas..."):

                st.session_state.ideas = generate_ideas(
                    st.session_state.diploma,
                    st.session_state.category,
                    st.session_state.concern,
                    solution_type
                )

            next_page()
            st.rerun()

# =========================================================
# PAGE 5
# =========================================================

elif st.session_state.page == 5:

    ideas = st.session_state.ideas
    current = st.session_state.current_idea

    idea = ideas[current]

    st.markdown("""
    <div style="text-align:center;">
        <div class="page-subtitle">
            Here are your
        </div>

        <div class="page-title">
            Project Ideas!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1,10,1])

    with left:

        if st.button("←", key="idea_left"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

    with center:

        st.markdown(f"""
        <div class="idea-card">

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
        """, unsafe_allow_html=True)

    with right:

        if st.button("→", key="idea_right"):

            if current < len(ideas) - 1:
                st.session_state.current_idea += 1
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Start Over"):

            st.session_state.page = 0
            st.session_state.current_idea = 0
            st.session_state.ideas = []

            st.rerun()
