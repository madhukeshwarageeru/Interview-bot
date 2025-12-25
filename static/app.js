// ==================== Global Variables ====================
let recorder;
let audioChunks = [];
let sttMode = "browser"; // default, will fetch from /config
let recording = false;

// ==================== Fetch Config ====================
async function loadConfig() {
    try {
        const config = await fetch("/config").then(r => r.json());
        sttMode = config.stt_mode || "browser";
    } catch (err) {
        console.error("Failed to load config, using default STT mode:", err);
    }
}

// ==================== Fetch Question ====================
async function getQuestion() {
    try {
        const res = await fetch("/question");
        const data = await res.json();

        document.getElementById("question").innerText = data.question;

        const audio = document.getElementById("questionAudio");
        audio.src = data.audio_url;
        audio.play();
    } catch (err) {
        console.error("Error fetching question:", err);
    }
}

// ==================== Start Recording ====================
let recognizedText = ""; // Store the recognized text temporarily

async function startRecording() {
    if (sttMode === "browser") {
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";

        recognition.onresult = (event) => {
            recognizedText = event.results[0][0].transcript; // Save text
            document.getElementById("recognizedText").innerText = recognizedText; // optional: show in UI
        };

        recognition.start();

        // Save recognition object globally so we can stop it manually
        window.browserRecognition = recognition;

    } else if (sttMode === "whisper") {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        audioChunks = [];

        recorder.ondataavailable = (e) => {
            audioChunks.push(e.data);
        };

        recorder.start();
    }
}

// ==================== Stop Recording (Whisper) ====================
async function stopRecordingAndSubmit() {
    if (sttMode !== "whisper" || !recorder) return;

    return new Promise((resolve) => {
        recorder.onstop = async () => {
            const blob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("audio", blob, "answer.wav");

            try {
                const res = await fetch("/answer", {
                    method: "POST",
                    body: formData
                });

                if (!res.ok) throw new Error("Server error");

                const data = await res.json();
                displayResult(data);
            } catch (err) {
                console.error("Error submitting audio answer:", err);
                alert("Failed to submit answer. Please try again.");
            }

            recording = false;
            resolve();
        };

        recorder.stop();
    });
}

// ==================== Submit Text Answer (Browser STT) ====================
async function submitBrowserAnswer() {
    if (sttMode === "browser" && recognizedText) {
        await submitAnswerText(recognizedText);

        // Stop recognition
        if (window.browserRecognition) {
            window.browserRecognition.stop();
        }

        // Clear recognized text after submission
        recognizedText = "";
        document.getElementById("recognizedText").innerText = "";
    } else {
        alert("No text recognized yet.");
    }
}


async function submitAnswerText(text) {
    const res = await fetch("/answer", {
        method: "POST",
        body: new URLSearchParams({ text })
        
    });
    const data = await res.json();
    displayResult(data);
}


// ==================== Display Result ====================
function displayResult(data) {
    document.getElementById("result").innerText =
        `Decision: ${data.decision}\n\n${data.evaluation}`;

    const feedback = document.getElementById("feedbackAudio");
    if (data.audio_url) {
        feedback.src = data.audio_url;
        feedback.play();
    }
}

// ==================== Event Listeners ====================

// Call this on "Load Question" button
document.getElementById("loadQuestionBtn").addEventListener("click", getQuestion);

// Call this on "Start Recording" button
document.getElementById("startRecordingBtn").addEventListener("click", startRecording);

// Call this on "Stop & Submit" button (only for whisper)
document.getElementById("stopRecordingBtn").addEventListener("click", stopRecordingAndSubmit);

// ==================== Initialize ====================
window.addEventListener("DOMContentLoaded", async () => {
    await loadConfig();
});
