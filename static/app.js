// ==================================================
// STUDYMATE AI - FRONTEND CONTROLLER (FINAL FIX)
// ==================================================



// =============================
// ENTER KEY SUPPORT (GLOBAL)
// =============================
document.addEventListener("keydown", function (event) {

    // RAG ENTER
    if (event.key === "Enter") {

        const questionBox = document.getElementById("question");
        if (document.activeElement === questionBox) {
            askQuestion();
        }

        // RESUME ENTER
        const resumeFile = document.getElementById("resumeFile");
        if (document.activeElement === resumeFile) {
            analyzeResume();
        }
    }
});



// =============================
// RESUME ANALYZER
// =============================
async function analyzeResume() {

    const fileInput = document.getElementById("resumeFile");
    const output = document.getElementById("output");

    if (!fileInput.files.length) {
        output.innerText = "❌ Please select a PDF resume.";
        return;
    }

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);

    output.innerText = "Analyzing resume... Please wait.";

    try {

        const response = await fetch("/api/resume", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            output.innerText = data.result;
        } else {
            output.innerText = "❌ " + data.error;
        }

    } catch (err) {
        output.innerText = "❌ Failed to analyze resume.";
    }
}



// =============================
// RAG - UPLOAD DOCUMENT (FIXED MESSAGE)
// =============================
async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");
    const chatBox = document.getElementById("chatBox");

    if (!fileInput.files.length) {
        alert("Please select a document");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    let uploadMsg = document.createElement("div");
    uploadMsg.className = "message ai";
    uploadMsg.innerText = "Uploading document...";
    chatBox.appendChild(uploadMsg);

    try {

        const response = await fetch("/api/rag/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        // REMOVE "Uploading..." AFTER RESPONSE
        uploadMsg.remove();

        let finalMsg = document.createElement("div");
        finalMsg.className = "message ai";

        if (data.success) {
            finalMsg.innerText = "Document uploaded and indexed successfully.";
        } else {
            finalMsg.innerText = "❌ " + data.error;
        }

        chatBox.appendChild(finalMsg);

    } catch (err) {
        uploadMsg.remove();

        let errorMsg = document.createElement("div");
        errorMsg.className = "message ai";
        errorMsg.innerText = "❌ Upload failed";

        chatBox.appendChild(errorMsg);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}



// =============================
// RAG - ASK QUESTION (ENTER FIXED UX)
// =============================
async function askQuestion() {

    const questionInput = document.getElementById("question");
    const chatBox = document.getElementById("chatBox");

    const question = questionInput.value.trim();

    if (!question) return;

    // user message
    let userMsg = document.createElement("div");
    userMsg.className = "message user";
    userMsg.innerText = question;
    chatBox.appendChild(userMsg);

    questionInput.value = "";

    // thinking message
    let botMsg = document.createElement("div");
    botMsg.className = "message ai" ;
    botMsg.innerText = "Thinking...";
    chatBox.appendChild(botMsg);

    try {

        const response = await fetch("/api/rag/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        botMsg.innerText = data.success
            ? data.result
            : "❌ " + data.error;

    } catch (err) {
        botMsg.innerText = "❌ Server error";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}