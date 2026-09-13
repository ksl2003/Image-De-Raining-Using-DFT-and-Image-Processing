import React from 'react';
import './ImageDisplay.css';

const ImageDisplay = ({ images }) => {
  const handleDownload = (imageData, filename) => {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="image-display">
      <h2 className="display-title">Processing results</h2>
      {images?.processingMode === 'dft' && (
        <p className="processing-note">Processed with directional DFT rain filtering and edge sharpening.</p>
      )}
      <div className="images-container">
        <div className="image-card">
          <h3 className="image-card-title">Original</h3>
          <div className="image-wrapper">
            {images ? <img src={images.original} alt="Original rainy scene" className="result-image" /> : <p>Original image preview</p>}
          </div>
        </div>
        <div className="image-card">
          <h3 className="image-card-title">De-rained Result</h3>
          <div className="image-wrapper">
            {images ? <img src={images.derained} alt="Processed scene with reduced rain" className="result-image" /> : <p>Processed image preview</p>}
          </div>
          {images && <button onClick={() => handleDownload(images.derained, 'derained-result.png')} className="download-btn">Download Result</button>}
        </div>
      </div>
    </div>
  );
};

export default ImageDisplay;

