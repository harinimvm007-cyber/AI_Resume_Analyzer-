# AI Resume Analyzer and Job Recommendation System

## Abstract

This project is an educational application that compares skills listed in a resume with skills required by example job roles. It accepts PDF, DOCX, and TXT files, extracts their text, identifies skills from a predefined list, calculates a skill coverage score, and displays role recommendations and learning suggestions.

## Problem

Students may be unsure which skills their resumes show for different career paths. This project provides a simple way to compare a resume with example role requirements and identify skills to learn next.

## Objectives

- Read text from PDF, DOCX, and TXT resumes.
- Identify job related skills using keyword matching.
- Compare resume skills with at least five job roles.
- Calculate a match score and rank the roles.
- Show missing skills for a selected role.
- Suggest a basic learning roadmap.

## Tools Used

- Python
- Streamlit for the web interface
- pypdf for reading PDF text
- python-docx for reading DOCX text
- pandas for reading the job role dataset

## How It Works

The user uploads a resume. The app extracts its text and searches for skills from a predefined list. It reads job roles and their required skills from `job_roles.csv`. For each role, it calculates:

**Match score = (required skills found / total required skills) × 100**

The app ranks roles by score, displays the top three, and shows missing skills and learning suggestions for a selected role.

## Testing

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Sample student resume | Relevant roles and skill gaps appear | Data Analyst 71%; Junior Machine Learning Engineer 71%; Python Developer 57%. Data Analyst gaps: Power BI and statistics. | Pass |
| NLP focused resume | NLP Engineer ranks highest | NLP Engineer ranked highest. | Pass |
| Computer vision focused resume | Computer Vision Engineer ranks highest | Computer Vision Engineer 100%; NLP Engineer 33%; Data Analyst 14%. | Pass |
| Empty text file | App displays an error instead of crashing | App displayed: “I couldn't read text from this file.” | Pass |

## Responsible Use and Limitations

This application is for learning and career guidance. Its score is a keyword coverage estimate, not a hiring decision or a measure of a person's full ability. It may miss skills described using different words, and a missing keyword does not prove that someone lacks a skill. The current version uses keyword matching; it does not use Ollama or another AI model. Use sample resumes with personal details removed.

## Future Improvements

Possible improvements include expanding the skill dictionary, supporting scanned resumes with OCR, adding optional AI generated feedback, and deploying the app online.

## Conclusion

The project demonstrates resume text extraction, skill matching, role ranking, skill gap identification, and a learning roadmap in a Streamlit application.