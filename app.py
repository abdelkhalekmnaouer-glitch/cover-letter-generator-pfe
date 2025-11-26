"""
Streamlit AI Cover Letter Generator (GitHub-ready)

How it works:
- You paste your personal info and the job posting (or upload files).
- App calls OpenAI (requires OPENAI_API_KEY set as a secret on Streamlit Cloud).
- Generated letter is shown and can be downloaded as a PDF.

Requirements: see requirements.txt
"""
import os
import textwrap
from io import BytesIO

import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import openai

# ---------- Config ----------
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")

SYSTEM_PROMPT = (
    "You are a professional career coach and technical writer. "
    "Write a single-page, professional cover letter tailored to the job posting and the candidate's info. "
    "Be concise (approx 250-400 words). Keep a formal tone. "
    "If the candidate provided an availability date, mention it in the body. "
    "Return only the cover letter text (no extra commentary)."
)

PROMPT_TEMPLATE = """
Personal information:
{personal}

Job posting:
{job}

Instructions:
- Mention 2-3 relevant skills/experiences matching the job posting.
- Use a formal tone and include a short closing (request an interview).
- Keep it one page.
- Return only the letter text.
"""

# ---------- Helpers ----------
def call_openai(personal_text: str, job_text: str, model: str = "gpt-4o-mini", max_tokens: int = 850):
    """
    Call OpenAI ChatCompletion. Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment. On Streamlit Cloud add it under Settings → Secrets.")
    openai.api_key = api_key

    prompt = PROMPT_TEMPLATE.format(personal=personal_text.strip(), job=job_text.strip())
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.15,
        max_tokens=max_tokens,
    )
    text = resp["choices"][0]["message"]["content"].strip()
    return text

def letter_to_pdf_bytes(letter_text: str, author_name: str = "Candidate") -> BytesIO:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    margin = 50
    x = margin
    y = h - margin
    c.setFont("Helvetica", 11)
    lines = letter_text.splitlines()
    for line in lines:
        wrapped = textwrap.wrap(line, 90)
        for sub in wrapped:
            y -= 14
            if y < margin + 40:
                c.showPage()
                y = h - margin
                c.setFont("Helvetica", 11)
            c.drawString(x, y, sub)
    c.setAuthor(author_name)
    c.save()
    buf.seek(0)
    return buf

# ---------- UI ----------
st.title("AI Cover Letter Generator")
st.markdown(
    """
Use this app on your phone or desktop. Paste your personal info and the job advertisement, then tap **Generate**.
**Security:** Don’t paste very sensitive data. Store your OpenAI key as a secret on Streamlit Cloud.
"""
)

with st.expander("Example usage / tips (tap to expand)"):
    st.write(
        "- For best results paste a short 3–6 bullet CV and 2–3 lines explaining your key strengths.\n"
        "- Paste the job posting exactly (responsibilities, required skills). The AI matches words from the ad.\n"
        "- If you want the letter in French, provide the inputs in French or add a note 'Write in French'."
    )

col1, col2 = st.columns([2, 1])

with col1:
    personal = st.text_area("Your personal info (name, contact, short bullets about experience/skills)", height=180)
    job = st.text_area("Job offer text (paste the full ad)", height=260)
    availability = st.text_input("Availability (optional, e.g. 'from March 2026')")

with col2:
    st.markdown("**Optional uploads**")
    uploaded_personal = st.file_uploader("Upload personal info (txt)", type=["txt"])
    uploaded_job = st.file_uploader("Upload job text (txt)", type=["txt"])
    st.markdown("---")
    st.markdown("**Model settings**")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    st.caption("Lower temperature = more deterministic results")

if uploaded_personal is not None and not personal:
    personal = uploaded_personal.getvalue().decode("utf-8")

if uploaded_job is not None and not job:
    job = uploaded_job.getvalue().decode("utf-8")

generate_clicked = st.button("Generate cover letter")

if generate_clicked:
    if not personal.strip():
        st.error("Please add your personal info.")
    elif not job.strip():
        st.error("Please paste the job posting.")
    else:
        prompt_personal = personal
        if availability.strip():
            prompt_personal += f"\nAvailability: {availability.strip()}"
        try:
            with st.spinner("Generating letter with AI..."):
                letter = call_openai(prompt_personal, job, model=model)
        except Exception as e:
            st.error(f"OpenAI call failed: {e}")
            letter = None

        if letter:
            st.success("Generated — preview below")
            st.subheader("Preview")
            st.text_area("Cover letter", value=letter, height=320)

            pdf_bytes = letter_to_pdf_bytes(letter, author_name=personal.splitlines()[0] if personal else "Candidate")
            st.download_button("Download as PDF", data=pdf_bytes, file_name="cover_letter.pdf", mime="application/pdf")

# Small footer
st.markdown("---")
st.caption("Made with Streamlit · Keep your API key private. If using Streamlit Community Cloud add OPENAI_API_KEY under Settings → Secrets.")
