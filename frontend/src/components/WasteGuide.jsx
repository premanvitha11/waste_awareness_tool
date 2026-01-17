import React, { useState, useEffect } from 'react';
import '../styles/WasteGuide.css';

function WasteGuide({ region }) {
  const [tips, setTips] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetchTips();
  }, []);

  const fetchTips = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/tips`);
      const data = await response.json();
      setTips(data.tips || []);
    } catch (err) {
      console.error('Error fetching tips:', err);
      // Fallback tips
      setTips([
        {
          title: 'Segregate at Source',
          description: 'Keep recyclable, organic, and hazardous waste separate from the start',
          impact: 'Makes processing more efficient'
        },
        {
          title: 'Clean Your Recyclables',
          description: 'Rinse plastic, glass, and metal containers before recycling',
          impact: 'Reduces contamination, improves recycling quality'
        },
        {
          title: 'Compost Organic Waste',
          description: 'Use food and garden waste for composting to create soil',
          impact: 'Reduces methane emissions from landfills'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const wasteCategories = [
    {
      name: 'Recyclable',
      icon: '♻️',
      description: 'Materials that can be processed and made into new products',
      examples: ['Plastic', 'Paper', 'Glass', 'Metal']
    },
    {
      name: 'Organic',
      icon: '🌱',
      description: 'Biodegradable waste that can be composted',
      examples: ['Food waste', 'Garden waste', 'Paper products']
    },
    {
      name: 'Hazardous',
      icon: '⚠️',
      description: 'Requires special handling and disposal',
      examples: ['Batteries', 'Electronics', 'Chemicals']
    },
    {
      name: 'Mixed',
      icon: '🔀',
      description: 'Multi-material items requiring special treatment',
      examples: ['Clothing', 'Ceramics', 'Contaminated items']
    }
  ];

  return (
    <div className="waste-guide">
      <h2>Waste Segregation Guide</h2>
      <p className="subtitle">Learn how to properly classify and dispose of different waste types</p>

      <div className="categories-grid">
        {wasteCategories.map((category) => (
          <div 
            key={category.name}
            className={`category-card ${selectedCategory === category.name ? 'selected' : ''}`}
            onClick={() => setSelectedCategory(category.name)}
          >
            <h3>{category.icon} {category.name}</h3>
            <p>{category.description}</p>
            <div className="examples">
              {category.examples.map((example) => (
                <span key={example} className="example-tag">{example}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="tips-section">
        <h3>💡 Segregation Tips</h3>
        {loading ? (
          <p>Loading tips...</p>
        ) : (
          <div className="tips-list">
            {tips.map((tip, idx) => (
              <div key={idx} className="tip-card">
                <h4>{tip.title}</h4>
                <p>{tip.description}</p>
                <div className="tip-impact">
                  <strong>Impact:</strong> {tip.impact}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="best-practices">
        <h3>✅ Best Practices</h3>
        <ul>
          <li><strong>Clean Before Recycling:</strong> Rinse containers to avoid contamination</li>
          <li><strong>Check Local Rules:</strong> Waste guidelines vary by region</li>
          <li><strong>Flatten Items:</strong> Save space by crushing boxes and bottles</li>
          <li><strong>Avoid Mixing:</strong> Keep hazardous items completely separate</li>
          <li><strong>Compost at Home:</strong> Start a compost bin for organic waste</li>
          <li><strong>Take E-Waste Seriously:</strong> Never throw electronics in trash</li>
        </ul>
      </div>
    </div>
  );
}

export default WasteGuide;
