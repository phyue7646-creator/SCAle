import streamlit as st
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SCAle",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# GOOGLE GEMINI API
# =========================================================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #F7F8F5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Buttons */
.stButton > button {
    background-color: #477A4A;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 28px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #355E38;
    color: white;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    border-radius: 12px;
    border: 1px solid #D8E4D2;
}

/* Text area */
textarea {
    border-radius: 12px !important;
    border: 1px solid #D8E4D2 !important;
}

/* Main Title */
.main-title {
    text-align: center;
    color: #2F5D3A;
    font-size: 52px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #5B5B5B;
    font-size: 22px;
    margin-bottom: 40px;
}

/* Section Header */
.section-header {
    color: #2F5D3A;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 8px;
}

/* Description */
.section-desc {
    color: #666666;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Result Card */
.result-card {
    background-color: white;
    padding: 40px;
    border-radius: 22px;
    border: 1px solid #DCE8D7;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

/* Scale Logo */
.scale-logo {
    font-size: 58px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 10px;
}

.scale-green {
    color: #7BAE3F;
}

.scale-dark {
    color: #355E38;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

solution_types = [
    "Digital Prototype",
    "Physical Prototype",
    "Social Campaign"
]

categories = [
    "Circular Economy",
    "Renewable Energy",
    "Green Transportation",
    "Waste Management and Recycling",
    "Sustainable Food Systems",
    "Green Buildings",
    "Biodiversity and Conservation",
    "Green Finance and Impact Investing",
    "Liveable City and Community",
    "Sustainable Tourism"
]

diplomas = [
    "Diploma in Big Data & Analytics",
    "Diploma in Information Technology",
    "Diploma in Applied AI",
    "Diploma in Chemical Engineering",
    "Diploma in Accountancy & Finance",
    "Diploma in Business",
    "Diploma in Marketing",
    "Diploma in Pharmaceutical Science",
    "Diploma in Veterinary Technology",
    "Diploma in Communication Design"
]

# =========================================================
# SESSION STATES
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "generated_idea" not in st.session_state:
    st.session_state.generated_idea = ""

# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    st.markdown("""
    <div class="scale-logo">
        <span class="scale-green">SCA</span><span class="scale-dark">le</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
        Hi! I'm SCAle.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sub-title">
        I will help you explore sustainability project ideas tailored to your diploma and interests.
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4149/4149670.png",
        width=320
    )

    st.write("")

    center = st.columns([1, 1, 1])

    with center[1]:
        if st.button("Start Your Project Ideas", use_container_width=True):
            st.session_state.page = "form"
            st.rerun()

# =========================================================
# FORM PAGE
# =========================================================

elif st.session_state.page == "form":

    st.markdown("""
    <div class="section-header">
        Generate Sustainability Project Ideas
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-desc">
        Fill in the information below and SCAle will generate a personalized sustainability project idea.
    </div>
    """, unsafe_allow_html=True)

    diploma = st.selectbox(
        "Select your diploma",
        diplomas
    )

    category = st.selectbox(
        "Select sustainability category",
        categories
    )

    concern = st.text_area(
        "Describe your sustainability concern",
        height=180,
        max_chars=300,
        placeholder="Example: Food waste in hawker centres, excessive electricity consumption, poor recycling habits..."
    )

    solution_type = st.selectbox(
        "Select solution type",
        solution_types
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button("Generate Idea", use_container_width=True):

            if concern.strip() == "":
                st.warning("Please enter your sustainability concern.")
            else:

                with st.spinner("Generating sustainability idea..."):

                    prompt = f"""
You are SCAle, an AI assistant that generates sustainability project ideas for diploma students.

Generate ONE innovative but achievable sustainability project idea.

Student Information:
- Diploma: {diploma}
- Sustainability Category: {category}
- Sustainability Concern: {concern}
- Preferred Solution Type: {solution_type}

Requirements:
- Tailor the project to the student's diploma skills
- Ensure the idea is realistic for diploma students
- Focus on sustainability impact
- Keep the explanation concise but complete
- Avoid overly technical or unrealistic ideas
- Do not generate mobile app names or campaign names
- Output only the project idea title and description

Format:

Project Title

Project Description
"""

                    try:

                        response = model.generate_content(prompt)

                        st.session_state.generated_idea = response.text
                        st.session_state.page = "result"
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error generating response: {e}")

# =========================================================
# RESULT PAGE
# =========================================================

elif st.session_state.page == "result":

    st.markdown("""
    <div class="scale-logo">
        <span class="scale-green">SCA</span><span class="scale-dark">le</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
        Your Project Idea
    </div>
    """, unsafe_allow_html=True)

    formatted_response = st.session_state.generated_idea.replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="result-card">

            <div style="
                color:#2F5D3A;
                font-size:34px;
                font-weight:700;
                margin-bottom:25px;
                text-align:center;
            ">
                🌱 Sustainability Project Idea
            </div>

            <div style="
                font-size:20px;
                line-height:1.9;
                color:#2E2E2E;
                text-align:justify;
            ">
                {formatted_response}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:

        if st.button("Start Over", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.generated_idea = ""
            st.rerun()
