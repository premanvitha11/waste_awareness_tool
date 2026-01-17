import React, { useState, useEffect } from 'react';
import '../styles/RegulationsPanel.css';

function RegulationsPanel({ region }) {
  const [regulations, setRegulations] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetchRegulations();
  }, [region]);

  const fetchRegulations = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/regulations?region=${region}`
      );
      const data = await response.json();
      setRegulations(data);
    } catch (err) {
      console.error('Error fetching regulations:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="regulations-panel"><p>Loading regulations...</p></div>;
  }

  return (
    <div className="regulations-panel">
      <h2>Waste Regulations & Guidelines</h2>
      <p className="region-info">📍 Showing regulations for: <strong>{region}</strong></p>

      {regulations && regulations.regulations && (
        <div className="regulations-content">
          <div className="regulation-section">
            <div className="reg-card">
              <h3>♻️ Recyclable Waste</h3>
              <p>{regulations.regulations.recyclable}</p>
            </div>

            <div className="reg-card">
              <h3>🌱 Organic Waste</h3>
              <p>{regulations.regulations.organic}</p>
            </div>

            <div className="reg-card">
              <h3>⚠️ Hazardous Waste</h3>
              <p>{regulations.regulations.hazardous}</p>
            </div>

            {regulations.regulations.fines && (
              <div className="reg-card warning">
                <h3>⚖️ Important Notice</h3>
                <p>{regulations.regulations.fines}</p>
              </div>
            )}

            {regulations.regulations.standards && (
              <div className="reg-card info">
                <h3>📋 Compliance Standards</h3>
                <p>{regulations.regulations.standards}</p>
              </div>
            )}
          </div>

          <div className="action-section">
            <h3>Need More Information?</h3>
            <div className="resource-links">
              <a href="#" className="resource-link">📞 Contact Local Waste Management</a>
              <a href="#" className="resource-link">🌐 Official Guidelines</a>
              <a href="#" className="resource-link">🗺️ Find Nearby Recycling Centers</a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default RegulationsPanel;
