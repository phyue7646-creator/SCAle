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
# GEMINI API
# =========================================================

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #F5F5F2;
}

/* hide streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* headings */

.main-title{
    font-size:58px;
    font-weight:700;
    color:#1F1F1F;
    text-align:center;
    margin-bottom:10px;
}

.sub-title{
    font-size:24px;
    color:#666666;
    text-align:center;
    margin-bottom:50px;
}

.question-title{
    font-size:52px;
    font-weight:700;
    color:#1F1F1F;
    margin-bottom:15px;
}

.question-desc{
    font-size:24px;
    color:#666666;
    margin-bottom:40px;
}

/* buttons */

.stButton > button{
    background-color:#477A4A;
    color:white;
    border:none;
    border-radius:14px;
    height:60px;
    font-size:24px;
    font-weight:600;
    width:100%;
}

.stButton > button:hover{
    background-color:#355E38;
    color:white;
}

/* selectbox */

div[data-baseweb="select"] > div{
    min-height:58px;
    border-radius:10px;
    border:1px solid #D6D6D6;
    font-size:20px;
}

/* textarea */

textarea{
    border-radius:12px !important;
    border:1px solid #D6D6D6 !important;
    font-size:18px !important;
}

/* result card */

.result-card{
    background:white;
    border-radius:22px;
    padding:45px;
    border:1px solid #DDDDDD;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
}

/* logo */

.logo{
    font-size:48px;
    font-weight:800;
}

.logo-light{
    color:#8EB54B;
}

.logo-dark{
    color:#355E38;
}

.center{
    text-align:center;
}

/* arrows */

.arrow-btn{
    font-size:50px;
    color:#477A4A;
}

/* section spacing */

.top-space{
    margin-top:80px;
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
    <div class="logo">
        <span class="logo-dark">🌱 SCA</span><span class="logo-light">le</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="top-space"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
        Hi! I'm SCAle.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sub-title">
        I will help you explore sustainability project ideas tailored to your diploma and interests. Let's get started.
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
            width=420
        )

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("Start Your Project Ideas"):
            st.session_state.page = "diploma"
            st.rerun()

# =========================================================
# DIPLOMA PAGE
# =========================================================

elif st.session_state.page == "diploma":

    st.markdown("# ←")

    st.markdown("""
    <div class="top-space"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-title">
        What is your diploma?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-desc">
        This helps me to tailor sustainability project ideas to your field of study.
    </div>
    """, unsafe_allow_html=True)

    diploma = st.selectbox(
        "Select your diploma",
        diplomas
    )

    st.session_state.diploma = diploma

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):
            st.session_state.page = "category"
            st.rerun()

# =========================================================
# CATEGORY PAGE
# =========================================================

elif st.session_state.page == "category":

    st.markdown("# ←")

    st.markdown("""
    <div class="top-space"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-title">
        What sustainability category interests you?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-desc">
        This allows sustainability project ideas align to your focus areas.
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "Select sustainability category",
        categories
    )

    st.session_state.category = category

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):
            st.session_state.page = "concern"
            st.rerun()

# =========================================================
# CONCERN PAGE
# =========================================================

elif st.session_state.page == "concern":

    st.markdown("# ←")

    st.markdown("""
    <div class="top-space"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-title">
        What sustainability problem would you like to solve?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-desc">
        Share an issue or challenge you have noticed in school, community, or daily life.
    </div>
    """, unsafe_allow_html=True)

    concern = st.text_area(
        "Sustainability concern",
        height=220,
        max_chars=200
    )

    st.session_state.concern = concern

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("Continue →"):
            st.session_state.page = "solution"
            st.rerun()

# =========================================================
# SOLUTION PAGE
# =========================================================

elif st.session_state.page == "solution":

    st.markdown("# ←")

    st.markdown("""
    <div class="top-space"></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-title">
        Which solution format are you interested in developing?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-desc">
        This helps me to suggest the right type of project for you.
    </div>
    """, unsafe_allow_html=True)

    solution_type = st.selectbox(
        "Select Solution Type",
        solution_types
    )

    st.session_state.solution_type = solution_type

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("Submit"):

            with st.spinner("Generating idea..."):

                prompt = f"""
Generate ONE sustainability project idea.

Diploma:
{st.session_state.diploma}

Category:
{st.session_state.category}

Concern:
{st.session_state.concern}

Solution Type:
{st.session_state.solution_type}

Requirements:
- realistic
- innovative
- diploma-level
- sustainability focused
- concise but complete
"""

                response = model.generate_content(prompt)

                st.session_state.generated_idea = response.text

                st.session_state.page = "result"

                st.rerun()

# =========================================================
# RESULT PAGE
# =========================================================

elif st.session_state.page == "result":

    st.markdown("""
    <div class="center">
        <img src="https://cdn-icons-png.flaticon.com/512/427/427735.png" width="120">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="center">
        <div style="font-size:34px;font-weight:700;color:#1F1F1F;">
            Here are your
        </div>

        <div style="font-size:62px;font-weight:800;color:#355E38;">
            Project Ideas!
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,8,1])

    with col2:

        formatted = st.session_state.generated_idea.replace("\n","<br>")

        st.markdown(
            f"""
            <div class="result-card">

                <div style="
                    font-size:22px;
                    line-height:1.9;
                    color:#2A2A2A;
                    text-align:justify;
                ">
                    {formatted}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    col1,col2,col3 = st.columns([1,2,1])

    with col2:
        if st.button("Start Over"):
            st.session_state.page = "home"
            st.session_state.generated_idea = ""
            st.rerun()
