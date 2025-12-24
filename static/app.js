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

async function startRecording() {
    audioChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.start();
}

function stopRecording() {
    mediaRecorder.stop();
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
