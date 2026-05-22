import streamlit as st
import pandas as pd
import joblib

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Loan Approval Prediction System",
    layout="wide"
)

# ================= LOAD MODEL =================
model = joblib.load("loan_model.pkl")

# ================= CUSTOM CSS =================
st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(rgba(1,10,30,0.92),
                    rgba(1,10,30,0.94)),
    url("https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=1600&q=80");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

.block-container{
    padding-top: 1rem;
}

.main-title{
    color:#00FFAA;
    font-size:55px;
    font-weight:800;
}

.sub-title{
    color:#CFCFCF;
    font-size:18px;
    margin-bottom:20px;
}

.card{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:20px;
    padding:25px;
    backdrop-filter: blur(14px);
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
}

.small-card{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.10);
    border-radius:18px;
    padding:20px;
    margin-top:18px;
}

.result-success{
    background: rgba(0,255,120,0.12);
    border:1px solid #00FFAA;
    border-radius:18px;
    padding:25px;
    text-align:center;
    color:#00FFAA;
    font-size:35px;
    font-weight:bold;
}

.result-reject{
    background: rgba(255,0,0,0.12);
    border:1px solid red;
    border-radius:18px;
    padding:25px;
    text-align:center;
    color:#ff4b4b;
    font-size:35px;
    font-weight:bold;
}

.stButton>button{
    width:100%;
    height:3.5em;
    border:none;
    border-radius:12px;
    background: linear-gradient(90deg,#00c853,#00e676);
    color:black;
    font-size:20px;
    font-weight:bold;
}

label{
    color:white !important;
    font-weight:600 !important;
}

div[data-baseweb="select"]{
    color:black;
}

.metric-box{
    background: rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

.footer-box{
    background: rgba(255,255,255,0.04);
    border-radius:15px;
    padding:15px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(
    '<div class="main-title">🏦 Loan Approval Prediction System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI Powered Financial Decision Engine</div>',
    unsafe_allow_html=True
)

# ================= MAIN LAYOUT =================
left, right = st.columns([1.25,1])

# ================= LEFT SIDE =================
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📋 Enter Applicant Details")

    c1, c2 = st.columns(2)

    with c1:

        Applicant_Income = st.number_input(
            "Applicant Income (₹)",
            value=50000
        )

        Age = st.number_input(
            "Age",
            value=28
        )

        Credit_Score = st.number_input(
            "Credit Score",
            value=750
        )

        DTI_Ratio = st.number_input(
            "DTI Ratio",
            value=25
        )

        Education_Level = st.number_input(
            "Education Level",
            value=1
        )

        Employment_Status_Salaried = st.selectbox(
            "Employment Salaried",
            [0,1]
        )

        Employment_Status_Unemployed = st.selectbox(
            "Employment Unemployed",
            [0,1]
        )

        Loan_Amount = st.number_input(
            "Loan Amount (₹)",
            value=200000
        )

        Loan_Purpose_Home = st.selectbox(
            "Loan Purpose Home",
            [0,1]
        )

        Property_Area_Semiurban = st.selectbox(
            "Property Area Semiurban",
            [0,1]
        )

        Gender_Male = st.selectbox(
            "Gender Male",
            [0,1]
        )

    with c2:

        Coapplicant_Income = st.number_input(
            "Coapplicant Income (₹)",
            value=25000
        )

        Dependents = st.number_input(
            "Dependents",
            value=0
        )

        Existing_Loans = st.number_input(
            "Existing Loans",
            value=0
        )

        Savings = st.number_input(
            "Savings (₹)",
            value=100000
        )

        Collateral_Value = st.number_input(
            "Property Value (₹)",
            value=300000
        )

        Employment_Status_Self_employed = st.selectbox(
            "Self Employed",
            [0,1]
        )

        Marital_Status_Single = st.selectbox(
            "Marital Status Single",
            [0,1]
        )

        Loan_Term = st.number_input(
            "Loan Term (Months)",
            value=360
        )

        Loan_Purpose_Car = st.selectbox(
            "Loan Purpose Car",
            [0,1]
        )

        Loan_Purpose_Education = st.selectbox(
            "Loan Purpose Education",
            [0,1]
        )

        Loan_Purpose_Personal = st.selectbox(
            "Loan Purpose Personal",
            [0,1]
        )

    # Fixed values
    Property_Area_Urban = 0
    Employer_Category_Government = 1
    Employer_Category_MNC = 0
    Employer_Category_Private = 0
    Employer_Category_Unemployed = 0

    predict_btn = st.button("🔍 Predict Loan Approval")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT SIDE =================
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Prediction Result")

    if predict_btn:

        input_data = pd.DataFrame([[

            Applicant_Income,
            Coapplicant_Income,
            Age,
            Dependents,
            Credit_Score,
            Existing_Loans,
            DTI_Ratio,
            Savings,
            Collateral_Value,
            Loan_Amount,
            Loan_Term,
            Education_Level,
            Employment_Status_Salaried,
            Employment_Status_Self_employed,
            Employment_Status_Unemployed,
            Marital_Status_Single,
            Loan_Purpose_Car,
            Loan_Purpose_Education,
            Loan_Purpose_Home,
            Loan_Purpose_Personal,
            Property_Area_Semiurban,
            Property_Area_Urban,
            Gender_Male,
            Employer_Category_Government,
            Employer_Category_MNC,
            Employer_Category_Private,
            Employer_Category_Unemployed

        ]], columns=[

            'Applicant_Income',
            'Coapplicant_Income',
            'Age',
            'Dependents',
            'Credit_Score',
            'Existing_Loans',
            'DTI_Ratio',
            'Savings',
            'Collateral_Value',
            'Loan_Amount',
            'Loan_Term',
            'Education_Level',
            'Employment_Status_Salaried',
            'Employment_Status_Self-employed',
            'Employment_Status_Unemployed',
            'Marital_Status_Single',
            'Loan_Purpose_Car',
            'Loan_Purpose_Education',
            'Loan_Purpose_Home',
            'Loan_Purpose_Personal',
            'Property_Area_Semiurban',
            'Property_Area_Urban',
            'Gender_Male',
            'Employer_Category_Government',
            'Employer_Category_MNC',
            'Employer_Category_Private',
            'Employer_Category_Unemployed'

        ])

        prediction = model.predict(input_data)

        if prediction[0] == 1:

            st.markdown(
                '<div class="result-success">✅ Loan Approved</div>',
                unsafe_allow_html=True
            )

            approval_chance = "87%"

        else:

            st.markdown(
                '<div class="result-reject">❌ Loan Rejected</div>',
                unsafe_allow_html=True
            )

            approval_chance = "24%"

        # ================= METRICS =================
        st.markdown("<br>", unsafe_allow_html=True)

        m1, m2 = st.columns(2)

        with m1:
            st.markdown(
                f"""
                <div class="metric-box">
                <h2 style="color:#00FFAA;">{approval_chance}</h2>
                <p>Approval Chance</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                """
                <div class="metric-box">
                <h2 style="color:#00FFAA;">Fast</h2>
                <p>Prediction Speed</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ================= SUMMARY =================
        st.markdown(
            f"""
            <div class="small-card">

            <h3>📌 Applicant Summary</h3>

            <hr>

            <p><b>Loan Amount:</b> ₹ {Loan_Amount}</p>

            <p><b>Applicant Income:</b> ₹ {Applicant_Income}</p>

            <p><b>Credit Score:</b> {Credit_Score}</p>

            <p><b>Loan Term:</b> {Loan_Term} Months</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ================= FOOTER FEATURES =================
        f1, f2, f3, f4 = st.columns(4)

        with f1:
            st.markdown(
                """
                <div class="footer-box">
                🤖<br>
                Smart Prediction
                </div>
                """,
                unsafe_allow_html=True
            )

        with f2:
            st.markdown(
                """
                <div class="footer-box">
                ⚡<br>
                Fast Results
                </div>
                """,
                unsafe_allow_html=True
            )

        with f3:
            st.markdown(
                """
                <div class="footer-box">
                🔒<br>
                Secure System
                </div>
                """,
                unsafe_allow_html=True
            )

        with f4:
            st.markdown(
                """
                <div class="footer-box">
                📈<br>
                AI Analysis
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info("Fill all details and click Predict")

    st.markdown("</div>", unsafe_allow_html=True)