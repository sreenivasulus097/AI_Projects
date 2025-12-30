import streamlit as st
from agent import split_text, create_embeddings, store_embeddings, search, generate_answer
from document_loader import load_pdf

st.title("📄 Document Q&A AI Agent")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    text = load_pdf(uploaded_file)
    chunks = split_text(text)
    embeddings = create_embeddings(chunks)
    index = store_embeddings(embeddings)

    question = st.text_input("Ask a question about the document")

    if question:
        context = search(question, index, chunks)
        answer = generate_answer(question, context)
        st.write("### Answer:")
        st.write(answer)
