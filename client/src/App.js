import React, { useState } from "react";
import "./App.css";
import ImageUploader from "./components/ImageUploader";
import ImageDisplay from "./components/ImageDisplay";
import History from "./components/History";

function App() {
  const [processedImages, setProcessedImages] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  const handleImageProcessed = (data) => {
    setProcessedImages(data);
    setError(null);
  };

  const handleError = (err) => {
    setError(err);
    setProcessedImages(null);
  };

  const handleLoading = (isLoading) => {
    setLoading(isLoading);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="brand">
          <strong>
            <span>Image De-Raining Tool</span>
          </strong>
        </div>
        <button
          className="history-btn"
          onClick={() => setShowHistory(!showHistory)}
        >
          {showHistory ? "Back to workspace" : "History"}
        </button>
      </header>

      <main className="App-main">
        <div className="container">
          {showHistory ? (
            <History />
          ) : (
            <>
              <section className="intro">
                <h1>Image De-raining</h1>
                <p>Clear the rain. Keep the moment.</p>
              </section>
              <ImageUploader
                onImageProcessed={handleImageProcessed}
                onError={handleError}
                onLoading={handleLoading}
                loading={loading}
              />

              {error && (
                <div className="error-message" role="alert">
                  <p>{error}</p>
                </div>
              )}

              <ol
                className="process-steps"
                aria-label="How image processing works"
              >
                <li>
                  <span>1</span>
                  <div>
                    <strong>Choose a rainy image</strong>
                    <small>Upload your photo</small>
                  </div>
                </li>
                <li>
                  <span>2</span>
                  <div>
                    <strong>Process image</strong>
                    <small>Remove rain patterns</small>
                  </div>
                </li>
                <li>
                  <span>3</span>
                  <div>
                    <strong>See the difference</strong>
                    <small>Compare and download</small>
                  </div>
                </li>
              </ol>
              <ImageDisplay images={processedImages} />
            </>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Kolli Surya Lakshman © All Rights Reserved</p>
      </footer>
    </div>
  );
}

export default App;
