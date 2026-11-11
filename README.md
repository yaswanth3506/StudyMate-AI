# StudyMate AI – AI-Powered Study Assistant

StudyMate AI is a Generative AI-powered study assistant that allows users to upload academic documents and interact with their content through natural language questions. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-aware responses.

## Overview

Studying from lengthy academic documents can make it difficult to find specific information quickly. StudyMate AI addresses this by providing an interactive question-answering system that helps users understand and explore their study materials.

The application processes uploaded documents, converts their content into searchable representations, retrieves relevant context, and uses a Large Language Model (LLM) to generate answers.

## Features

- **Document Upload:** Upload academic materials in PDF format.
- **Document Processing:** Extract text from uploaded documents using PyMuPDF.
- **Semantic Search:** Retrieve relevant document content using Sentence Transformers and FAISS.
- **AI-Powered Responses:** Generate context-aware answers using the Groq LLM API.
- **Conversational Interface:** Interact with uploaded study materials using natural language queries.
- **RAG Architecture:** Combine document retrieval with Large Language Model generation.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Streamlit | User interface |
| Groq API | LLM integration |
| FAISS | Vector similarity search |
| Sentence Transformers | Text embeddings |
| PyMuPDF | PDF text extraction |
| RAG | Retrieval-Augmented Generation |

## System Workflow

1. **Document Upload:** Users upload their academic PDF documents.
2. **Text Extraction:** PyMuPDF extracts textual content from the documents.
3. **Text Processing:** Extracted content is divided into smaller chunks.
4. **Embedding Generation:** Sentence Transformers converts text chunks into vector embeddings.
5. **Vector Storage:** FAISS stores the embeddings for efficient similarity search.
6. **Context Retrieval:** Relevant document chunks are retrieved based on the user's question.
7. **Response Generation:** The retrieved context is passed to the Groq LLM API to generate a relevant answer.
8. **User Interaction:** The generated response is displayed through the Streamlit interface.

## RAG Architecture

The project follows a Retrieval-Augmented Generation pipeline:

**Document → Text Extraction → Chunking → Embeddings → FAISS Retrieval → Context → LLM → Answer**

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yaswanth3506-beep/StudyMate-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd StudyMate-AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project directory and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

## Use Cases

- Understanding lengthy academic documents.
- Finding specific information from study materials.
- Asking questions about uploaded PDFs.
- Supporting interactive and personalized learning.

## Future Enhancements

- Support for DOCX and TXT documents.
- Improved retrieval and response quality.
- Document summarization.
- Multi-document question answering.
- Enhanced conversational memory.

## Disclaimer

StudyMate AI is an educational assistance tool designed to support learning and document exploration. Generated responses should be verified against the original study materials.
