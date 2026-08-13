import fitz
import faiss
import numpy as np
from docx import Document
from pptx import Presentation

from modules.llm import chat_with_llm
from sentence_transformers import SentenceTransformer

# Load embedding model only once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Global variables
vector_index = None
document_chunks = []


def extract_text(file):
    """
    Extract text from PDF, DOCX or PPTX.
    """

    filename = file.filename.lower()

    # ---------------- PDF ----------------
    if filename.endswith(".pdf"):

        text = ""

        pdf = fitz.open(
            stream=file.read(),
            filetype="pdf"
        )

        for page in pdf:
            text += page.get_text()

        return text

    # ---------------- DOCX ----------------
    elif filename.endswith(".docx"):

        document = Document(file)

        text = []

        for para in document.paragraphs:

            if para.text.strip():
                text.append(para.text)

        return "\n".join(text)

    # ---------------- PPTX ----------------
    elif filename.endswith(".pptx"):

        prs = Presentation(file)

        text = []

        for slide in prs.slides:

            for shape in slide.shapes:

                if hasattr(shape, "text"):

                    if shape.text.strip():
                        text.append(shape.text)

        return "\n".join(text)

    else:

        raise ValueError(
            "Unsupported file format. Please upload a PDF, DOCX, or PPTX."
        )


def split_into_chunks(text, chunk_size=800, overlap=150):
    """
    Split text into overlapping chunks to preserve context.
    """

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_vector_store(text):
    """
    Create FAISS vector database from document.
    """

    global vector_index
    global document_chunks

    if not text.strip():
        raise ValueError("No readable text found in the document.")

    # Split document
    document_chunks = split_into_chunks(text)

    if len(document_chunks) == 0:
        raise ValueError("Unable to create document chunks.")

    # Generate embeddings
    embeddings = embedding_model.encode(document_chunks)

    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS Index
    dimension = embeddings.shape[1]

    vector_index = faiss.IndexFlatL2(dimension)
    vector_index.add(embeddings)


def retrieve_context(question, k=5):
    """
    Retrieve top-k relevant chunks from the vector store.
    """

    global vector_index
    global document_chunks

    if vector_index is None:
        return []

    # Embed Question
    question_embedding = embedding_model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    # Search
    distances, indices = vector_index.search(question_embedding, k)

    contexts = []

    for rank, idx in enumerate(indices[0], start=1):

        if idx < len(document_chunks):

            contexts.append(document_chunks[idx])


    return contexts


def ask_document(question):
    """
    Handle conversations and answer document-related questions.
    """

    user_question = question.strip()
    lower_question = user_question.lower()

    # ---------------- Conversation Handler ----------------

    if lower_question in ("hi", "hello", "hey"):
        return "Hello! 👋 I'm your AI Document Assistant."

    if lower_question in ("thanks", "thank you"):
        return "You're welcome! 😊"

    if lower_question in ("bye", "goodbye"):
        return "Goodbye! 👋 Happy learning!"
    
    contexts = retrieve_context(question)

    if vector_index is None:
        return (
        "No document has been uploaded yet.\n\n"
        "Please upload a PDF, DOCX, or PPTX first."
    )

    if not contexts:
        return (
        "I couldn't find relevant information in the uploaded document."
    )

    # Format retrieved contexts
    formatted_context = ""

    for i, chunk in enumerate(contexts, start=1):

        formatted_context += f"""
Context {i}

{chunk}

------------------------------------------------------------
"""

    prompt = f"""
You are an AI Document Assistant.

Answer ONLY using the supplied document context.

Rules:
- Never use outside knowledge.
- If unavailable, reply:
"I couldn't find this information in the uploaded document."
- Use headings and bullet points whenever appropriate.
- Preserve technical terms.
- Use numbered lists for procedures.

------------------------
Document Context
------------------------

{formatted_context}

------------------------
User Question
------------------------

{question}

------------------------
Answer
------------------------
"""
    return chat_with_llm(prompt)