# AI Resume Analyzer and Job Recommender

A beginner student project that reads a sample resume, finds listed skills, compares them with five example job roles, and suggests skills to learn.

## Features

- Accepts PDF, DOCX, and TXT resumes
- Extracts resume text
- Searches for skills from a predefined list
- Calculates a simple skill coverage score for each role
- Shows the top three matching roles
- Lists skills not found for a selected role
- Suggests a basic learning roadmap
- Processes the uploaded file in memory during the session

## Technology

- Python
- Streamlit
- pypdf
- python-docx
- pandas

## Run on Windows

Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py

## Supporting files

- `job_roles.csv` - job roles and the skills each role expects
- `skill_dictionary.csv` - skills the app searches for
- `testing_sheet.csv` - recorded test cases and results
- `architecture.md` - project workflow diagram
- `project_report.md` - short project report
- `test_nlp.txt` and `test_vision.txt` - fictional test resumes
- `empty_test.txt` - empty file used for error handling