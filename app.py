import streamlit as st
import tempfile
import os
from rag_pipeline import RAGChatbot
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Local RAG AI Chatbot", layout="wide")
st.title("Local RAG-based AI Chatbot")

# Initialize session state
if "chatbot" not in st.session_state:
    st.session_state["chatbot"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.sidebar.header("Local AI Configuration")
st.sidebar.info("This chatbot uses free local HuggingFace models. No API key needed!")

st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True
)

if st.sidebar.button("Process Documents"):
    if not uploaded_files:
        st.sidebar.warning("Please upload at least one document.")
    else:
        with st.spinner("Processing documents..."):
            temp_files = []
            for file in uploaded_files:
                suffix = ".pdf" if file.type == "application/pdf" else ".txt"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(file.read())
                    temp_files.append((file.name, tmp.name))
            
            # Create local chatbot
            chatbot = RAGChatbot()
            chatbot.process_files(temp_files)
            st.session_state["chatbot"] = chatbot
            st.session_state["chat_history"] = []
            st.sidebar.success("Files processed and indexed successfully using local AI!")

# Display current status
if st.session_state.get("chatbot"):
    st.info("Currently using: LOCAL AI (HuggingFace models)")

st.write("### Ask a question about your documents:")
user_question = st.text_input("Your question", key="user_question")

if st.button("Ask"):
    chatbot = st.session_state.get("chatbot")
    if not chatbot:
        st.warning("Please upload and process documents first.")
    elif not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            result = chatbot.ask(user_question)
            st.session_state["chat_history"].append((user_question, result["answer"]))
            
            # Display question and answer
            st.write(f"**Q:** {user_question}")
            st.write(f"**A:** {result['answer']}")
            
            # Display sources
            if result["sources"]:
                st.write("**Sources:**")
                for i, src in enumerate(result["sources"], 1):
                    with st.expander(f"Source {i}: {src['filename']}"):
                        st.write(src['snippet'])
            else:
                st.write("No sources found.")

if st.button("Clear Chat"):
    st.session_state["chat_history"] = []
    if st.session_state.get("chatbot"):
        st.session_state["chatbot"].clear_memory()
    st.success("Chat history cleared.")

if st.session_state["chat_history"]:
    st.write("---")
    st.write("### Chat History:")
    for q, a in st.session_state["chat_history"]:
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")
        st.write("---") 