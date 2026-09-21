import streamlit as st
from pypdf import PdfReader
import requests

st.title("🔎 Secure Corporate Data Audit App")
st.caption("Built for Data Specialist & Assistant Manager Paths")

# 1. Upload Box
uploaded_file = st.file_uploader("Upload a Company PDF Report", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading PDF and running AI..."):
        # Extract text from the first two pages of the PDF
        reader = PdfReader(uploaded_file)
        raw_text = "".join([page.extract_text() for page in reader.pages[:2]])
        
        # 2. Get the secret key safely from Streamlit's hidden cloud settings
        hf_token = st.secrets["HF_TOKEN"]
        
        # 3. Ask the free AI to read the text
        API_URL = "https://huggingface.co"
        headers = {"Authorization": f"Bearer {hf_token}"}
        prompt = f"<s>[INST] Extract the Company Name and Reporting Year from this text. Note if anything is missing: {raw_text[:1500]} [/INST]"
        
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        try:
            result = response.json()['generated_text']
            clean_result = result.split("[/INST]")[-1]
            
            # 4. Show the results on the screen
            st.subheader("📋 Audit Results")
            st.info(clean_result)
            st.success("✅ Data quality check complete!")
        except Exception as e:
            st.error("Error. Please check your secret key settings.")
