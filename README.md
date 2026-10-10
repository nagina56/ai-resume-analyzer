#  AI Resume Analyzer

An AI-powered desktop application built with Python and Google Gemini AI to analyze resumes against job descriptions and provide personalized feedback.

##  About the Project

The AI Resume Analyzer helps users understand how well their resume aligns with a specific job description. It extracts text from PDF resumes and uses Gemini AI to identify relevant skills, possible skill gaps, strengths, and opportunities for improvement.

The application features a modern dark-themed graphical user interface built with CustomTkinter.

##  Features

*  Upload resumes in PDF format
*  Paste a job description for comparison
*  Generate AI-powered resume analysis using Google Gemini
*  Identify relevant skills and possible skill gaps
*  Review experience and education relevance
*  Receive resume improvement suggestions
*  Suggest relevant keywords based on the job description
*  Get an overall qualitative match assessment
*  Modern dark-themed GUI with a teal color palette
*  Basic error handling for API and PDF issues

##  Technologies Used

* **Python** — Core programming language
* **CustomTkinter** — Graphical user interface
* **Google Gemini API** — AI-powered resume analysis
* **PyMuPDF** — PDF text extraction
* **python-dotenv** — Secure environment variable management
* **Threading** — Run analysis without freezing the interface

##  Project Structure

```text
ai-resume-analyzer/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The `.venv/` virtual environment folder is created locally and should not be uploaded to GitHub.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project Folder

```bash
cd ai-resume-analyzer
```

### 3. Create a Virtual Environment

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Get a Gemini API Key

Create an API key through [Google AI Studio](https://aistudio.google.com/apikey).

Add your key to the `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_api_key
```

**Important:** Never publish your real API key or commit your `.env` file to GitHub.

### 6. Run the Application

```bash
python main.py
```

## 📦 Requirements

Create a `requirements.txt` file containing:

```text
customtkinter
google-genai
python-dotenv
pymupdf
```

##  How to Use

1. Launch the application.
2. Click **Choose PDF Resume** to upload a resume.
3. Paste the relevant job description into the text box.
4. Click **Analyze Resume**.
5. Review the generated analysis and improvement suggestions.
6. Use the **Clear** button to start another analysis.

##  Screenshots

Add screenshots of your application here after running and testing it successfully.

```markdown
![AI Resume Analyzer GUI](screenshots/app-screenshot.png)
```

To use this screenshot, create a `screenshots` folder in your repository and add your image as `app-screenshot.png`.

## 🔐 Security and Privacy

* Store your Gemini API key in a local `.env` file.
* Keep `.env` excluded from Git using `.gitignore`.
* Avoid uploading resumes containing real personal information to public repositories.
* Only analyze resumes you have permission to process.
* Review AI-generated feedback before making career decisions.

##  Limitations

* Requires an internet connection and a valid Gemini API key.
* API availability, model access, quotas, and usage limits may vary.
* Scanned PDFs without extractable text may not work.
* AI-generated feedback may be incomplete or inaccurate.
* Resume matching is an informational aid, not a validated hiring score.

##  Future Improvements

* Export analysis reports to PDF.
* Add a resume scorecard with transparent criteria.
* Support additional document formats.
* Improve the interface with progress indicators.
* Add resume section detection and more detailed keyword comparisons.

##  Author

**Nagina Azhar**

Python Learner | AI & Automation Enthusiast

Building projects and exploring AI one step at a time.



