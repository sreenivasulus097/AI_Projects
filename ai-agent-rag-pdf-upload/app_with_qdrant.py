import streamlit as st
from qadrant_agent import split_text, upload_chunks, search_qdrant, generate_answer
from document_loader import load_pdf
from qdrant_db import COLLECTION_NAME

st.title("📄 Document Q&A AI Agent (Qdrant)")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    text = load_pdf(uploaded_file)
    chunks = split_text(text)

    # initialize session state for indexed files
    if "indexed_files" not in st.session_state:
        st.session_state["indexed_files"] = []

    if uploaded_file.name in st.session_state["indexed_files"]:
        st.info("This file has already been indexed in this session.")
    else:
        with st.spinner("Indexing document..."):
            upload_chunks(chunks, source_name=uploaded_file.name)

        st.success("Document indexed successfully!")
        st.session_state["indexed_files"].append(uploaded_file.name)

    st.write("---")
    st.write("## Ask the document")
    top_k = st.selectbox("Number of context matches to retrieve", options=[1, 3, 5, 10], index=1)
    question = st.text_input("Ask a question about the document")
    do_search = st.button("Search")

    if do_search and question:
        try:
            with st.spinner("Searching Qdrant and generating an answer..."):
                context = search_qdrant(question, top_k=top_k)

            if not context:
                st.warning("No relevant context found in the indexed documents.")
            else:
                st.write("### Retrieved context snippets")
                for i, ctx in enumerate(context, start=1):
                    # ctx is expected to be a dict {'text':..., 'source':...}
                    src = ctx.get("source") if isinstance(ctx, dict) else None
                    header = f"Match {i}" + (f" — {src}" if src else "")
                    with st.expander(header):
                        text_body = ctx.get("text") if isinstance(ctx, dict) else str(ctx)
                        excerpt = text_body if len(text_body) < 1000 else text_body[:1000] + "..."
                        st.write(excerpt)

                # Generate answer from retrieved context (pass list as-is, generator handles dicts)
                try:
                    answer = generate_answer(question, context)
                    st.write("### Answer:")
                    st.write(answer)
                except Exception as e:
                    st.error("Answer generation failed: %s" % e)

        except Exception as e:
            st.error("Search failed: %s" % e)
            st.info("Check your Qdrant connection, API keys, and network.")
