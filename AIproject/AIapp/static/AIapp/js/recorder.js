console.log("recorder.js loaded");

let mediaRecorder = null;
let audioChunks = [];
let recordTimeout = null;
let stream = null;

const MAX_RECORD_TIME = 30000;

const button = document.getElementById("recordBtn");
const status = document.getElementById("status");
const textOutput = document.getElementById("text");
const transcriptOutput = document.getElementById("transcript");
const indicator = document.getElementById("record-indicator");

button.onmousedown = async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") return;

    try {
        status.innerText = "Recording...";
        indicator.style.display = "inline-block";
        audioChunks = [];

        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            indicator.style.display = "none";
            status.innerText = "Processing...";

            try {
                const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                const formData = new FormData();
                formData.append("audio", audioBlob);

                const response = await fetch("/api/voice/", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Server error");
                }

                const data = await response.json();

                transcriptOutput.innerText = "You: " + (data.transcript || "");
                textOutput.innerText = "AI: " + (data.response || "No response");

                speak(data.response);

                status.innerText = "Ready";
            } catch (error) {
                console.error(error);
                status.innerText = "Error occurred";
                textOutput.innerText = "AI: Something went wrong.";
            }

            // 🔥 ВАЖНО — выключаем микрофон
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        };

        mediaRecorder.start();

        recordTimeout = setTimeout(() => {
            stopRecording();
        }, MAX_RECORD_TIME);

    } catch (error) {
        console.error(error);
        status.innerText = "Microphone access denied";
    }
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
    if (!text) return;

    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-GB";

    speechSynthesis.speak(utterance);
}