import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load the environment variables
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# Set page config
st.set_page_config(page_title="Resume ATS Score Checker", page_icon="📄", layout="wide")

# Custom CSS for Glassmorphism and Modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Fade In Animation */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .stMarkdown, .stButton, div[data-testid="stMetric"] {
        animation: fadeIn 0.8s ease-out forwards;
    }

    /* Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease;
    }
    
    /* Typography */
    h1 {
        font-weight: 700;
        color: transparent;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    p, label, li {
        color: #e0e0e0 !important;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: rgba(0, 210, 255, 0.1);
        border: 1px solid rgba(0, 210, 255, 0.3);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #b0c4de !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00d2ff !important;
        font-size: 2.5rem !important;
    }

    /* Custom Input Styling */
    .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
    }
    
    .stTextArea textarea:focus {
        border-color: #00c6ff !important;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.05);
    }

    /* Gradient Button */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0, 210, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 25px rgba(0, 210, 255, 0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0 0;
        color: white;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 210, 255, 0.2);
        color: #00d2ff;
        border-bottom: 2px solid #00d2ff;
    }

</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; color: white;'>🚀 Resume ATS Score Checker</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 3rem;'>
    <p style='font-size: 1.2rem; display: inline-block; background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 50px; border: 1px solid rgba(255,255,255,0.2);'>
        Optimize your resume for <b>Software Engineering</b>, <b>Data Science</b>, and more.
    </p>
</div>
""", unsafe_allow_html=True)

# Main Dashboard Layout
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📋 Job Description")
    jd = st.text_area("Paste the text here", height=300, label_visibility="collapsed", placeholder="Paste the full job description here...")

with col2:
    st.markdown("### 📤 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", label_visibility="collapsed")
    
    if uploaded_file:
        st.success("✅ File uploaded successfully")
    else:
        st.info("Supported format: PDF")

st.markdown("<br>", unsafe_allow_html=True)
check_btn = st.button("✨ Analyze Resume Score")

# Logic
import json 

if check_btn:
    if uploaded_file is not None and jd:
        with st.status("🚀 Processing your Request...", expanded=True) as status:
            try:
                # 1. Extract Text
                status.write("📄 Extracting text from PDF...")
                reader = pdf.PdfReader(uploaded_file)
                extracted_text = ""
                for page in range(len(reader.pages)):
                    page = reader.pages[page]
                    extracted_text += page.extract_text()
                
                # 2. Analyze with Gemini
                status.write("🧠 Analyzing resume against Job Description...")
                
                input_prompt = f"""
                You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of tech job markets and resume optimization. 

                Task: Evaluate the Resume against the Job Description.

                Resume: {extracted_text}
                Job Description: {jd}

                Output Format: Provide a valid JSON string with the following keys:
                {{
                    "match_percentage": "Integer between 0-100",
                    "missing_keywords": ["keyword1", "keyword2", ...],
                    "profile_summary": "Concise evaluation of the candidate's profile summary.",
                    "improvement_tips": ["Bullet point 1", "Bullet point 2", ...],
                    "application_success_rate": "Estimated % score based on market competitiveness"
                }}
                Do NOT include any markdown formatting (like ```json), just return the raw JSON string.
                """
                
                response = model.invoke(input_prompt)
                
                # 3. Parse and Display
                status.write("📊 Generating Dashboard...")
                
                # Clean up response if it contains markdown code blocks
                response_text = response.content.replace("```json", "").replace("```", "").strip()
                data = json.loads(response_text)
                
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

                # --- DASHBOARD UI ---
                st.markdown("---")
                
                # Top Metrics
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.metric(label="Match Percentage", value=f"{data.get('match_percentage', 0)}%")
                with m_col2:
                    st.metric(label="Est. Success Rate", value=f"{data.get('application_success_rate', 'N/A')}")
                
                # Detailed Tabs
                tab1, tab2, tab3 = st.tabs(["🔍 Missing Skills", "💡 Improvements", "📝 Profile Summary"])
                
                with tab1:
                    st.markdown("### ⚠️ Critical Missing Keywords")
                    keywords = data.get("missing_keywords", [])
                    if keywords:
                        for kw in keywords:
                            st.markdown(f"- 🔸 **{kw}**")
                    else:
                        st.success("🎉 No critical missing keywords found!")

                with tab2:
                    st.markdown("### 🚀 Actionable Tips to Improve")
                    tips = data.get("improvement_tips", [])
                    for tip in tips:
                        st.markdown(f"- 📌 {tip}")

                with tab3:
                    st.markdown("### 📝 Profile Assessment")
                    st.info(data.get("profile_summary", "No summary available."))

            except json.JSONDecodeError:
                status.update(label="⚠️ Parsing Error", state="error")
                st.error("The model returned an invalid format. Showing raw output below:")
                st.code(response.content)
            
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"An error occurred: {e}")
    
    elif not uploaded_file:
        st.warning("⚠️ Please upload your resume (PDF) to proceed.")
    elif not jd:
        st.warning("⚠️ Please paste the Job Description.")
