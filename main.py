
from google.genai import types
import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import pymupdf
from dotenv import load_dotenv
from google import genai


# -------------------- CONFIGURATION --------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Color palette
BG_COLOR = "#101827"
NAVY = "#14213D"
CARD_COLOR = "#1C2B40"
TEAL = "#16A085"
TEAL_HOVER = "#12806A"
TEXT_COLOR = "#F4F7FB"
MUTED_COLOR = "#B8C5D6"
INPUT_COLOR = "#0F1A2B"
BORDER_COLOR = "#30435C"
ERROR_COLOR = "#FCA5A5"


class ResumeAnalyzerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("AI Resume Analyzer")
        self.geometry("1100x800")
        self.minsize(850, 680)
        self.configure(fg_color=BG_COLOR)

        self.resume_path = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # -------------------- HEADER --------------------

        self.header = ctk.CTkFrame(
            self,
            fg_color=NAVY,
            corner_radius=18,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.header.grid(
            row=0, column=0,
            padx=22, pady=(22, 12),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.header,
            text="✦  AI RESUME ANALYZER",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FFFFFF"
        ).pack(pady=(20, 6))

        ctk.CTkLabel(
            self.header,
            text="Smart resume insights powered by Python & Gemini AI",
            font=ctk.CTkFont(size=14),
            text_color="#B8D8D2"
        ).pack(pady=(0, 20))

        # -------------------- RESUME UPLOAD --------------------

        self.upload_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=16,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.upload_frame.grid(
            row=1, column=0,
            padx=22, pady=10,
            sticky="ew"
        )

        ctk.CTkLabel(
            self.upload_frame,
            text="01  |  Upload Resume",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#72E0C2"
        ).pack(anchor="w", padx=18, pady=(16, 10))

        upload_row = ctk.CTkFrame(
            self.upload_frame,
            fg_color="transparent"
        )
        upload_row.pack(fill="x", padx=18, pady=(0, 16))

        self.upload_button = ctk.CTkButton(
            upload_row,
            text="📄  Choose PDF Resume",
            command=self.choose_resume,
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color="#FFFFFF",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.upload_button.pack(side="left")

        self.file_label = ctk.CTkLabel(
            upload_row,
            text="No resume selected",
            text_color=MUTED_COLOR,
            wraplength=450,
            anchor="w"
        )
        self.file_label.pack(
            side="left", padx=15, fill="x", expand=True
        )

        # -------------------- JOB DESCRIPTION --------------------

        self.job_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=16,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.job_frame.grid(
            row=2, column=0,
            padx=22, pady=10,
            sticky="ew"
        )

        ctk.CTkLabel(
            self.job_frame,
            text="02  |  Job Description",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#72E0C2"
        ).pack(anchor="w", padx=18, pady=(16, 10))

        self.job_input = ctk.CTkTextbox(
            self.job_frame,
            height=115,
            wrap="word",
            fg_color=INPUT_COLOR,
            text_color=TEXT_COLOR,
            border_color=BORDER_COLOR,
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.job_input.pack(
            fill="x", padx=18, pady=(0, 16)
        )
        self.job_input.insert(
            "1.0",
            "Paste the job description here..."
        )

        # -------------------- RESULTS --------------------

        self.result_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=16,
            border_width=1,
            border_color=BORDER_COLOR
        )
        self.result_frame.grid(
            row=3, column=0,
            padx=22, pady=10,
            sticky="nsew"
        )
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.result_frame,
            text="03  |  AI Analysis Results",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color="#72E0C2"
        ).grid(
            row=0, column=0,
            padx=18, pady=(16, 10),
            sticky="w"
        )

        self.output = ctk.CTkTextbox(
            self.result_frame,
            wrap="word",
            fg_color=INPUT_COLOR,
            text_color=TEXT_COLOR,
            border_color=BORDER_COLOR,
            border_width=1,
            corner_radius=10,
            font=ctk.CTkFont(size=13)
        )
        self.output.grid(
            row=1, column=0,
            padx=18, pady=(0, 18),
            sticky="nsew"
        )
        self.output.insert(
            "1.0",
            "Welcome!\n\n"
            "Upload a PDF resume, paste a job description, "
            "and click Analyze Resume to view AI-generated insights.\n\n"
            "Your results will appear here."
        )
        self.output.configure(state="disabled")

        # -------------------- FOOTER --------------------

        self.footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.footer.grid(
            row=4, column=0,
            padx=22, pady=(6, 22),
            sticky="ew"
        )
        self.footer.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            self.footer,
            text="●  Ready to analyze",
            text_color="#72E0C2",
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(
            row=0, column=0,
            sticky="w", padx=(0, 10)
        )

        self.analyze_button = ctk.CTkButton(
            self.footer,
            text="✦  Analyze Resume",
            command=self.start_analysis,
            fg_color=TEAL,
            hover_color=TEAL_HOVER,
            text_color="#FFFFFF",
            height=43,
            width=180,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.analyze_button.grid(
            row=0, column=1, padx=5
        )

        self.clear_button = ctk.CTkButton(
            self.footer,
            text="Clear",
            command=self.clear_results,
            fg_color="#34445B",
            hover_color="#435671",
            text_color="#FFFFFF",
            height=43,
            width=90,
            corner_radius=10
        )
        self.clear_button.grid(
            row=0, column=2, padx=5
        )

    # -------------------- FILE UPLOAD --------------------

    def choose_resume(self):
        path = filedialog.askopenfilename(
            title="Select your resume",
            filetypes=[("PDF files", "*.pdf")]
        )

        if path:
            self.resume_path = path
            self.file_label.configure(
                text=f"✓  {Path(path).name}",
                text_color="#72E0C2"
            )
            self.status_label.configure(
                text="●  Resume selected",
                text_color="#72E0C2"
            )

    # -------------------- PDF TEXT EXTRACTION --------------------

    def read_pdf(self, path):
        with pymupdf.open(path) as document:
            text = "\n".join(
                page.get_text() for page in document
            )

        if not text.strip():
            raise ValueError(
                "No readable text found in this PDF. "
                "Try a text-based PDF instead of a scanned image."
            )

        return text

    # -------------------- START ANALYSIS --------------------

    def start_analysis(self):
        if not API_KEY:
            self.show_result(
                "API KEY NOT FOUND\n\n"
                "1. Create a .env file beside main.py.\n"
                "2. Add GEMINI_API_KEY=your_actual_key\n"
                "3. Save the file and restart the application."
            )
            return

        if not self.resume_path:
            self.show_result(
                "Please upload a PDF resume first."
            )
            return

        job_description = self.job_input.get(
            "1.0", "end"
        ).strip()

        if (
            not job_description
            or job_description == "Paste the job description here..."
        ):
            self.show_result(
                "Please paste a job description first."
            )
            return

        self.analyze_button.configure(state="disabled")
        self.status_label.configure(
            text="●  Analyzing... Please wait",
            text_color="#F6C66B"
        )
        self.show_result(
            "Your resume is being analyzed by AI.\n\n"
            "Please wait while we prepare your report..."
        )

        threading.Thread(
            target=self.run_analysis,
            args=(self.resume_path, job_description),
            daemon=True
        ).start()

    # -------------------- GEMINI ANALYSIS --------------------

    def run_analysis(self, resume_path, job_description):
        try:
            resume_text = self.read_pdf(resume_path)
            resume_text = resume_text[:18000]
            job_description = job_description[:8000]

            prompt = f"""
You are a helpful resume review assistant.

Analyze the resume against the job description.
Use only information explicitly supported by the resume.
Do not invent qualifications, skills, employers or dates.

Return a clear report with these sections:

1. RESUME SUMMARY
Briefly summarize the candidate's background.

2. RELEVANT SKILLS
List skills supported by the resume that match the role.

3. POSSIBLE SKILL GAPS
Identify requirements not clearly demonstrated.
Do not assume that an unlisted skill is absent.

4. EXPERIENCE AND EDUCATION
Explain the relevance of stated experience and education.

5. STRENGTHS
List evidence-based strengths.

6. IMPROVEMENT SUGGESTIONS
Provide specific, honest resume improvement suggestions.

7. KEYWORDS TO CONSIDER
Suggest relevant keywords only if truthful for the candidate.

8. OVERALL MATCH
Give a qualitative assessment. Any numerical estimate
must be described as approximate and not a validated score.

JOB DESCRIPTION:
{job_description}

RESUME TEXT:
{resume_text}
"""

            # Gemini client with retry settings
            client = genai.Client(
                api_key=API_KEY,
                http_options=types.HttpOptions(
                    retry_options=types.HttpRetryOptions(
                        attempts=5,
                        initial_delay=2,
                        max_delay=30,
                        http_status_codes=[
                            408, 429, 500, 502, 503, 504
                        ],
                    )
                ),
            )

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )

            result = response.text

            if not result:
                result = (
                    "The API returned no text. Please try again."
                )

            self.after(
                0, self.finish_analysis, result, None
            )

        except Exception as exc:
            error_message = (
                f"{type(exc).__name__}: {exc}"
            )
            self.after(
                0,
                self.finish_analysis,
                None,
                error_message
            )

    # -------------------- DISPLAY RESULTS --------------------

    def finish_analysis(self, result, error):
        self.analyze_button.configure(state="normal")

        if error:
            self.status_label.configure(
                text="●  Analysis failed",
                text_color=ERROR_COLOR
            )
            self.show_result(
                "SOMETHING WENT WRONG\n\n"
                + error
                + "\n\nCheck your API key, internet connection, "
                  "model availability and API usage limits."
            )
        else:
            self.status_label.configure(
                text="●  Analysis completed",
                text_color="#72E0C2"
            )
            self.show_result(result)

    def show_result(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    # -------------------- CLEAR --------------------

    def clear_results(self):
        self.resume_path = None
        self.file_label.configure(
            text="No resume selected",
            text_color=MUTED_COLOR
        )
        self.job_input.delete("1.0", "end")
        self.show_result(
            "Welcome!\n\n"
            "Upload a PDF resume and paste a job description "
            "to begin a new analysis."
        )
        self.status_label.configure(
            text="●  Ready to analyze",
            text_color="#72E0C2"
        )


if __name__ == "__main__":
    app = ResumeAnalyzerApp()
    app.mainloop()

