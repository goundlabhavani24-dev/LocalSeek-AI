import streamlit as st
import os
from pathlib import Path

# Backend imports
from app.pdf_parser import extract_text_from_pdf
from app.ocr_engine import extract_text_from_image
from app.llm_client import OllamaClient
from database.db_manager import DBManager


def show():
    st.title("📤 Upload Document")

    st.write("Upload a PDF or Image for offline AI processing.")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if uploaded_file:

        st.success(f"Selected File: {uploaded_file.name}")

        if st.button("🚀 Process Document"):

            # Create uploads folder if missing
            Path("uploads").mkdir(exist_ok=True)

            file_path = os.path.join("uploads", uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.info("Extracting text...")

            # Extract text
            if uploaded_file.name.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            else:
                text = extract_text_from_image(file_path)

            st.success("Text extraction completed.")

            st.info("Connecting to Local Llama 3.2...")

            llm = OllamaClient()

            metadata = llm.extract_metadata(text)

            db = DBManager()

            doc_id = db.index_document(
                file_path,
                text,
                metadata
            )

            st.success("Document processed successfully!")

            st.subheader("Extracted Metadata")

            st.json(metadata)

            st.success(f"Document ID: {doc_id}")
            st.divider()

st.caption(
    "LocalSeek AI • CPU-First Hackathon • Offline AI • Llama 3.2"
)