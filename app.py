import streamlit as st
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# --- Streamlit App ---
st.title("AI Cover Letter Generator (PDF)")

st.write("Enter your personal info and paste the job offer text.")

# User Inputs
name = st.text_input("Your name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")
job_offer = st.text_area("Paste the job offer here")
your_info = st.text_area("Describe your experience or paste your CV")

# OpenAI API Key (from Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("Generate Cover Letter"):

    prompt = f"""
Write a professional cover letter based on the following information.

PERSONAL INFO:
Name: {name}
Email: {email}
Phone: {phone}
Address: {address}

My Experience:
{your_info}

Job Offer:
{job_offer}

The cover letter should be well structured, polite, and in good French.
Do NOT include placeholder text.
"""

    # --- New OpenAI 1.x API call ---
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # updated model name
        messages=[
            {"role": "system", "content": "You are a professional cover letter writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )

    cover_letter = response.choices[0].message.content  # updated attribute

    st.success("Cover Letter Generated!")
    st.text_area("Generated Cover Letter", cover_letter, height=300)

    # Generate PDF
    pdf_file = "cover_letter.pdf"
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_file)
    story = [Paragraph(cover_letter.replace("\n", "<br/>"), styles["Normal"])]
    doc.build(story)

    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name="cover_letter.pdf")
