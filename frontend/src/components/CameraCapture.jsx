import React, { useRef, useState } from 'react';
import '../styles/CameraCapture.css';

function CameraCapture({ onImageCapture, loading }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [preview, setPreview] = useState(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' },
        audio: false
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setCameraActive(true);
      }
    } catch (err) {
      console.error('Error accessing camera:', err);
      alert('Unable to access camera. Please check permissions.');
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
      setCameraActive(false);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
      
      const imageData = canvasRef.current.toDataURL('image/jpeg').split(',')[1];
      setPreview(canvasRef.current.toDataURL('image/jpeg'));
      stopCamera();
      
      onImageCapture(imageData);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const base64 = event.target.result.split(',')[1];
        setPreview(event.target.result);
        onImageCapture(base64);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleReset = () => {
    setPreview(null);
    setCameraActive(false);
  };

  return (
    <div className="camera-capture">
      <h2>Capture or Upload Waste Image</h2>
      
      <div className="capture-container">
        {!cameraActive && !preview && (
          <div className="button-group">
            <button 
              className="btn btn-primary"
              onClick={startCamera}
              disabled={loading}
            >
              📷 Start Camera
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => fileInputRef.current.click()}
              disabled={loading}
            >
              📁 Upload Image
            </button>
            <input 
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
          </div>
        )}

        {cameraActive && (
          <div className="camera-view">
            <video 
              ref={videoRef}
              autoPlay
              playsInline
              muted
            />
            <canvas 
              ref={canvasRef}
              style={{ display: 'none' }}
              width={640}
              height={480}
            />
            <div className="camera-controls">
              <button 
                className="btn btn-success"
                onClick={capturePhoto}
                disabled={loading}
              >
                ✓ Capture
              </button>
              <button 
                className="btn btn-danger"
                onClick={stopCamera}
              >
                ✕ Cancel
              </button>
            </div>
          </div>
        )}

        {preview && !cameraActive && (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <div className="preview-controls">
              <button 
                className="btn btn-primary"
                onClick={handleReset}
              >
                ◀ Retake
              </button>
            </div>
            {loading && <p className="processing">Processing image...</p>}
          </div>
        )}
      </div>

      <div className="info-section">
        <h3>💡 Tips for Best Results</h3>
        <ul>
          <li>Ensure good lighting and clear view of the waste item</li>
          <li>Include the entire item in the frame</li>
          <li>Avoid shadows and reflections</li>
          <li>Clean the camera lens for better accuracy</li>
        </ul>
      </div>
    </div>
  );
}

export default CameraCapture;
