"""
LinkBrain - app.py (Simplified UI - Fully Connected)
A clean, minimal, single-page Streamlit frontend for an AI-powered RAG system.
"""

import streamlit as st
import database.db_queries as db_helper


from pipelines.ingest_pipeline import ingest_url
from retrieval.ask_llm import answer_query


# ------------------------------------------------------------------------

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="LinkBrain",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# MINIMAL CSS: Hide Streamlit's default chrome for a cleaner app feel.
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# 2. SESSION STATE INITIALIZATION
if "active_view" not in st.session_state:
    st.session_state.active_view = "add"


# 3. SIDEBAR
with st.sidebar:
    st.markdown("## 🧠 LinkBrain")
    st.markdown("**Personal Knowledge Base**")
    st.write("Save URLs. Build knowledge. Ask questions later.")
    
    st.divider()
    
    st.markdown("### Important Points")
    st.markdown("- AI-powered RAG")
    st.markdown("- Semantic Search")
    st.markdown("- Vector Retrieval")
    st.markdown("- Knowledge Base")
    
    st.divider()
    st.caption("Version 1.0")


# 4. MAIN HEADER
st.title("🧠 LinkBrain")
st.subheader("Save a URL today, ask questions tomorrow.")
st.write(
    "LinkBrain extracts text from your saved links, generates embeddings, "
    "and lets you query your entire personal knowledge base instantly."
)
st.write("") # Spacer


# 5. VIEW TOGGLE BUTTONS
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Add Source", use_container_width=True):
        st.session_state.active_view = "add"
with col2:
    if st.button("💬 Ask Question", use_container_width=True):
        st.session_state.active_view = "ask"

st.divider()


# 6. DYNAMIC CONTENT SECTION
if st.session_state.active_view == "add":
    # --- ADD SOURCE VIEW ---
    st.markdown("### Add a Source")
    url_input = st.text_input(
        "URL", 
        placeholder="https://example.com/article", 
        label_visibility="collapsed"
    )
    
    if st.button("ADD", type="primary"):
        if url_input.strip():
            with st.spinner("Extracting and indexing content..."):
                result = ingest_url(url_input.strip())
                
            if result and result.get("success"):
                title = result.get("title")
                if title:
                    st.success(f"Successfully added '{title}' to your knowledge base.")
                else:
                    st.success("Successfully added to your knowledge base.")
                st.balloons()
            else:
                error_msg = (
                    result.get("message") or result.get("error")
                    if result
                    else "Failed to process the URL."
                )
                st.error(f"Error: {error_msg}")
        else:
            st.warning("Please enter a valid URL.")

elif st.session_state.active_view == "ask":
    # --- ASK QUESTION VIEW ---
    st.markdown("### Ask LinkBrain")
    
    stats = db_helper.get_stats()

    if stats["documents"] == 0:
        st.info(
            "Your knowledge base is empty. Add a source before asking questions."
        )
        st.stop()

    query_input = st.text_area(
        "Question", 
        placeholder="What does the article say about...?", 
        label_visibility="collapsed",
        height=100
    )
    
    if st.button("ASK", type="primary"):
        if query_input.strip():
            with st.spinner("Searching knowledge base..."):
                # Calling your REAL query function
                result = answer_query(query_input.strip())
                
            if result and "answer" in result:
                # Display Answer
                with st.container(border=True):
                    st.markdown("**Answer:**")
                    st.markdown(result["answer"])
                
                # Display Sources
                if result.get("sources"):
                    st.markdown("##### Sources:")
                    for title, url in result["sources"]:
                        display_text = title if title else url
                        st.caption(f"🔗 [{display_text}]({url})")
            else:
                error_msg = (result.get("error")
                             if result
                             else "Failed to generate an answer."
                             )
                st.error(f"Error: {error_msg}")
        else:
            st.warning("Please enter a question.")


# 7. STATISTICS SECTION
st.divider()
stats = db_helper.get_stats()

col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.metric(label="Total Documents", value=stats.get("documents", 0))
with col_stat2:
    st.metric(label="Total Chunks", value=f"{stats.get('chunks', 0):,}")


# 8. HOW IT WORKS SECTION
st.divider()
st.markdown("#### How LinkBrain Works")

steps = st.columns(5, gap="small")

with steps[0].container(border=True):
    st.markdown(
        "<div style='text-align:center'>🔗<br><b>Save</b></div>",
        unsafe_allow_html=True
    )

with steps[1].container(border=True):
    st.markdown(
        "<div style='text-align:center'>📖<br><b>Extract</b></div>",
        unsafe_allow_html=True
    )

with steps[2].container(border=True):
    st.markdown(
        "<div style='text-align:center'>🧬<br><b>Embed</b></div>",
        unsafe_allow_html=True
    )

with steps[3].container(border=True):
    st.markdown(
        "<div style='text-align:center'>💾<br><b>Store</b></div>",
        unsafe_allow_html=True
    )

with steps[4].container(border=True):
    st.markdown(
        "<div style='text-align:center'>💬<br><b>Ask</b></div>",
        unsafe_allow_html=True
    )