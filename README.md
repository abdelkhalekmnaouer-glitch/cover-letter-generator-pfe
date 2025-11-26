# AI Cover Letter Generator — Streamlit

This repository contains a Streamlit app that generates tailored cover letters using the OpenAI API and exports them as PDF.

## How to deploy (Streamlit Community Cloud)
1. Create a GitHub repo and push these files.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app** → select the repo, branch and `app.py`.
4. Add your OpenAI key in the Streamlit app settings:
   - Settings → Secrets → add `OPENAI_API_KEY` with value `sk-...`
5. Deploy. The app URL will be like `https://yourname-yourrepo.streamlit.app`.

## Local run (for testing)
1. Install dependencies:
