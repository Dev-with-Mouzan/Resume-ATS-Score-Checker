# 🚀 Resume ATS Score Checker

**Resume ATS Score Checker** is a powerful, AI-driven application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). Validated against specific job descriptions, it provides deep insights, scoring, and actionable feedback to increase your chances of landing an interview.

## ✨ Features

- **📄 PDF Resume Parsing**: robustly extracts text from PDF resumes using `PyPDF2`.
- **🧠 Advanced AI Analysis**: Utilizes Google's **Gemini Pro** (via LangChain) to understand context, skills, and industry nuances.
- **📊 Smart Scoring System**: Provides a match percentage score (0-100%) based on the job description.
- **🔍 Detailed Insights**: Identifies:
  - **Missing Keywords**: Specific hard skills and keywords found in the JD but missing from the resume.
  - **Profile Summary Check**: Critiques the professional summary for impact and clarity.
  - **Improvement Tips**: Actionable advice to formatting, content, and achievements.
  - **Success Rate Estimation**: Predicts the estimated application success rate.
- **🎨 Modern Dashbaord UI**: Features a premium "Glassmorphism" design with animated backgrounds, tabbed results, and real-time processing feedback.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Model**: Google Gemini (via `langchain-google-genai`)
- **PDF Processing**: `PyPDF2`
- **Environment Management**: `python-dotenv`

## ⚙️ Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.9 or higher
- A Google Cloud API Key with access to Gemini

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Resume Cabin ATS"
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your Google API key:
```ini
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
2. The app will open in your default browser (usually at `http://localhost:8501`).
3. **Paste the Job Description** into the text area.
4. **Upload your Resume** (PDF format).
5. Click **"Analyze Resume Score"**.
6. View your **Match Score**, **Missing Skills**, and **Personalized Tips** in the interactive dashboard.

## 📂 Project Structure

```
Resume Cabin ATS/
├── app.py               # Main application logic and UI
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API Key)
├── examples/            # (Optional) Example resumes/JDs
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
*Built with ❤️ using Python and Generative AI.*
