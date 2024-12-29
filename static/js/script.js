document.addEventListener('DOMContentLoaded', function() {
    const joinButton = document.getElementById('join-button');
    if(joinButton) {
        joinButton.addEventListener('click', function() {
            window.location.href = '/chatbot/interview/';
        });
    }

    const cameraPreview = document.getElementById('camera-preview');
    const cameraOffText = document.getElementById('camera-off-text');

    const localCameraPreview = document.getElementById('local-camera-preview');
    const localCameraOffText = document.getElementById('local-camera-off-text');

    let stream = null;
    let localStream = null;
    let isMicOn = true;
    let isCameraOn = true;

        // Get the buttons from the DOM
    const micToggleButton = document.getElementById('mic-toggle');
    const cameraToggleButton = document.getElementById('camera-toggle');


    // Function to request camera and microphone permissions
    async function requestMediaPermissions(cameraPreviewElement, cameraOffTextElement, streamVariable, isLocal) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: isCameraOn,
                audio: isMicOn
            });

            //Set audio volume to 0 in all video tags
            if(stream){
                if(isLocal){
                    localCameraPreview.volume = 0;
                }else{
                    cameraPreview.volume = 0;
                }
            }

            // Set the video source to the stream
            cameraPreviewElement.srcObject = stream;

            // Show the video element and hide the text message
            cameraPreviewElement.style.opacity = isCameraOn ? 1 : 0;
            cameraOffTextElement.style.display = isCameraOn ? 'none' : 'flex';

            if(isLocal){
                localStream = stream;
            }else{
                streamVariable = stream;
            }

        } catch (error) {
            console.error('Error requesting camera and microphone permissions:', error);
            cameraPreviewElement.style.opacity = 0;
            cameraOffTextElement.style.display = 'flex';
        }
    }

    // Call the function to request permissions
    if(cameraPreview && cameraOffText){
        requestMediaPermissions(cameraPreview, cameraOffText, stream, false);
    }
    if(localCameraPreview && localCameraOffText){
       requestMediaPermissions(localCameraPreview,localCameraOffText, localStream, true);
    }


    // Dynamic Video Logic
    const videoPlaceholder = document.getElementById('video-placeholder');

    if(videoPlaceholder){
        const videoFiles = [
            '/static/videos/goat.mp4',
            '/static/videos/bear.mp4',
            '/static/videos/rabbit.mp4',
        ];

        const randomIndex = Math.floor(Math.random() * videoFiles.length);
        const selectedVideo = videoFiles[randomIndex];

        const source = document.createElement('source');
        source.src = selectedVideo;
        source.type = 'video/mp4';

        videoPlaceholder.appendChild(source);
    }

    //Add event listeners to the buttons
    micToggleButton.addEventListener('click', function() {
        isMicOn = !isMicOn;
            if(isMicOn){
                micToggleButton.classList.remove('mic-off');
                micToggleButton.classList.add('mic-on');
                micToggleButton.innerHTML =  '<i class="bi bi-mic-fill"></i>';
            }else {
                micToggleButton.classList.remove('mic-on');
                micToggleButton.classList.add('mic-off');
                micToggleButton.innerHTML =  '<i class="bi bi-mic-mute-fill"></i>';
            }
            if(cameraPreview && cameraOffText) {
                requestMediaPermissions(cameraPreview, cameraOffText, stream, false);
            }
    })

    cameraToggleButton.addEventListener('click', function() {
        isCameraOn = !isCameraOn;
            if(isCameraOn) {
                cameraToggleButton.classList.remove('camera-off');
                cameraToggleButton.classList.add('camera-on');
                cameraToggleButton.innerHTML =  '<i class="bi bi-camera-video-fill"></i>';
            }else {
                cameraToggleButton.classList.remove('camera-on');
                cameraToggleButton.classList.add('camera-off');
                cameraToggleButton.innerHTML =  '<i class="bi bi-camera-video-off-fill"></i>';
            }
            if(cameraPreview && cameraOffText) {
                requestMediaPermissions(cameraPreview, cameraOffText, stream, false);
            }
    })
});