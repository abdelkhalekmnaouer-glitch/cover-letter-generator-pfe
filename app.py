import streamlit as st
from openai import OpenAI

# Create client using the API key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

prompt = "Write a short professional cover letter for a junior engineer."

# New API call
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional cover letter writer."},
        {"role": "user", "content": prompt}
    ]
)

cover_letter = response.choices[0].message.content
st.text_area("Generated Cover Letter", cover_letter, height=300)
