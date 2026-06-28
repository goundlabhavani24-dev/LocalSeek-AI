import streamlit as st
from database.db_manager import DBManager


def show():

    st.title("🔍 Search Documents")

    st.write("Search documents stored in the local database.")

    db = DBManager()

    query = st.text_input(
        "Search by title, tags, summary or document type"
    )

    if st.button("🔍 Search"):

        results = db.search_documents(query)

        if not results:
            st.warning("No documents found.")
            return

        st.success(f"{len(results)} document(s) found")

        for doc in results:

            with st.container():

                st.subheader(doc["title"])

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Type:** {doc['document_type']}")

                with col2:
                    st.write(f"**ID:** {doc['id']}")

                st.write(f"**Summary:** {doc['summary']}")

                st.write("**Tags:**")
                st.write(", ".join(doc["tags"]))

                st.divider()