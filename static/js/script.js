document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('join-button');
    const cameraPreview = document.getElementById('camera-preview');
    const cameraOffText = document.getElementById('camera-off-text');
    const localCameraPreview = document.getElementById('local-camera-preview');
    const localCameraOff = document.getElementById('local-camera-off');
    const cameraToggleButton = document.getElementById('camera-toggle');
    const endInterviewButton = document.getElementById('end-interview');

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
                previewElement.style.display = isCameraOn ? 'unset' : 'none';
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
            if (offTextElement) offTextElement.style.display = 'flex';
        }
    };

    const handleToggle = (toggleButton, isOn, classOn, classOff, iconOn, iconOff) => {
        toggleClass(toggleButton, isOn, classOn, classOff, iconOn, iconOff);
        if (localCameraPreview && localCameraOff) {
            requestMediaPermissions(localCameraPreview, localCameraOff, true);
        }
        if (cameraPreview && cameraOffText) {
            requestMediaPermissions(cameraPreview, cameraOffText, false);
        }
    };

    const endInterview = () => {
        console.log('endInterview function called'); // Add this line
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
        console.log('Attempting redirection to /chatbot/interview/end/'); // Add this line
        window.location.href = "/chatbot/interview/end/";
    };


    if (joinButton) {
        joinButton.addEventListener('click', () => {
            window.location.href = '/chatbot/interview/';
        });
    }

    if (cameraPreview && cameraOffText) {
        requestMediaPermissions(cameraPreview, cameraOffText, false);
    }
    if (localCameraPreview && localCameraOff) {
        requestMediaPermissions(localCameraPreview, localCameraOff, true);
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