const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const WS_URL = WS_PROTOCOL + window.location.host + '/ws/voice/';
const recordToggleButton = document.getElementById('record-toggle');
const videoPlaceholder = document.getElementById('video-placeholder');
const cameraOffLottieContainer = document.getElementById('local-camera-off');

let ws;
let mediaRecorder;
let audioContext;
let audioQueue = [];
let audioSource;
let isPlaying = false;
let isRecording = false;

function initializeWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
        console.log("WebSocket connection opened");
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    };

    ws.onmessage = handleWebSocketMessage;
    ws.onerror = (error) => console.error("WebSocket error:", error);
    ws.onclose = (event) => console.log('WebSocket closed', event);
}

function handleWebSocketMessage(event) {
    if (event.data instanceof Blob) {
        console.log("Received audio data");
        audioQueue.push(event.data);
        if (!isPlaying) {
            playNextAudioInQueue();
        }
    } else {
        const data = JSON.parse(event.data);
        console.log("Received text data", data);
    }
}

async function playNextAudioInQueue() {
    if (audioQueue.length === 0) {
        isPlaying = false;
        console.log("All audio finished playing.");
        if (videoPlaceholder) {
            videoPlaceholder.pause();
        }
        return;
    }

    const audioBlob = audioQueue.shift();
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    isPlaying = true;
    console.log("Audio playback starting.");
    if (videoPlaceholder) {
        videoPlaceholder.play();
    }

    if (audioSource) {
        audioSource.stop();
    }

    audioSource = audioContext.createBufferSource();
    audioSource.buffer = audioBuffer;
    audioSource.connect(audioContext.destination);

    audioSource.onended = playNextAudioInQueue;
    audioSource.start();
}

async function toggleRecording() {
    recordToggleButton.classList.toggle('record-on');
    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            cameraOffLottieContainer.play();
            isRecording = true;

            mediaRecorder.ondataavailable = (event) => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(event.data);
                }
            };
        } catch (error) {
            console.error("Error accessing media devices.", error);
        }
    } else {
        mediaRecorder.stop();
        cameraOffLottieContainer.pause();
        isRecording = false;
    }
}

recordToggleButton.addEventListener('click', toggleRecording);

// Initialize WebSocket connection
initializeWebSocket();
