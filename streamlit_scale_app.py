import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# GEMINI API
# =========================================================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

client = genai.Client(
    api_key=GOOGLE_API_KEY
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background-color: #f5f5f5;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    color: #2f5e36;
    margin-top: 20px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 24px;
    color: #555;
    margin-bottom: 40px;
}

/* Section Title */
.section-title {
    font-size: 42px;
    font-weight: 700;
    color: #1f1f1f;
    margin-bottom: 10px;
}

/* Section Description */
.section-desc {
    font-size: 22px;
    color: #666;
    margin-bottom: 30px;
}

/* Card */
.result-card {
    background: white;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-top: 20px;
}

/* Buttons */
.stButton > button {
    background-color: #46784d;
    color: white;
    border-radius: 12px;
    height: 60px;
    width: 280px;
    font-size: 22px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #35603b;
    color: white;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: white;
    border-radius: 12px;
    border: 2px solid #dcdcdc;
    min-height: 58px;
}

/* Text Area */
textarea {
    border-radius: 12px !important;
    border: 2px solid #dcdcdc !important;
    font-size: 18px !important;
}

/* Result Text */
.idea-title {
    font-size: 34px;
    font-weight: 700;
    color: #2f5e36;
    margin-bottom: 20px;
}

.idea-text {
    font-size: 21px;
    line-height: 1.8;
    color: #333;
}

.center {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATES
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

if "generated_idea" not in st.session_state:
    st.session_state.generated_idea = ""

# =========================================================
# DATA
# =========================================================

diplomas = [
    "Diploma in Big Data & Analytics",
    "Diploma in Information Technology",
    "Diploma in Applied AI",
    "Diploma in Chemical Engineering",
    "Diploma in Accountancy & Finance",
    "Diploma in Business",
    "Diploma in Cybersecurity",
    "Diploma in Pharmaceutical Science",
    "Diploma in Medical Biotechnology",
    "Diploma in Marketing"
]

categories = [
    "Circular Economy",
    "Renewable Energy",
    "Green Transportation",
    "Sustainable Tourism",
    "Waste Management and Recycling",
    "Green Buildings",
    "Sustainable Food Systems",
    "Biodiversity and Conservation"
]

solution_types = [
    "Digital Prototype",
    "Physical Prototype",
    "Social Campaign"
]

# =========================================================
# WELCOME PAGE
# =========================================================

if st.session_state.page == "welcome":

    st.markdown(
        "<div class='main-title'>🌱 SCAle</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>"
        "Suggests scaling sustainability impact and innovation"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4149/4149670.png",
            width=300
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='center'>
        <h2>Hi! I'm SCAle.</h2>
        <p style='font-size:24px;color:#666;'>
        I will help you explore sustainability project ideas tailored to your diploma and interests.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Your Project Ideas"):
            st.session_state.page = "diploma"
            st.rerun()

# =========================================================
# DIPLOMA PAGE
# =========================================================

elif st.session_state.page == "diploma":

    st.markdown(
        "<div class='section-title'>What is your diploma?</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-desc'>"
        "This helps me tailor sustainability project ideas to your field of study."
        "</div>",
        unsafe_allow_html=True
    )

    st.session_state.diploma = st.selectbox(
        "Select your diploma",
        diplomas
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Continue →"):
        st.session_state.page = "category"
        st.rerun()

# =========================================================
# CATEGORY PAGE
# =========================================================

elif st.session_state.page == "category":

    st.markdown(
        "<div class='section-title'>What sustainability category interests you?</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-desc'>"
        "This allows sustainability project ideas align to your focus areas."
        "</div>",
        unsafe_allow_html=True
    )

    st.session_state.category = st.selectbox(
        "Select sustainability category",
        categories
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Continue →"):
        st.session_state.page = "concern"
        st.rerun()

# =========================================================
# CONCERN PAGE
# =========================================================

elif st.session_state.page == "concern":

    st.markdown(
        "<div class='section-title'>What sustainability problem would you like to solve?</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-desc'>"
        "Share a problem or challenge you have noticed in school, community, or daily life."
        "</div>",
        unsafe_allow_html=True
    )

    st.session_state.concern = st.text_area(
        "Sustainability concern",
        max_chars=300,
        height=250
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Continue →"):
        st.session_state.page = "solution"
        st.rerun()

# =========================================================
# SOLUTION PAGE
# =========================================================

elif st.session_state.page == "solution":

    st.markdown(
        "<div class='section-title'>Which solution format are you interested in developing?</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='section-desc'>"
        "This helps me to suggest the right type of project for you."
        "</div>",
        unsafe_allow_html=True
    )

    st.session_state.solution = st.selectbox(
        "Select solution type",
        solution_types
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Generate Idea"):

        prompt = f"""
Generate ONE innovative but achievable sustainability project idea.

Requirements:
- Tailored to the diploma
- Related to the sustainability category
- Match the sustainability concern
- Match the preferred solution type
- Suitable for diploma students
- Realistic and practical
- Clear explanation
- Around 180-250 words
- Include:
    1. Project title
    2. Description
    3. Main features
    4. Sustainability impact

Diploma:
{st.session_state.diploma}

Category:
{st.session_state.category}

Concern:
{st.session_state.concern}

Solution Type:
{st.session_state.solution}
"""

        with st.spinner("Generating sustainability idea..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

            st.session_state.generated_idea = response.text
            st.session_state.page = "result"
            st.rerun()

# =========================================================
# RESULT PAGE
# =========================================================

elif st.session_state.page == "result":

    st.markdown(
        """
        <div class='center'>
        <h1 style='color:#2f5e36;'>💡 Here are your Project Ideas!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='result-card'>
            <div class='idea-text'>
                {st.session_state.generated_idea}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Over"):
            st.session_state.page = "welcome"
            st.rerun()
