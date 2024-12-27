console.log("Chatbot JavaScript loaded");

const ws = new WebSocket((window.location.protocol === 'https:' ? 'wss://' : 'ws://') + window.location.host + '/ws/voice/');
let mediaRecorder;
let audioContext;
let audioQueue = [];
let audioSource;
let isPlaying = false;

ws.onopen = () => {
    console.log("WebSocket connection opened");
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
};

ws.onmessage = (event) => {
    if (event.data instanceof Blob) {
        console.log("Received audio data");
        audioQueue.push(event.data);
        if (!isPlaying) {
            playNextAudio();
        }
    } else {
        const data = JSON.parse(event.data);
        console.log("Received text data", data);
        if (data.message) {
            appendMessage(data.message);
        }
    }
};

ws.onerror = (error) => {
    console.error("WebSocket error:", error);
};

ws.onclose = (event) => {
    console.log('WebSocket closed', event);
};

function appendMessage(message) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('p');
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
}

async function playNextAudio() {
    if (audioQueue.length === 0) {
        isPlaying = false;
        return;
    }

    const audioBlob = audioQueue.shift();
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    isPlaying = true;

    if (audioSource) {
        audioSource.stop();
    }

    audioSource = audioContext.createBufferSource();
    audioSource.buffer = audioBuffer;
    audioSource.connect(audioContext.destination);

    audioSource.onended = () => {
        isPlaying = false;
        playNextAudio();
    };

    audioSource.start();
}

document.getElementById('start').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (event) => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(event.data);
        }
    };

    document.getElementById('start').disabled = true;
    document.getElementById('stop').disabled = false;
});

document.getElementById('stop').addEventListener('click', () => {
    mediaRecorder.stop();
    document.getElementById('start').disabled = false;
    document.getElementById('stop').disabled = true;
});
