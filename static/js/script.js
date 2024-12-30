document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('join-button');
    const cameraPreview = document.getElementById('camera-preview');
    const cameraOffText = document.getElementById('camera-off-text');
    const localCameraPreview = document.getElementById('local-camera-preview');
    const localCameraOffText = document.getElementById('local-camera-off-text');
    const micToggleButton = document.getElementById('mic-toggle');
    const cameraToggleButton = document.getElementById('camera-toggle');
    const endInterviewButton = document.getElementById('end-interview');
    const videoPlaceholder = document.getElementById('video-placeholder');

    let stream = null;
    let localStream = null;
    let isMicOn = true;
    let isCameraOn = true;

    const toggleClass = (element, condition, classOn, classOff, iconOn, iconOff) => {
        if (condition) {
            element.classList.remove(classOff);
            element.classList.add(classOn);
            element.innerHTML = iconOn;
        } else {
            element.classList.remove(classOn);
            element.classList.add(classOff);
            element.innerHTML = iconOff;
        }
    };

    const requestMediaPermissions = async (previewElement, offTextElement, isLocal) => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: isCameraOn,
                audio: isMicOn
            });

            if (mediaStream) {
                if (isLocal && localCameraPreview) {
                    localCameraPreview.volume = 0;
                } else if (cameraPreview) {
                    cameraPreview.volume = 0;
                }
            }

            if (previewElement) {
                previewElement.srcObject = mediaStream;
                previewElement.style.opacity = isCameraOn ? 1 : 0;
            }
            if (offTextElement) {
                offTextElement.style.display = isCameraOn ? 'none' : 'flex';
            }

            if (isLocal) {
                localStream = mediaStream;
            } else {
                stream = mediaStream;
            }
        } catch (error) {
            console.error('Error requesting camera and microphone permissions:', error);
            if (previewElement) previewElement.style.opacity = 0;
            if (offTextElement) offTextElement.style.display = 'flex';
        }
    };

    const initializeVideoPlaceholder = () => {
        if (videoPlaceholder) {
            const videoFiles = [
                '/static/videos/goat.webm',
                '/static/videos/bear.webm',
                '/static/videos/rabbit.webm',
            ];
            const selectedVideo = videoFiles[Math.floor(Math.random() * videoFiles.length)];
            const source = document.createElement('source');
            source.src = selectedVideo;
            source.type = 'video/webm';
            videoPlaceholder.appendChild(source);
        }
    };

    const handleToggle = (toggleButton, isOn, classOn, classOff, iconOn, iconOff) => {
        toggleClass(toggleButton, isOn, classOn, classOff, iconOn, iconOff);
        if (localCameraPreview && localCameraOffText) {
            requestMediaPermissions(localCameraPreview, localCameraOffText, true);
        }
        if (cameraPreview && cameraOffText) {
            requestMediaPermissions(cameraPreview, cameraOffText, false);
        }
    };

    const endInterview = () => {
        console.log('Interview Ended');
        [localStream, stream].forEach((s, index) => {
            if (s) {
                s.getTracks().forEach(track => track.stop());
                if (index === 0 && localCameraPreview) {
                    localCameraPreview.srcObject = null;
                } else if (index === 1 && cameraPreview) {
                    cameraPreview.srcObject = null;
                }
            }
        });
        window.location.href = "/chatbot/";
    };

    if (joinButton) {
        joinButton.addEventListener('click', () => {
            window.location.href = '/chatbot/interview/';
        });
    }

    if (cameraPreview && cameraOffText) {
        requestMediaPermissions(cameraPreview, cameraOffText, false);
    }
    if (localCameraPreview && localCameraOffText) {
        requestMediaPermissions(localCameraPreview, localCameraOffText, true);
    }

    initializeVideoPlaceholder();

    if (micToggleButton) {
        micToggleButton.addEventListener('click', () => {
            isMicOn = !isMicOn;
            handleToggle(micToggleButton, isMicOn, 'mic-on', 'mic-off', '<i class="bi bi-mic-fill"></i>', '<i class="bi bi-mic-mute-fill"></i>');
        });
    }

    if (cameraToggleButton) {
        cameraToggleButton.addEventListener('click', () => {
            isCameraOn = !isCameraOn;
            handleToggle(cameraToggleButton, isCameraOn, 'camera-on', 'camera-off', '<i class="bi bi-camera-video-fill"></i>', '<i class="bi bi-camera-video-off-fill"></i>');
        });
    }

    if (endInterviewButton) {
        endInterviewButton.addEventListener('click', endInterview);
    }
});
