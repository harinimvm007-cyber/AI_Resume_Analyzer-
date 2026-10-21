import io
import re

import pandas as pd
import streamlit as st
from docx import Document
from pypdf import PdfReader


# A beginner-friendly skill list. The app searches resumes for these terms.
SKILLS = [
    "python", "java", "c++", "c#", ".net", "javascript", "html", "css",
    "sql", "excel", "pandas", "numpy", "matplotlib", "power bi",
    "machine learning", "scikit-learn", "deep learning", "nlp",
    "transformers", "hugging face", "computer vision", "opencv", "cnn",
    "yolo", "fastapi", "flask", "django", "streamlit", "docker",
    "git", "github", "aws", "azure", "linux", "statistics"
]

# Each role has a small set of skills used for comparison.
JOB_ROLES = {
    "Data Analyst": [
        "python", "sql", "excel", "pandas", "numpy", "power bi", "statistics"
    ],
    "Junior Machine Learning Engineer": [
        "python", "machine learning", "scikit-learn", "pandas",
        "numpy", "fastapi", "docker"
    ],
    "Python Developer": [
        "python", "sql", "git", "github", "fastapi", "flask", "django"
    ],
    "NLP Engineer": [
        "python", "nlp", "transformers", "hugging face",
        "machine learning", "deep learning"
    ],
    "Computer Vision Engineer": [
        "python", "computer vision", "opencv", "cnn",
        "yolo", "deep learning"
    ],
}

# Simple suggestions for learning skills that are not found.
LEARNING_TOPICS = {
    "python": "Python basics and small practice programs",
    "sql": "SQL queries: SELECT, JOIN, GROUP BY",
    "excel": "Excel formulas, pivot tables, and charts",
    "pandas": "Pandas DataFrames and data cleaning",
    "numpy": "NumPy arrays and basic calculations",
    "power bi": "Power BI dashboards and visualizations",
    "statistics": "Descriptive statistics and probability",
    "machine learning": "Introductory machine learning with scikit-learn",
    "scikit-learn": "Training and evaluating models with scikit-learn",
    "fastapi": "Building a small API with FastAPI",
    "docker": "Docker images and containers",
    "nlp": "Text cleaning and natural language processing basics",
    "transformers": "Transformer models for text",
    "hugging face": "Using Hugging Face models and datasets",
    "deep learning": "Neural network fundamentals",
    "computer vision": "Image processing and computer vision basics",
    "opencv": "Image reading and processing with OpenCV",
    "cnn": "Convolutional neural network basics",
    "yolo": "Object detection with YOLO",
    "git": "Git basics: commit, branch, and push",
    "github": "Repositories and README files on GitHub",
    "flask": "Building a small web app with Flask",
    "django": "Django models, views, and URLs",
    "matplotlib": "Creating charts with Matplotlib",
    "java": "Java programming fundamentals",
    "javascript": "JavaScript fundamentals",
    "html": "HTML page structure",
    "css": "CSS styling basics",
    "c++": "C++ programming fundamentals",
    "c#": "C# programming fundamentals",
    ".net": ".NET application basics",
    "aws": "Cloud fundamentals with AWS",
    "azure": "Cloud fundamentals with Azure",
    "linux": "Linux terminal basics",
}


def extract_text(uploaded_file):
    """Read text from an uploaded PDF, DOCX, or TXT file."""
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        pdf = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

    if file_name.endswith(".docx"):
        document = Document(io.BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    if file_name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    return ""


def find_skills(text):
    """Return skills from our list that appear in the resume text."""
    text = text.lower()
    found = []

    for skill in SKILLS:
        # Match whole words, while allowing common symbols such as C++ and C#.
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(found)


def compare_roles(found_skills):
    """Calculate the percent of each role's required skills that were found."""
    results = []

    for role, required_skills in JOB_ROLES.items():
        matched = [skill for skill in required_skills if skill in found_skills]
        missing = [skill for skill in required_skills if skill not in found_skills]
        score = round(100 * len(matched) / len(required_skills))

        results.append({
            "Job role": role,
            "Match score": score,
            "Matched skills": ", ".join(matched) if matched else "None found",
            "Missing skills": missing,
        })

    return sorted(results, key=lambda item: item["Match score"], reverse=True)


job_data = pd.read_csv("job_roles.csv")
JOB_ROLES = {
    row["role"]: row["required_skills"].split("|")
    for _, row in job_data.iterrows()
}
skill_data = pd.read_csv("skill_dictionary.csv")
SKILLS = skill_data["skill"].astype(str).str.lower().tolist()
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI Resume Analyzer and Job Recommender")
st.write(
    "Upload a sample resume to see detected skills, job matches, "
    "and learning suggestions."
)
st.caption(
    "This is an educational estimate based on listed skills, "
    "not a hiring decision."
)

uploaded_file = st.file_uploader(
    "Choose a resume file",
    type=["pdf", "docx", "txt"],
    help="For this demo, use a sample resume with personal details removed."
)

if uploaded_file is not None:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("This file is larger than 10 MB. Please choose a smaller file.")
    else:
        resume_text = extract_text(uploaded_file)

        if not resume_text.strip():
            st.error(
                "I couldn't read text from this file. "
                "Try a text-based PDF, DOCX, or TXT file."
            )
        else:
            found_skills = find_skills(resume_text)
            results = compare_roles(found_skills)

            st.subheader("Skills found in the resume")
            if found_skills:
                st.write(", ".join(found_skills))
            else:
                st.write("No skills from the current skill list were found.")

            st.subheader("Top 3 recommended roles")
            top_three = results[:3]
            chart_data = pd.DataFrame({
                "Match score (%)": [item["Match score"] for item in top_three]
            }, index=[item["Job role"] for item in top_three])
            st.bar_chart(chart_data)

            for item in top_three:
                st.markdown(
                    f"**{item['Job role']} — {item['Match score']}% match**"
                )
                st.write(f"Skills found: {item['Matched skills']}")

            st.subheader("Choose a target role to see skill gaps")
            target_role = st.selectbox("Target role", list(JOB_ROLES.keys()))
            selected = next(
                item for item in results if item["Job role"] == target_role
            )

            st.write(f"**Current match score: {selected['Match score']}%**")
            missing_skills = selected["Missing skills"]

            if missing_skills:
                st.write("Skills not found in this resume:")
                st.write(", ".join(missing_skills))

                st.write("**Starter learning roadmap:**")
                for week, skill in enumerate(missing_skills[:4], start=1):
                    topic = LEARNING_TOPICS.get(skill, f"Learn {skill}")
                    st.write(f"- Week {week}: {topic}")
            else:
                st.success("All listed skills for this role were found.")

            with st.expander("View extracted resume text"):
                st.text(resume_text[:5000])

            st.caption(
                "The app processes the uploaded file in memory for this session. "
                "It does not save the resume to a database."
            )