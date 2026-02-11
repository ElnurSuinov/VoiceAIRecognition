console.log("recorder.js loaded");
console.log("Sending audio to server");


let mediaRecorder = null;
let audioChunks = [];
let recordTimeout = null;

const MAX_RECORD_TIME = 10000;

const button = document.getElementById("recordBtn");
const status = document.getElementById("status");
const textOutput = document.getElementById("text");
const indicator = document.getElementById("record-indicator");

button.onmousedown = async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") return;

    status.innerText = "Recording...";
    indicator.style.display = "inline-block";
    audioChunks = [];

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.onstop = async () => {
        indicator.style.display = "none";
        status.innerText = "Processing...";

        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", audioBlob);

        const response = await fetch("/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        textOutput.innerText = "AI: " + data.response;
        speak(data.response);

        status.innerText = "Done.";
    };

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.start();

    recordTimeout = setTimeout(() => {
        stopRecording();
    }, MAX_RECORD_TIME);
};

button.onmouseup = () => {
    stopRecording();
};

function stopRecording() {
    if (!mediaRecorder) return;

    if (mediaRecorder.state === "recording") {
        mediaRecorder.stop();
    }

    if (recordTimeout) {
        clearTimeout(recordTimeout);
        recordTimeout = null;
    }
}

function speak(text) {
    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-GB";

    speechSynthesis.speak(utterance);
}
