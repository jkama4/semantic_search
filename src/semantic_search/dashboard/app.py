import streamlit as st

from semantic_search import config
from semantic_search.dashboard.components import chat_history, chat_input, sidebar

st.title("Candidate Discovery")

for key in ("status_filter", "city_filter", "category_filter"):
    if key not in st.session_state:
        st.session_state[key] = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "search_results" not in st.session_state:
    st.session_state.search_results = {}

inject_info, rerank = sidebar(config.SEARCH_ENDPOINT)
chat_history()
chat_input(config.LLM_ENDPOINT, inject_info, rerank)
