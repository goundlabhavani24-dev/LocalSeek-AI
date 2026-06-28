# ruff: noqa: E402
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

st.set_page_config(
    page_title="LocalSeek AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.png"

st.sidebar.image(str(logo_path), width=90)

st.sidebar.title("LocalSeek AI")

st.sidebar.markdown(
    """
### Offline Document Intelligence

AI-powered document indexing
running completely offline.
"""
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation", ["🏠 Home", "📤 Upload", "🔍 Search", "📊 Dashboard"]
)

if page == "🏠 Home":
    from views.home import show

    show()

elif page == "📤 Upload":
    from views.upload import show

    show()

elif page == "🔍 Search":
    from views.search import show

    show()

elif page == "📊 Dashboard":
    from views.dashboard import show

    show()
