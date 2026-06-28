import streamlit as st
import os
from pathlib import Path

# Backend imports
from app.pipeline import DocumentPipeline


def show():
    st.title("📤 Upload Document")

    st.write("Upload a PDF or Image for offline AI processing.")

    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "png", "jpg", "jpeg", "txt"]
    )

    if uploaded_file:
        st.success(f"Selected File: {uploaded_file.name}")

        if st.button("🚀 Process Document"):
            # Create uploads folder if missing
            Path("uploads").mkdir(exist_ok=True)

            file_path = os.path.join("uploads", uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            pipeline = DocumentPipeline()

            with st.spinner("Processing document through offline AI pipeline..."):
                res = pipeline.process_file(file_path)

            if res["status"] == "error":
                st.error(f"❌ Processing failed: {res['error']}")
            else:
                doc = res["document"]
                if res["status"] == "cached":
                    st.warning(
                        "⚠️ This document was already processed and retrieved from local cache!"
                    )
                else:
                    st.success("🚀 Document processed and indexed successfully!")

                st.subheader("Extracted Metadata")
                st.json(
                    {
                        "document_type": doc["document_type"],
                        "title": doc["title"],
                        "tags": doc["tags"],
                        "summary": doc["summary"],
                        "metadata": doc["metadata"],
                    }
                )

                st.success(f"Document ID: {doc['id']}")
            st.divider()


st.caption("LocalSeek AI • CPU-First Hackathon • Offline AI • Llama 3.2")
