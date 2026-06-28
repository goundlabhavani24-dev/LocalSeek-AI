import streamlit as st
from database.db_manager import DBManager


def show():
    st.title("📊 Dashboard")

    db = DBManager()

    documents = db.search_documents("")

    total = len(documents)

    notes = len([d for d in documents if d["document_type"] == "Notes"])

    invoices = len([d for d in documents if d["document_type"] == "Invoice"])

    medical = len([d for d in documents if d["document_type"] == "Medical"])

    certificates = len([d for d in documents if d["document_type"] == "Certificate"])

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📄 Documents", total)
    c2.metric("📝 Notes", notes)
    c3.metric("🧾 Invoices", invoices)
    c4.metric("🏥 Medical", medical)
    c5.metric("🎓 Certificates", certificates)

    st.markdown("---")

    st.subheader("Recent Documents")

    if total == 0:
        st.info("No documents indexed yet.")

    else:
        for doc in documents:
            st.write(f"**{doc['title']}** • {doc['document_type']}")
            st.divider()


st.caption("LocalSeek AI • CPU-First Hackathon • Offline AI • Llama 3.2")
