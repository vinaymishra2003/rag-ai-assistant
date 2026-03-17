import streamlit as st
import os
import zipfile
import json
from dotenv import load_dotenv
from groq import Groq

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- CONFIG ----------------
st.set_page_config(page_title="RAG Assistant", layout="wide")

# ---------------- COLORFUL UI ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1f1f2e;
    color: white;
}

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    text-align: right;
}

.chat-bot {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff7eb3, #ff758c);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px 16px;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #ff4e8a, #ff2e63);
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD API ----------------
load_dotenv()
api_key = api_key = os.getenv("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"]

if not api_key:
    st.error("❌ API key missing")
    st.stop()

client = Groq(api_key=api_key)
MODEL_NAME = "llama-3.1-8b-instant"

# ---------------- SESSION ----------------
if "db" not in st.session_state:
    st.session_state.db = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "docs" not in st.session_state:
    st.session_state.docs = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Controls")

    uploaded_file = st.file_uploader("Upload JSON ZIP", type=["zip"])

    if uploaded_file:
        with st.spinner("Processing document..."):

            with open("temp.zip", "wb") as f:
                f.write(uploaded_file.read())

            with zipfile.ZipFile("temp.zip", 'r') as zip_ref:
                zip_ref.extractall("data")

            file_path = "data/train-v1.1.json"

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            documents = []
            for item in data["data"]:
                for para in item["paragraphs"]:
                    documents.append(Document(page_content=para["context"]))

            documents = documents[:300]

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=150
            )

            docs = splitter.split_documents(documents)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            db = FAISS.from_documents(docs, embeddings)

            st.session_state.db = db
            st.session_state.docs = docs

        st.success("✅ Document Ready")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align: center;'>🤖 RAG AI Assistant</h1>
<p style='text-align: center;'>Ask questions from your uploaded document</p>
""", unsafe_allow_html=True)

# ---------------- SUMMARY ----------------
if st.session_state.docs:
    if st.button("📄 Generate Summary"):
        with st.spinner("Generating summary..."):
            sample_text = "\n".join(
                [doc.page_content for doc in st.session_state.docs[:5]]
            )

            prompt = f"Summarize:\n\n{sample_text}"

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = response.choices[0].message.content

        st.success("Summary Generated")
        st.write(summary)

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user">🧑‍💻 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------
query = st.chat_input("Type your question...")

if query and st.session_state.db:
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    with st.spinner("Thinking..."):
        retriever = st.session_state.db.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)

        context = "\n".join([doc.page_content for doc in docs])

        history_text = "\n".join(
            [f'{m["role"]}: {m["content"]}' for m in st.session_state.chat_history]
        )

        prompt = f"""
        You are a helpful AI assistant.

        Chat History:
        {history_text}

        Context:
        {context}

        Question:
        {query}

        Answer clearly.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# ---------------- PDF DOWNLOAD ----------------
def create_pdf(chat_history, filename="chat.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        text = f"<b>{role}:</b> {msg['content']}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)
    return filename

if st.session_state.chat_history:
    if st.button("📥 Download Chat as PDF"):
        file_path = create_pdf(st.session_state.chat_history)

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Click to Download",
                data=f,
                file_name="chat_history.pdf",
                mime="application/pdf"
            )