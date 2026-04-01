import streamlit as st
import pandas as pd
import base64

from utils.loader import load_data
from utils.cleaner import get_nulls, remove_nulls, fill_nulls, remove_duplicates
from utils.insights import generate_insights, data_quality_score
from utils.visualizer import auto_visualize
from utils.outliers import detect_outliers
from utils.profiler import generate_profile
from utils.nlp_query import process_query
from utils.report import generate_pdf_report
from utils.trend import trend_analysis

# ---------------- BACKGROUND ----------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10,15,25,0.85), rgba(10,15,25,0.85)),
                          url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Glass container */
    .block-container {{
        background: rgba(15, 23, 42, 0.6);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(12px);
    }}

    /* Upload */
    .stFileUploader {{
        background: rgba(30, 41, 59, 0.6) !important;
        border: 2px dashed rgba(59,130,246,0.5);
        border-radius: 15px;
        padding: 20px;
    }}

    /* Text */
    h1, h2, h3 {{
        color: #e2e8f0;
    }}

    p, label {{
        color: #cbd5f5;
    }}

    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
        border-radius: 10px;
        border: none;
    }}

    /* Metrics */
    [data-testid="stMetric"] {{
        background: rgba(30, 41, 59, 0.6);
        padding: 15px;
        border-radius: 12px;
        color: white;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: rgba(2, 6, 23, 0.95);
    }}

    section[data-testid="stSidebar"] * {{
        color: #e2e8f0 !important;
    }}

    /* Alerts */
    .stAlert {{
        background-color: rgba(59,130,246,0.2);
        color: #e2e8f0;
        border-radius: 10px;
    }}

    </style>
    """, unsafe_allow_html=True)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Data Analyst", layout="wide")

# Apply background (put image in same folder)
set_bg("background.png")

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center; font-size: 42px; color: #ffffff;
text-shadow: 0px 0px 10px rgba(59,130,246,0.8);'>
🤖 AI-Powered Smart Data Analyst
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align: center; color:#cbd5f5;'>
📊 Analyze • Clean • Visualize • Understand your data with AI
</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- UPLOAD UI ----------------
st.markdown("""
<div style="
    background: rgba(30,41,59,0.6);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
">
    <h3 style="color:#e2e8f0;">📂 Upload Your Dataset</h3>
    <p style="color:#cbd5f5;">Drag & drop your CSV file below</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["csv"])

# ---------------- MAIN APP ----------------
if uploaded_file:
    df = load_data(uploaded_file)

    # Sidebar
    st.sidebar.title("⚙️ Navigation")
    option = st.sidebar.radio("Select Module", [
        "Dashboard",
        "Data Cleaning",
        "Insights",
        "Visualization",
        "Trends",
        "Outliers",
        "Data Score",
        "Profiling",
        "AI Chat",
        "Report"
    ])

    # Dashboard
    if option == "Dashboard":
        st.subheader("📊 Dashboard")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing", df.isnull().sum().sum())
        col4.metric("Duplicates", df.duplicated().sum())

        st.dataframe(df.head(), use_container_width=True)

    # Cleaning
    elif option == "Data Cleaning":
        st.subheader("🧹 Data Cleaning")

        if st.button("Show Nulls"):
            st.write(get_nulls(df))

        if st.button("Remove Nulls"):
            df = remove_nulls(df)
            st.success("Removed nulls")

        if st.button("Fill Nulls"):
            df = fill_nulls(df)
            st.success("Filled nulls")

        if st.button("Remove Duplicates"):
            df = remove_duplicates(df)
            st.success("Duplicates removed")

        csv = df.to_csv(index=False).encode()
        st.download_button("📥 Download Cleaned Data", csv, "cleaned.csv")

    # Insights
    elif option == "Insights":
        st.subheader("🧠 Insights")

        insights = generate_insights(df)
        if insights:
            for i in insights:
                st.info(i["message"])
        else:
            st.success("Dataset looks clean")

    # Visualization
    elif option == "Visualization":
        st.subheader("📈 Visualizations")

        plots = auto_visualize(df)
        for p in plots:
            st.pyplot(p)

    # Trends
    elif option == "Trends":
        st.subheader("📊 Trends")

        plots = trend_analysis(df)
        for p in plots:
            st.pyplot(p)

    # Outliers
    elif option == "Outliers":
        st.subheader("🚨 Outliers")

        out = detect_outliers(df)
        for k, v in out.items():
            st.write(f"{k}: {v}")

    # Score
    elif option == "Data Score":
        st.subheader("🏆 Quality Score")

        score = data_quality_score(df)
        st.metric("Score", f"{score}/100")

    # Profiling
    elif option == "Profiling":
        st.subheader("📄 Profiling Report")

        profile = generate_profile(df)
        st.components.v1.html(profile.to_html(), height=800)

    # AI Chat
    elif option == "AI Chat":
        st.subheader("🤖 AI Chat")

        q = st.text_input("Ask your data")
        if q:
            st.write(process_query(q, df))

    # Report
    elif option == "Report":
        st.subheader("📄 Generate Report")

        insights = generate_insights(df)

        if st.button("Generate Report"):
            file = generate_pdf_report(df, insights)

            with open(file, "rb") as f:
                st.download_button("Download PDF", f, "report.pdf")

else:
    st.warning("👆 Upload dataset to start")