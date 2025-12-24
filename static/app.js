let mediaRecorder;
let audioChunks = [];

async function getQuestion() {
    const res = await fetch("/question");
    const data = await res.json();

    document.getElementById("question").innerText = data.question;

    const audio = document.getElementById("questionAudio");
    audio.src = data.audio_url;
    audio.play();
}
let recorder;

const config = await fetch("/config").then(r => r.json());
const sttMode = config.stt_mode;




async function recordAnswer() {
  if (sttMode === "whisper") {
  const blob = await recorder.stop();
  const form = new FormData();
  form.append("audio", blob);

  await fetch("/answer", {
    method: "POST",
    body: form
  });
  }

  if (sttMode === "browser") {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = async (event) => {
      const text = event.results[0][0].transcript;

      await fetch("/answer", {
        method: "POST",
        body: new URLSearchParams({ text })
      });
    };
  }
}


async function submitAnswer() {
    const blob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("audio", blob, "answer.wav");

    const res = await fetch("/answer", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("result").innerText =
        `Decision: ${data.decision}\n\n${data.evaluation}`;

    const feedback = document.getElementById("feedbackAudio");
    feedback.src = data.audio_url;
    feedback.play();
}


async function startRecording() {
    if (sttMode === "browser") {
        // Browser STT using Web Speech API
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        const recognition = new SpeechRecognition();
        recognition.lang = "en-US";

        recognition.onresult = async (event) => {
            const text = event.results[0][0].transcript;
            await submitAnswerText(text);
        };

        recognition.start();

    } else if (sttMode === "whisper") {
        // Whisper requires audio recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        audioChunks = [];

        recorder.ondataavailable = (e) => {
            audioChunks.push(e.data);
        };

        recorder.start();
    }
}

// Call this to stop recording for Whisper
async function stopRecordingAndSubmit() {
    if (sttMode === "whisper" && recorder) {
        return new Promise((resolve) => {
            recorder.onstop = async () => {
                const blob = new Blob(audioChunks, { type: "audio/wav" });
                const formData = new FormData();
                formData.append("audio", blob, "answer.wav");

                const res = await fetch("/answer", {
                    method: "POST",
                    body: formData
                });
                const data = await res.json();
                displayResult(data);
                resolve();
            };
            recorder.stop();
        });
    }
}

// Helper for browser STT (text)
async function submitAnswerText(text) {
    const res = await fetch("/answer", {
        method: "POST",
        body: new URLSearchParams({ text })
    });
    const data = await res.json();
    displayResult(data);
}

// Common result display
function displayResult(data) {
    document.getElementById("result").innerText =
        `Decision: ${data.decision}\n\n${data.evaluation}`;

    const feedback = document.getElementById("feedbackAudio");
    feedback.src = data.audio_url;
    feedback.play();
}
