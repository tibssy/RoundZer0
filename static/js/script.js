document.addEventListener('DOMContentLoaded', function() {
    const cameraPreview = document.getElementById('camera-preview');
    const cameraOffText = document.getElementById('camera-off-text');
    let stream = null;

    // Function to request camera and microphone permissions
    async function requestMediaPermissions() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            // Mute the audio track of the local stream.
            stream.getAudioTracks().forEach(track => track.enabled = false);

            // Set the video source to the stream
            cameraPreview.srcObject = stream;

            // Show the video element and hide the text message
            cameraPreview.style.display = 'block';
            cameraOffText.style.display = 'none';

        } catch (error) {
            console.error('Error requesting camera and microphone permissions:', error);
            cameraPreview.style.display = 'none';
            cameraOffText.style.display = 'block';
        }
    }

    // Call the function to request permissions
    requestMediaPermissions();
});