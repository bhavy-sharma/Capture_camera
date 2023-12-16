document.addEventListener('DOMContentLoaded', () => {
  const startButton = document.getElementById('startButton');
  const cameraVideo = document.getElementById('cameraVideo');

  let stream;
  let ws;

  startButton.addEventListener('click', async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      cameraVideo.srcObject = stream;

      // Initialize WebSocket connection
      ws = new WebSocket('ws://localhost:8080');

      // Send the camera stream to the server
      const mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          ws.send(event.data);
        }
      };

      mediaRecorder.start();
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  });
});
