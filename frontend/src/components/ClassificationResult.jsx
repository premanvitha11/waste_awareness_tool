import React from 'react';
import '../styles/ClassificationResult.css';

function ClassificationResult({ result, onReset }) {
  const getCategoryColor = (category) => {
    switch(category) {
      case 'recyclable': return '#4CAF50';
      case 'organic': return '#8BC34A';
      case 'hazardous': return '#F44336';
      case 'mixed': return '#FF9800';
      default: return '#2196F3';
    }
  };

  const getCategoryIcon = (category) => {
    switch(category) {
      case 'recyclable': return '♻️';
      case 'organic': return '🌱';
      case 'hazardous': return '⚠️';
      case 'mixed': return '🔀';
      default: return '❓';
    }
  };

  return (
    <div className="classification-result">
      <div className="result-card">
        <div 
          className="category-badge"
          style={{ backgroundColor: getCategoryColor(result.classification) }}
        >
          <span className="badge-icon">{getCategoryIcon(result.classification)}</span>
          <span className="badge-text">{result.classification.toUpperCase()}</span>
        </div>

        <div className="result-details">
          <h2>{result.waste_type.replace('_', ' ').toUpperCase()}</h2>
          <div className="confidence-meter">
            <label>Confidence Score</label>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${result.confidence * 100}%` }}
              ></div>
            </div>
            <span className="confidence-text">{(result.confidence * 100).toFixed(1)}%</span>
          </div>
        </div>

        {result.top_predictions && result.top_predictions.length > 1 && (
          <div className="top-predictions">
            <h3>Other Possible Classifications</h3>
            <ul>
              {result.top_predictions.slice(1).map((pred, idx) => (
                <li key={idx}>
                  <span>{pred.waste_type}</span>
                  <span className="confidence">{(pred.confidence * 100).toFixed(1)}%</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="disposal-guide">
          <h3>♻️ How to Dispose</h3>
          {result.disposal_guide && (
            <div className="guide-content">
              <h4>Disposal Instructions</h4>
              <ul>
                {typeof result.disposal_guide.disposal_steps === 'string' 
                  ? [result.disposal_guide.disposal_steps]
                  : result.disposal_guide.disposal_steps || []
                }
              </ul>
              
              <div className="guide-info">
                <div className="info-item">
                  <h5>Environmental Impact</h5>
                  <p>{result.disposal_guide.environmental_impact}</p>
                </div>
                <div className="info-item">
                  <h5>Recycling Process</h5>
                  <p>{result.disposal_guide.recycling_info}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {result.regulations && (
          <div className="regulations-info">
            <h3>⚖️ Local Regulations</h3>
            <div className="reg-content">
              <p><strong>Region:</strong> {result.regulations.region}</p>
              <p><strong>Guidelines:</strong> {result.regulations.specific_regulations || 'Follow local waste management guidelines'}</p>
            </div>
          </div>
        )}

        {result.sdg_impact && (
          <div className="sdg-section">
            <h3>🌍 UN Sustainable Development Goals</h3>
            <div className="sdg-items">
              <div className="sdg-item">
                <span className="sdg-num">11</span>
                <span className="sdg-desc">{result.sdg_impact.SDG_11}</span>
              </div>
              <div className="sdg-item">
                <span className="sdg-num">12</span>
                <span className="sdg-desc">{result.sdg_impact.SDG_12}</span>
              </div>
            </div>
          </div>
        )}

        <div className="action-buttons">
          <button className="btn btn-primary" onClick={onReset}>
            📸 Classify Another Item
          </button>
          <button className="btn btn-secondary" onClick={() => {}}>
            👍 Helpful / Not Helpful
          </button>
        </div>
      </div>
    </div>
  );
}

export default ClassificationResult;
