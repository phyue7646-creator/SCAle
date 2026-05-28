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

st.markdown("""
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
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* =========================================================
LOGO
========================================================= */

.scale-logo {
    display: flex;
    align-items: center;
}

.scale-logo-text {
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

    font-size: 72px !important;
    font-weight: 300 !important;

    min-height: unset !important;
}

.back-arrow button:hover {
    background: transparent !important;
    color: black !important;
    border: none !important;
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
    background: rgba(255,255,255,1) !important;

    border: 1px solid #D9D9D9 !important;

    border-radius: 0px !important;

    min-height: 60px !important;

    box-shadow: none !important;
}

/* Selected text */

div[data-baseweb="select"] span {
    color: black !important;
    font-size: 18px !important;
}

/* Dropdown popup */

div[role="listbox"] {
    background: white !important;
    border: 1px solid #D9D9D9 !important;
}

/* Dropdown option */

div[role="option"] {
    background: white !important;
    color: black !important;

    font-size: 17px !important;
}

/* Hover */

div[role="option"]:hover {
    background: #E7F3EC !important;
    color: black !important;
}

/* Selected */

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

    font-size: 70px !important;

    padding-top: 150px !important;

    min-height: unset !important;
}

.arrow-button button:hover {
    background: transparent !important;
}

.arrow-button button p {
    font-size: 70px !important;
    color: #1F6F43 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 0
# =========================================================

if st.session_state.page == 0:

    st.markdown("""
    <div class="scale-logo">
        <div class="scale-logo-text">
            <span style="color:#14532D;">SCA</span><span style="color:#8BC34A;">le</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
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
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.image(
        "https://i.imgur.com/V4sQ9mA.png",
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

    col_back, col_space = st.columns([0.08, 0.92])

    with col_back:

        st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

        if st.button("←", key="back1"):
            previous_page()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">
        What is your diploma?
    </div>

    <br>

    <div class="page-subtitle">
        This helps me to tailor sustainability project ideas to your field of study.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

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

    col_back, col_space = st.columns([0.08, 0.92])

    with col_back:

        st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

        if st.button("←", key="back2"):
            previous_page()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">
        What sustainability category interests you?
    </div>

    <br>

    <div class="page-subtitle">
        This allows sustainability project ideas align to your focus areas.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    category = st.selectbox(
        "Select sustainability category",
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

    col_back, col_space = st.columns([0.08, 0.92])

    with col_back:

        st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

        if st.button("←", key="back3"):
            previous_page()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">
        What sustainability problem would you like to solve?
    </div>

    <br>

    <div class="page-subtitle">
        Share an problem or challenge you have noticed in school, community, or daily life.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    concern = st.text_area(
        "Sustainability concern",
        max_chars=200
    )

    st.session_state.concern = concern

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Continue →"):

            if concern.strip() == "":
                st.warning("Please enter a sustainability concern.")

            else:
                next_page()
                st.rerun()

# =========================================================
# PAGE 4
# =========================================================

elif st.session_state.page == 4:

    col_back, col_space = st.columns([0.08, 0.92])

    with col_back:

        st.markdown('<div class="back-arrow">', unsafe_allow_html=True)

        if st.button("←", key="back4"):
            previous_page()
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">
        Which solution format are you interested in developing?
    </div>

    <br>

    <div class="page-subtitle">
        This helps me to suggest the right type of project for you.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    solution_type = st.selectbox(
        "Select Solution Type",
        SOLUTION_TYPES
    )

    st.session_state.solution_type = solution_type

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        if st.button("Submit"):

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

        <div style="font-size:22px;font-weight:600;color:black;">
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

        st.markdown('<div class="arrow-button">', unsafe_allow_html=True)

        if st.button("←", key="idea_left"):

            if current > 0:
                st.session_state.current_idea -= 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="arrow-button">', unsafe_allow_html=True)

        if st.button("→", key="idea_right"):

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
