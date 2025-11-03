# frontend/streamlit_app.py
import streamlit as st
import requests
import json
from pathlib import Path

BACKEND_PARSE_URL = st.secrets.get("BACKEND_PARSE_URL", "http://localhost:8000/parse")

st.set_page_config(page_title="Financial Agent Demo", layout="wide")
st.title("Intelligent Financial Agent — Demo")

uploaded = st.file_uploader("Upload financial PDF (10-K / Loan doc / Invoice)", type=["pdf"])
if uploaded:
    files = {"file": (uploaded.name, uploaded.getvalue())}
    with st.spinner("Uploading and parsing via ADE..."):
        resp = requests.post(BACKEND_PARSE_URL, files=files)
    st.write("ADE parse response:")
    st.json(resp.json())

st.markdown("---")
st.header("Ask a question")
q = st.text_input("Enter a financial question (e.g., 'Compute debt-to-equity from latest quarter')", "")
if st.button("Ask") and q:
    # call agent endpoint - for now call a local stub or LangChain service
    AGENT_URL = st.secrets.get("AGENT_URL", "http://localhost:8000/query")
    r = requests.post(AGENT_URL, json={"query": q})
    st.subheader("Answer")
    st.write(r.json().get("answer"))
    st.subheader("Sources / Evidence")
    st.json(r.json().get("sources", {}))
