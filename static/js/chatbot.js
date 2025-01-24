const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const WS_URL = `${WS_PROTOCOL}${window.location.host}/ws/voice/`;
const videoPlaceholder = document.getElementById('video-placeholder');
const cameraOffLottieContainer = document.getElementById('local-camera-off');

let ws;
let mediaRecorder;
let audioContext;
let audioQueue = [];
let audioSource;
let isPlaying = false;
let isRecording = false;
let silentSince = null;
let recordingStartTime = null;
let audioStream = null;
let isHandlingAudio = false;

const THRESHOLD = 0.01;
const SILENCE_DELAY = 2000;
const MIN_RECORDING_DURATION = 2000 + SILENCE_DELAY;


/**
 * Initializes the WebSocket connection and sets up audio processing.
 */
function initializeWebSocket() {
    ws = new WebSocket(WS_URL);

    ws.addEventListener('open', async () => {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        try {
            audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            setupAudioProcessing(audioStream);
        } catch (err) {
            console.error("Error accessing microphone:", err);
        }
    });

    ws.addEventListener('message', handleWebSocketMessage);
    ws.addEventListener('error', console.error.bind(console, "WebSocket error:"));
}

/**
 * Handles incoming WebSocket messages.
 * @param {MessageEvent} event - The WebSocket message event.
 */
function handleWebSocketMessage(event) {
    if (event.data instanceof Blob) {
        audioQueue.push(event.data);
        if (!isPlaying) playNextAudioInQueue();
    } else {
        const data = JSON.parse(event.data);
    }
}

/**
 * Plays the next audio file in the queue.
 */
async function playNextAudioInQueue() {
    if (audioQueue.length === 0) {
        isPlaying = false;
        videoPlaceholder.pause();
        isHandlingAudio = false;
        return;
    }

    const audioBlob = audioQueue.shift();
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    isPlaying = true;
    videoPlaceholder.play();

    if (audioSource) audioSource.stop();

    audioSource = audioContext.createBufferSource();
    audioSource.buffer = audioBuffer;
    audioSource.connect(audioContext.destination);
    audioSource.onended = playNextAudioInQueue;
    audioSource.start();
}

/**
 * Toggles the recording state between start and stop.
 */
async function toggleRecording() {
    if (!isRecording) {
        if (audioStream) {
            startMediaRecorder(audioStream);
        }
    } else {
        stopMediaRecorder();
    }
}

/**
 * Starts the media recorder for audio recording.
 * @param {MediaStream} stream - The audio stream to record.
 */
function startMediaRecorder(stream) {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    cameraOffLottieContainer.play();
    isRecording = true;
    recordingStartTime = performance.now();

    mediaRecorder.ondataavailable = (event) => {
        const recordingDuration = performance.now() - recordingStartTime;
        if (recordingDuration >= MIN_RECORDING_DURATION && ws.readyState === WebSocket.OPEN) {
            isHandlingAudio = true;
            ws.send(event.data);
        }
    };
}

/**
 * Stops the media recorder and resets recording-related variables.
 */
function stopMediaRecorder() {
    mediaRecorder.stop();
    cameraOffLottieContainer.pause();
    isRecording = false;
    recordingStartTime = null;
}

/**
 * Sets up audio processing using an audio context and analyser node.
 * @param {MediaStream} stream - The audio stream for processing.
 */
function setupAudioProcessing(stream) {
    const analyser = audioContext.createAnalyser();
    const microphone = audioContext.createMediaStreamSource(stream);
    const dataArray = new Uint8Array(analyser.fftSize);

    microphone.connect(analyser);
    calculateRMS(analyser, dataArray);
}

/**
 * Calculates the root mean square (RMS) of the audio data for silence detection.
 * @param {AnalyserNode} analyser - The audio analyser node.
 * @param {Uint8Array} dataArray - The array to store analyser data.
 */
function calculateRMS(analyser, dataArray) {
    if (audioQueue.length > 0 || isPlaying || isHandlingAudio) {
        silentSince = null;
        if (isRecording) toggleRecording();
        requestAnimationFrame(() => calculateRMS(analyser, dataArray));
        return;
    }

    analyser.getByteTimeDomainData(dataArray);
    const rms = computeRMS(dataArray);
    if (rms >= THRESHOLD) {
        if (!isRecording) toggleRecording();
        silentSince = null;
    } else {
        handleSilence();
    }

    requestAnimationFrame(() => calculateRMS(analyser, dataArray));
}

/**
 * Computes the root mean square (RMS) of the given audio data array.
 * @param {Uint8Array} dataArray - The array of audio data.
 * @returns {number} - The computed RMS value.
 */
function computeRMS(dataArray) {
    const sum = dataArray.reduce((acc, val) => {
        const normalized = (val - 128) / 128;
        return acc + normalized * normalized;
    }, 0);
    return Math.sqrt(sum / dataArray.length);
}

/**
 * Handles silence detection and stops recording if silent for too long.
 */
function handleSilence() {
    if (!silentSince) {
        silentSince = performance.now();
    } else if (performance.now() - silentSince >= SILENCE_DELAY && isRecording) {
        toggleRecording();
        silentSince = null;
    }
}

initializeWebSocket();
