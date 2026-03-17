# 🤖 RAG AI Assistant

### 📄 Document Q&A + Summarization using Generative AI

<p align="center">
  <img src="https://img.shields.io/badge/AI-RAG-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Streamlit-Deployed-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/LLM-Groq-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/VectorDB-FAISS-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

---

## 🚀 Live Demo

🔗 **Live App:**https://rag-ai-assistant-fcgixnxkc66puon8rlmktg.streamlit.app

---

## 📌 Overview

This project is a **Retrieval-Augmented Generation (RAG) system** that allows users to:

* Upload documents 📄
* Ask questions 💬
* Get accurate AI-generated answers 🤖

The system uses **semantic search + LLM reasoning** to provide context-aware responses.

---

## ✨ Key Features

🚀 Upload PDF/Text documents
🔍 Smart semantic search (FAISS)
💬 Chat with your document
🧠 Conversation memory
📑 Automatic document summarization
📥 Export chat as PDF
🎨 Clean and interactive UI

---

## 🏗️ RAG Architecture

```text
📄 Document Upload
        ↓
✂️ Text Chunking
        ↓
🧠 Embeddings Generation
        ↓
📦 FAISS Vector Store
        ↓
🔍 Retriever (Top-K Search)
        ↓
🤖 LLM (Groq)
        ↓
💬 Final Answer
```

---

## 🧰 Tech Stack

| Category      | Technology            |
| ------------- | --------------------- |
| 🖥️ Frontend  | Streamlit             |
| 🤖 LLM        | Groq (LLaMA)          |
| 🔍 Embeddings | Sentence Transformers |
| 📦 Vector DB  | FAISS                 |
| 🔗 Framework  | LangChain             |
| 📄 PDF Export | ReportLab             |

---

## 📂 Project Structure

```
rag-ai-assistant/
│── Ragui.py
│──Project_rag.ipynb
│── requirements.txt
│── README.md
│── .gitignore
```

---

## ⚙️ Installation & Setup

### 🔹 Clone Repository

```
git clone https://github.com/YOUR_USERNAME/rag-ai-assistant.git
cd rag-ai-assistant
```

---

### 🔹 Install Dependencies

```
pip install -r requirements.txt
```

---

### 🔹 Add API Key

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 🔹 Run App

```
streamlit run app.py
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Deploy on Streamlit Cloud
3. Add secret:

```
GROQ_API_KEY = "your_api_key_here"
```

---

## 🎯 Use Cases

🏢 Company Knowledge Assistant
📘 Student Learning Tool
⚖️ Legal Document Analysis
🎧 Customer Support Bot
📊 HR Policy Assistant

---

## ⚠️ Limitations

* Depends on document quality
* Large files may slow response
* Requires API access

---

## 🔮 Future Enhancements

✨ Source citation (very important)
🌍 Multi-language support
📊 Multi-document comparison
⚡ Faster retrieval optimization
🧾 Highlight answers in document

---

## 👨‍💻 Author

**Vinay Mishra**

---

## ⭐ Support

If you like this project:

👉 Give it a ⭐ on GitHub
👉 Share with others

---

## 📜 License

This project is open-source and free to use.
