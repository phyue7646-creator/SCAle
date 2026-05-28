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
REMOVE HEADER / TOOLBAR / TOP SPACING
========================================================= */

header {
    visibility: hidden !important;
    height: 0rem !important;
}

[data-testid="stHeader"] {
    display: none !important;
    height: 0rem !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.main .block-container {

    max-width: 1200px !important;

    padding-top: 0rem !important;

    padding-bottom: 1rem !important;

    padding-left: 4rem !important;

    padding-right: 4rem !important;

    margin-top: 0rem !important;
}

/* REMOVE EXTRA TOP GAP */

div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

/* REMOVE DEFAULT STREAMLIT TOP SPACE */

section.main > div {
    padding-top: 0rem !important;
}/* REMOVE DEFAULT STREAMLIT TOP SPACE */

section.main > div {
    padding-top: 0rem !important;
}

/* REMOVE TRUE ROOT TOP SPACE */

[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

.main .block-container {
    padding-top: 0px !important;
    margin-top: 0px !important;
}

.element-container:first-child {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

/* =========================================================
LOGO
========================================================= */

.logo {
    font-size: 46px;
    font-weight: 700;
    margin-top: 0px;
    margin-left: 40px;
}
/* =========================================================
WELCOME PAGE LAYOUT
========================================================= */

.welcome-wrapper {

    position: relative;

    min-height: 70vh;
}

.welcome-content {

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    margin-top: 120px;
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
    font-size: 34px;
    font-weight: 700;
    color: black;
    line-height: 1.2;
    margin-bottom: 8px;
}

.question-subtitle {
    font-size: 18px;
    color: #6B7280;
    line-height: 1.5;
    margin-bottom: 24px;
}

.question-label {
    font-size: 18px;
    font-weight: 600;
    color: black;
    margin-bottom: 10px;
}

.form-section {

    width: 100px;

    max-width: 90%;
    padding-left: 2rem;
}
.page-wrap {

    margin-top: -40px;
}
/* =========================================================
GREEN BUTTONS
========================================================= */

button[kind="primary"] {
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

button[kind="primary"]:hover {
    background-color: #1F6F43  !important;
    color: white !important;                /* UPDATED */

    border: none !important; 
}

button[kind="primary"]:active {
    background-color: #1F6F43 !important;
    color: white !important;
    border: none !important;
}

button[kind="primary"]:focus {

    background-color: #1F6F43 !important;   /* UPDATED */

    color: white !important;                /* UPDATED */

    border: none !important;

    outline: none !important;

    box-shadow: none !important;}
/* =========================================================
BACK ARROW ONLY
========================================================= */

button[kind="secondary"]  {

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;

    color: black !important;

    padding: 0 !important;

    margin: 0 !important;

    min-width: auto !important;

    width: auto !important;

    height: auto !important;

    border-radius: 0 !important;
    position: relative !important;

    top: -10px !important;
}

/* BIG ARROWS */

button[kind="secondary"] p {

    color: black !important;

    font-size: 70px !important;

    font-weight: 300 !important;

    margin: 0 !important;
}

button[kind="secondary"]:hover,
button[kind="secondary"]:active,
button[kind="secondary"]:focus  {

    background: transparent !important;

    color: black !important;

    border: none !important;

    box-shadow: none !important;

    outline: none !important;
}
/* =========================================================
SELECTBOX
========================================================= */

div[data-baseweb="select"] > div {

    background-color: white !important;

    border: 1px solid #D9D9D9 !important;

    border-radius: 0px !important;

    min-height: 58px !important;

    height: 58px !important;

    box-shadow: none !important;

    display: flex !important;

    align-items: center !important;
}

/* selected value */

div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] div {

    color: black !important;

    -webkit-text-fill-color: black !important;

    opacity: 1 !important;

    font-size: 18px !important;
}

/* FIX VERTICAL ALIGNMENT */

div[data-baseweb="select"] div[class*="singleValue"] {

    position: relative !important;

    top: 0px !important;

    transform: translateY(0px) !important;

    display: flex !important;

    align-items: center !important;

    height: 58px !important;

    line-height: 58px !important;

    margin: 0 !important;
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

    background-color: #EAF4EC !important;

    color: black !important;
}

/* selected */

[aria-selected="true"] {

    background-color: #1F6F43 !important;
}

[aria-selected="true"] * {

    color: black !important;
}

/* =========================================================
TEXT AREA
========================================================= */

div[data-testid="stTextArea"] textarea {

    background-color: white !important;

    color: black !important;

    -webkit-text-fill-color: black !important;

    caret-color: black !important;

    font-size: 18px !important;

    line-height: 1.6 !important;

    border-radius: 12px !important;

    border: 0.5px solid black !important;

    box-shadow: none !important;
}

/* REMOVE RED/GREEN FOCUS EFFECT */

div[data-testid="stTextArea"] textarea:focus {

    background-color: white !important;

    color: black !important;

    border: 2px solid black !important;

    outline: none !important;

    box-shadow: none !important;
}

/* REMOVE STREAMLIT DEFAULT BORDER */

div[data-testid="stTextArea"] > div {

    border: none !important;

    box-shadow: none !important;

    background: transparent !important;
}

/* WORD COUNT */

div[data-testid="stTextArea"] p {

    color: black !important;

    font-size: 14px !important;

    opacity: 1 !important;
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

/* =========================================================
CENTER BUTTON
========================================================= */

.button-center {

    display: flex;

    justify-content: center;

    align-items: center;

    width: 100%;
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    

    st.markdown(
        '<div style="text-align:center;"><div class="page-title">Hi! I\'m SCAle.</div><br><div class="page-subtitle">I will help you to explore sustainability project ideas tailored to your diploma and interests. Let\'s get started.</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
   
    

    #image = Image.open("d06d65c5-67c9-4a99-b853-40525a2c4d2c.png")

    #c1, c2, c3 = st.columns([1,1,1])

    #with c2:
        #st.image(image, width=430)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.3,1,1])

    with c2:
        if st.button("Start Your Project Ideas", type="primary"):
            st.session_state.page = "diploma"
            st.rerun()

    # button_left, button_center, button_right = st.columns([1,1,1])

    # with button_center:
    #     if st.button("Start Your Project Ideas", type="primary"):
    #         st.session_state.page = "diploma"
    #         st.rerun()


    
# =========================================================
# DIPLOMA PAGE
# =========================================================

elif st.session_state.page == "diploma":

    back_left, back_right = st.columns([0.08, 0.92])

    with back_left:
        if st.button("←", key="back1", type="secondary"):
            st.session_state.page = "welcome"
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
   
    
    st.markdown(
    '<div class="page-wrap"><div class="form-section">',
    unsafe_allow_html=True
    )

    st.markdown(
        '<div class="question-title">What is your diploma?</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="question-subtitle">This helps me to tailor sustainability project ideas to your field of study.</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="question-label">Select your diploma</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.session_state.diploma = st.selectbox(
        "Select Diploma",
        diplomas,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    button_left, button_center, button_right = st.columns([2.2,1,2.2])
    
    with button_center:
        if st.button("Continue →", type="primary"):
            st.session_state.page = "category"
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CATEGORY PAGE
# =========================================================

elif st.session_state.page == "category":

    back_left, back_right = st.columns([0.08, 0.92])

    with back_left:
        if st.button("←", key="back2", type="secondary"):
            st.session_state.page = "diploma"
            st.rerun()
    st.markdown(
    '<div class="page-wrap"><div class="form-section">',
    unsafe_allow_html=True
    )
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
        "Select Category",
        categories,
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    button_left, button_center, button_right = st.columns([2.2,1,2.2])
    
    with button_center:
        if st.button("Continue →", type="primary"):
            st.session_state.page = "concern"
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)
# =========================================================
# CONCERN PAGE
# =========================================================

elif st.session_state.page == "concern":

    back_left, back_right = st.columns([0.08, 0.92])

    with back_left:
        if st.button("←", key="back3", type="secondary"):
            st.session_state.page = "category"
            st.rerun()
    st.markdown(
    '<div class="page-wrap"><div class="form-section">',
    unsafe_allow_html=True
    )
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
        height=140,
        max_chars=200,
        label_visibility="collapsed"
    ) 

    button_left, button_center, button_right = st.columns([2.2,1,2.2])

    with button_center:
        if st.button("Continue →", type="primary"):
            st.session_state.page = "solution"
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

# =========================================================
# SOLUTION PAGE
# =========================================================

elif st.session_state.page == "solution":

    back_left, back_right = st.columns([0.08, 0.92])

    with back_left:
        if st.button("←", key="back4", type="secondary"):
            st.session_state.page = "concern"
            st.rerun()

    st.markdown(
    '<div class="page-wrap"><div class="form-section">',
    unsafe_allow_html=True
    )
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
        "Select Solution",
        solutions,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    button_left, button_center, button_right = st.columns([2.2,1,2.2])

    with button_center:
        if st.button("Submit", type="primary"):
    
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
    st.markdown('</div></div>', unsafe_allow_html=True)
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

    col1, col2, col3 = st.columns([1.5,6,1.5])

    with col1:
        if current > 0:
            if st.button("←", key="prev", type="primary"):
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
            if st.button("→", key="next", type="primary"):
                st.session_state.idea_index += 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    button_left, button_center, button_right = st.columns([2.2,1,2.2])

    with button_center:
        if st.button("Start Over", type="primary"):

            st.session_state.page = "welcome"
            st.session_state.idea_index = 0

            st.rerun()
