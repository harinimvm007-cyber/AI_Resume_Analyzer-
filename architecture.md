# Project Workflow

```mermaid
flowchart TD
    A[Upload PDF, DOCX, or TXT resume] --> B[Extract resume text]
    B --> C[Search text for skills from the skill list]
    C --> D[Read job roles and required skills from job_roles.csv]
    D --> E[Compare found skills with each role]
    E --> F[Calculate skill coverage score]
    F --> G[Rank roles and show the top three]
    E --> H[Show missing skills for the selected role]
    H --> I[Suggest learning topics]
    G --> J[Display results in the Streamlit app]
    I --> J
```

## Main parts

- **Streamlit** displays the upload control and results.
- **pypdf** reads text from PDF resumes.
- **python-docx** reads text from DOCX resumes.
- **Keyword matching** finds skills from the app's skill list.
- **job_roles.csv** stores the skills required for each job role.
- **Skill coverage** is the percentage of a role's required skills found in the resume.

The app analyzes the resume for learning guidance. It does not make hiring decisions.