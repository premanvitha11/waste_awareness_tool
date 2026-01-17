import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import CameraCapture from './components/CameraCapture';
import ClassificationResult from './components/ClassificationResult';
import WasteGuide from './components/WasteGuide';
import RegulationsPanel from './components/RegulationsPanel';

function App() {
  const [classificationResult, setClassificationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedRegion, setSelectedRegion] = useState('general');
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('capture');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleImageCapture = async (imageData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/classify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: imageData,
          region: selectedRegion
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const result = await response.json();
      setClassificationResult(result);
      setActiveTab('result');
    } catch (err) {
      setError(err.message || 'Failed to classify image');
      console.error('Classification error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setClassificationResult(null);
    setActiveTab('capture');
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>♻️ AI Waste Sorting Awareness Tool</h1>
          <p className="tagline">Classify waste. Learn disposal methods. Support SDG 11 & 12.</p>
        </div>
        
        <div className="region-selector">
          <label htmlFor="region">Your Region:</label>
          <select 
            id="region" 
            value={selectedRegion} 
            onChange={(e) => setSelectedRegion(e.target.value)}
          >
            <option value="general">General</option>
            <option value="USA">USA</option>
            <option value="EU">European Union</option>
            <option value="India">India</option>
            <option value="China">China</option>
          </select>
        </div>
      </header>

      <nav className="navigation">
        <button 
          className={`nav-button ${activeTab === 'capture' ? 'active' : ''}`}
          onClick={() => setActiveTab('capture')}
        >
          📸 Capture
        </button>
        <button 
          className={`nav-button ${activeTab === 'result' ? 'active' : ''}`}
          onClick={() => setActiveTab('result')}
          disabled={!classificationResult}
        >
          📊 Results
        </button>
        <button 
          className={`nav-button ${activeTab === 'guide' ? 'active' : ''}`}
          onClick={() => setActiveTab('guide')}
        >
          📖 Waste Guide
        </button>
        <button 
          className={`nav-button ${activeTab === 'regulations' ? 'active' : ''}`}
          onClick={() => setActiveTab('regulations')}
        >
          ⚖️ Regulations
        </button>
      </nav>

      <main className="main-content">
        {error && (
          <div className="error-message">
            <span>{error}</span>
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {loading && (
          <div className="loading-spinner">
            <div className="spinner"></div>
            <p>Analyzing your waste...</p>
          </div>
        )}

        {activeTab === 'capture' && (
          <section className="tab-content">
            <CameraCapture 
              onImageCapture={handleImageCapture}
              loading={loading}
            />
          </section>
        )}

        {activeTab === 'result' && classificationResult && (
          <section className="tab-content">
            <ClassificationResult 
              result={classificationResult}
              onReset={handleReset}
            />
          </section>
        )}

        {activeTab === 'guide' && (
          <section className="tab-content">
            <WasteGuide region={selectedRegion} />
          </section>
        )}

        {activeTab === 'regulations' && (
          <section className="tab-content">
            <RegulationsPanel region={selectedRegion} />
          </section>
        )}
      </main>

      <footer className="App-footer">
        <div className="sdg-impact">
          <h3>UN Sustainable Development Goals</h3>
          <div className="sdg-cards">
            <div className="sdg-card sdg-11">
              <h4>SDG 11</h4>
              <p>Sustainable Cities and Communities</p>
            </div>
            <div className="sdg-card sdg-12">
              <h4>SDG 12</h4>
              <p>Responsible Consumption and Production</p>
            </div>
          </div>
        </div>
        <p>&copy; 2026 AI Waste Awareness Tool. Supporting sustainable practices globally.</p>
      </footer>
    </div>
  );
}

export default App;
