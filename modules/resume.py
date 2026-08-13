import fitz
from modules.llm import chat_with_llm


def extract_text_from_pdf(pdf_file):
    try:
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

        text = ""
        for page in pdf:
            text += page.get_text()

        if not text.strip():
            return None

        return text

    except Exception:
        return None


def analyze_resume(text):

    prompt = f"""
You are a Senior Technical Recruiter and ATS (Applicant Tracking System).

Analyze the resume and give structured output.

If NOT a resume, reply ONLY:
NOT_RESUME

----------------------------

1. Resume Score (out of 10)
2. ATS Score (out of 100 + reason)
3. Skills (Technical + Soft Skills)
4. Missing Information
5. Improvements (bullet points)
6. Final Verdict (3–5 lines)

RULES:
- Do not hallucinate information
- Use only resume content
- Keep output structured

RESUME:
{text}
"""

    result = chat_with_llm(prompt)

    if result.strip() == "NOT_RESUME":
        return "❌ Not a valid resume. Please upload a proper resume."

    return result