document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        joinButton: document.getElementById('join-button'),
        cameraPreview: document.getElementById('camera-preview'),
        cameraOffText: document.getElementById('camera-off-text'),
        localCameraPreview: document.getElementById('local-camera-preview'),
        localCameraOff: document.getElementById('local-camera-off'),
        cameraToggleButton: document.getElementById('camera-toggle'),
        endInterviewButton: document.getElementById('end-interview')
    };

    let stream = null;
    let localStream = null;
    let isMicOn = true;
    let isCameraOn = true;

    const toggleClass = (element, condition, classOn, classOff, iconOn, iconOff) => {
        element.classList.toggle(classOn, condition);
        element.classList.toggle(classOff, !condition);
        element.innerHTML = condition ? iconOn : iconOff;
    };

    const requestMediaPermissions = async (previewElement, offTextElement, isLocal) => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: isCameraOn,
                audio: isMicOn
            });

            if (mediaStream) {
                previewElement.volume = 0;
                previewElement.srcObject = mediaStream;
                previewElement.style.display = isCameraOn ? 'unset' : 'none';
                offTextElement.style.display = isCameraOn ? 'none' : 'flex';

                if (isLocal) {
                    localStream = mediaStream;
                } else {
                    stream = mediaStream;
                }
            }
        } catch (error) {
            console.error('Error requesting camera and microphone permissions:', error);
            offTextElement.style.display = 'flex';
        }
    };

    const handleToggle = (toggleButton, isOn, classOn, classOff, iconOn, iconOff) => {
        toggleClass(toggleButton, isOn, classOn, classOff, iconOn, iconOff);
        requestMediaPermissions(elements.localCameraPreview, elements.localCameraOff, true);
        requestMediaPermissions(elements.cameraPreview, elements.cameraOffText, false);
    };

    const endInterview = () => {
        [localStream, stream].forEach((s, index) => {
            if (s) {
                s.getTracks().forEach(track => track.stop());
                const previewElement = index === 0 ? elements.localCameraPreview : elements.cameraPreview;
                if (previewElement) {
                    previewElement.srcObject = null;
                }
            }
        });
        window.location.href = "/chatbot/interview/end/";
    };

    const initialize = () => {
        if (elements.joinButton) {
            elements.joinButton.addEventListener('click', () => {
                window.location.href = '/chatbot/interview/';
            });
        }

        requestMediaPermissions(elements.cameraPreview, elements.cameraOffText, false);
        requestMediaPermissions(elements.localCameraPreview, elements.localCameraOff, true);

        if (elements.cameraToggleButton) {
            elements.cameraToggleButton.addEventListener('click', () => {
                isCameraOn = !isCameraOn;
                handleToggle(elements.cameraToggleButton, isCameraOn, 'camera-on', 'camera-off', '<i class="bi bi-camera-video-fill"></i>', '<i class="bi bi-camera-video-off-fill"></i>');
            });
        }

        if (elements.endInterviewButton) {
            elements.endInterviewButton.addEventListener('click', endInterview);
        }
    };

    initialize();
});
