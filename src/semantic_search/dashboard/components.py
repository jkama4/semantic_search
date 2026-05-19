from typing import Tuple, List

import streamlit as st
import requests

from typing import Tuple

from semantic_search.dashboard.utils import parse_profile_sections, relevance_badge


def sidebar(
    search_endpoint: str
) -> Tuple[bool, bool]:

    with st.sidebar:
        inject_info = st.toggle(label="Search candidate database", value=True)
        rerank = st.toggle(label="Rerank results with LLM", value=False)

        st.divider()
        _filters()
        st.divider()
        _reindex_action(search_endpoint)

    return inject_info, rerank


def _filters() -> None:

    st.subheader("Filters")
    st.caption(
        "Narrow results before the search runs. All fields require an exact match."
    )

    st.text_input(
        "Status",
        placeholder="e.g. Freelancer, Employed, New",
        key="status_filter",
    )
    st.text_input(
        "City",
        placeholder="e.g. Amsterdam, Utrecht",
        key="city_filter",
    )
    st.text_input(
        "Category — the candidate's IT discipline",
        placeholder="e.g. Cloud Engineering, DevOps, Data Science",
        key="category_filter",
        help=(
            "Category is the candidate's primary IT specialisation as recorded in "
            "the system — for example: Software Engineering, Cloud Engineering, "
            "DevOps, Data Science, Cybersecurity, IT Management, etc."
        ),
    )

    def _clear_filters():
        st.session_state["status_filter"] = ""
        st.session_state["city_filter"] = ""
        st.session_state["category_filter"] = ""

    st.button(
        label="Reset filters",
        use_container_width=True,
        on_click=_clear_filters
    )


def _reindex_action(
    search_endpoint: str
) -> None:

    if st.button(label="Re-index candidates", use_container_width=True):
        with st.spinner("Indexing candidates from database..."):
            index_url = search_endpoint.replace("/search", "/index")
            r: requests.Response = requests.post(url=index_url)
            if r.status_code == 200:
                st.success(f"Indexed {r.json()['indexed']} candidates.")
            else:
                st.error(f"Indexing failed: {r.status_code}")


def candidate_list(
    hits: List
) -> None:

    label: str = f"Retrieved candidates ({len(hits)})"
    with st.expander(label, expanded=False):
        for hit in hits:
            _candidate_card(hit)


def _candidate_card(
    hit: dict
) -> None:

    with st.container(border=True):
        name     = hit.get("name") or "Unknown"
        status   = hit.get("status") or "—"
        city     = hit.get("city") or "—"
        category = hit.get("category") or "—"
        distance = hit.get("vector_distance", 0.0)
        text     = hit.get("search_text", "")

        col_meta, col_score = st.columns([4, 1])
        with col_meta:
            st.markdown(f"**{name}**")
            st.caption(f"{category} · {city} · {status}")
        with col_score:
            badge = relevance_badge(distance)
            st.markdown(
                body=f"<div style='text-align:right; font-size:0.75rem; " # Determined by Claude, of course
                f"padding-top:4px'>{badge} {distance:.2f}</div>",
                unsafe_allow_html=True,
            )

        _candidate_profile(text)


def _candidate_profile(
    text: str
) -> None:

    profile = parse_profile_sections(text)

    with st.expander("View full profile"):
        if profile["education"]:
            st.markdown("**Education**")
            for edu in profile["education"]:
                st.markdown(f"- {edu}")

        if profile["work_experience"]:
            st.markdown("**Work Experience**")
            for role in profile["work_experience"]:
                st.markdown(f"- **{role['title']}**")
                for detail in role["details"]:
                    st.markdown(f"  _{detail}_")


def chat_history() -> None:
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        if idx in st.session_state.search_results:
            candidate_list(st.session_state.search_results[idx])


def chat_input(
    llm_endpoint: str,
    inject_info: bool,
    rerank: bool
) -> None:

    if prompt := st.chat_input("Describe the candidate you're looking for..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = requests.post(
            url=llm_endpoint,
            json={
                "history": st.session_state.messages,
                "inject_info": inject_info,
                "rerank": rerank,
            },
        )

        if response.status_code != 200:
            st.error(f"API error: {response.status_code} - {response.text}")
        else:
            data: List[Dict] = response.json()
            assistant_message: str = data["response"]
            candidates: List = data.get("candidates", [])
            assistant_idx: int = len(st.session_state.messages)

            with st.chat_message("assistant"):
                st.markdown(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

            if candidates:
                st.session_state.search_results[assistant_idx] = candidates
                candidate_list(candidates)
