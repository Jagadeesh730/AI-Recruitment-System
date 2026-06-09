import pdfplumber

SKILLS = [
    "python",
    "java",
    "sql",
    "django",
    "machine learning",
    "html",
    "css",
    "javascript",
    "react",
    "mysql",
    "flask"
]

def extract_skills(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:
            text += page.extract_text() or ""

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills