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

    // Function to request camera and microphone permissions
    async function requestMediaPermissions(cameraPreviewElement, cameraOffTextElement, streamVariable, isLocal) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });

            // Mute the audio track of the local stream.
            stream.getAudioTracks().forEach(track => track.enabled = false);
            //               if(isLocal){
            //                  stream.getAudioTracks().forEach(track => track.enabled = false);
            //               }


            // Set the video source to the stream
            cameraPreviewElement.srcObject = stream;

            // Show the video element and hide the text message
            cameraPreviewElement.style.display = 'block';
            cameraOffTextElement.style.display = 'none';
            if(isLocal){
                localStream = stream;
            }else{
                streamVariable = stream;
            }

        } catch (error) {
            console.error('Error requesting camera and microphone permissions:', error);
            cameraPreviewElement.style.display = 'none';
            cameraOffTextElement.style.display = 'block';
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
});