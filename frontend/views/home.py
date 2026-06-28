import streamlit as st


def show():
    st.title("🔍 LocalSeek AI")

    st.subheader("Offline AI-Powered Document Intelligence")

    st.write(
        """
Transform unstructured PDFs and images into structured,
searchable knowledge using completely offline AI.

✔ CPU Optimized
✔ Offline First
✔ Local Llama 3.2
✔ SQLite Database
✔ Privacy Focused
"""
    )

    st.divider()

    from database.db_manager import DBManager

    db = DBManager()
    total_docs = len(db.search_documents(""))

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📄 Documents", str(total_docs))
    c2.metric("🤖 AI Model", "Llama 3.2")
    c3.metric("💾 Database", "SQLite")
    c4.metric("🌐 Mode", "Offline")

    st.divider()

    st.subheader("AI Workflow")

    st.info("""
📄 Upload Document

⬇

📝 Extract Text (OCR / PDF)

⬇

🤖 Local Llama 3.2

⬇

📊 Generate Metadata

⬇

💾 Store in SQLite

⬇

🔍 Instant Search
""")
    st.divider()


st.caption("LocalSeek AI • CPU-First Hackathon • Offline AI • Llama 3.2")
