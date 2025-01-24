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

    /**
     * Toggles a CSS class and updates the element's inner HTML.
     * @param {HTMLElement} element - The element to update.
     * @param {boolean} condition - Whether to apply the "on" state.
     * @param {string} classOn - Class to apply when "on".
     * @param {string} classOff - Class to apply when "off".
     * @param {string} iconOn - HTML content for the "on" state.
     * @param {string} iconOff - HTML content for the "off" state.
     */
    const toggleClass = (element, condition, classOn, classOff, iconOn, iconOff) => {
        if (!element) return;
        element.classList.toggle(classOn, condition);
        element.classList.toggle(classOff, !condition);
        element.innerHTML = condition ? iconOn : iconOff;
    };

    /**
     * Sets up a media stream for a preview element and toggles visibility.
     * @param {MediaStream} mediaStream - The media stream to display.
     * @param {HTMLVideoElement} previewElement - The video element for the preview.
     * @param {HTMLElement} offTextElement - Element to display when the camera is off.
     */
    const handleMediaStream = (mediaStream, previewElement, offTextElement) => {
        if (!previewElement || !offTextElement) return;
        previewElement.srcObject = mediaStream;
        previewElement.style.display = isCameraOn ? 'unset' : 'none';
        offTextElement.style.display = isCameraOn ? 'none' : 'flex';
    };

    /**
     * Requests media permissions and sets up the appropriate stream.
     * @param {HTMLVideoElement} previewElement - The video element for preview.
     * @param {HTMLElement} offTextElement - Element to display when the camera is off.
     * @param {boolean} isLocal - Whether this is for the local camera.
     */
    const requestMediaPermissions = async (previewElement, offTextElement, isLocal) => {
        try {
            const mediaStream = await navigator.mediaDevices.getUserMedia({
                video: isCameraOn,
                audio: isMicOn
            });

            if (mediaStream) {
                if (previewElement) {
                    previewElement.volume = 0;
                }
            }

            handleMediaStream(mediaStream, previewElement, offTextElement);

            if (isLocal) {
                localStream = mediaStream;
            } else {
                stream = mediaStream;
            }
        } catch (error) {
            if (isLocal && localCameraPreview) {
                localCameraPreview.style.display = 'none';
            }
            if (offTextElement) {
                offTextElement.style.display = 'flex';
            }
        }
    };

    /**
     * Handles camera toggling and updates UI.
     * @param {HTMLElement} toggleButton - The camera toggle button element.
     * @param {boolean} isOn - Whether the camera is turned on.
     */
    const handleCameraToggle = (toggleButton, isOn) => {
        toggleClass(toggleButton, isOn, 'camera-on', 'camera-off', '<i class="bi bi-camera-video-fill"></i>', '<i class="bi bi-camera-video-off-fill"></i>');
        if (localCameraPreview && localCameraOff) {
            requestMediaPermissions(localCameraPreview, localCameraOff, true);
        }
        if (cameraPreview && cameraOffText) {
            requestMediaPermissions(cameraPreview, cameraOffText, false);
        }
    };

    /**
     * Ends the interview by stopping streams and redirecting the user.
     */
    const endInterview = () => {
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
            handleCameraToggle(cameraToggleButton, isCameraOn);
        });
    }

    if (endInterviewButton) {
        endInterviewButton.addEventListener('click', endInterview);
    }
});