from flask import Flask, request, jsonify, render_template

from modules.resume import (
    analyze_resume,
    extract_text_from_pdf
)

from modules.rag import (
    ask_document,
    extract_text,
    build_vector_store
)

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- RESUME ANALYZER ----------------
@app.route("/resume")
def resume_page():
    return render_template("resume.html")


@app.route("/api/resume", methods=["POST"])
def resume_api():

    # ✅ FIXED KEY: resume
    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "error": "No PDF uploaded."
        })

    document = request.files["resume"]

    if document.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select a document."
        })

    try:
        # Only extract text (NO RAG INDEXING HERE ❌)
        text = extract_text_from_pdf(document)

        if not text:
            return jsonify({
                "success": False,
                "error": "Could not extract text from resume."
            })

        result = analyze_resume(text)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


# ---------------- DOCUMENT RAG ----------------
@app.route("/rag")
def rag_page():
    return render_template("rag.html")


@app.route("/api/rag/upload", methods=["POST"])
def rag_upload():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No document uploaded."
        })

    document = request.files["file"]

    if document.filename == "":
        return jsonify({
            "success": False,
            "error": "Please select a document."
        })

    allowed_extensions = (".pdf", ".docx", ".pptx")

    if not document.filename.lower().endswith(allowed_extensions):
        return jsonify({
            "success": False,
            "error": "Only PDF, DOCX and PPTX files are allowed."
        })

    try:
        text = extract_text(document)
        build_vector_store(text)

        return jsonify({
            "success": True,
            "message": "Document uploaded and indexed successfully."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


@app.route("/api/rag/ask", methods=["POST"])
def rag_ask():

    data = request.get_json()
    question = data.get("question", "")

    result = ask_document(question)

    return jsonify({
        "success": True,
        "result": result
    })


if __name__ == "__main__":
    app.run(debug=True)