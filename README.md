# AI Waste Sorting Awareness Tool

An intelligent waste classification system that uses computer vision and RAG (Retrieval-Augmented Generation) to help people properly segregate waste and learn about disposal guidelines based on local regulations.

## 🌍 Problem Statement

**Challenge:** People globally don't know how to properly segregate waste, leading to contamination of recyclables, improper hazardous disposal, and wasted resources.

**Solution:** Use AI-powered image recognition to classify waste items in real-time and provide context-aware disposal guidance through a Retrieval-Augmented Generation system that knows local regulations.

## 🎯 Features

### Core Functionality
- **📸 Real-time Waste Classification**: Camera/image upload for instant waste identification
- **♻️ Multi-category Classification**: Classifies waste as Recyclable, Organic, Hazardous, or Mixed
- **🌍 Regional Awareness**: Provides disposal guidelines based on local regulations (USA, EU, India, China, General)
- **📖 RAG-based Guidance**: Uses LLM with waste regulation database for accurate disposal instructions
- **💡 Segregation Tips**: Contextual tips for proper waste handling
- **📊 Confidence Scores**: Shows model confidence and alternative classifications

### SDG Support
- **SDG 11** - Sustainable Cities and Communities
- **SDG 12** - Responsible Consumption and Production

## 🏗️ Project Architecture

```
AI waste awareness tool/
├── frontend/                    # React.js UI
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── CameraCapture.jsx
│   │   │   ├── ClassificationResult.jsx
│   │   │   ├── WasteGuide.jsx
│   │   │   └── RegulationsPanel.jsx
│   │   ├── styles/             # Component CSS
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── .env.example
│
├── backend/                     # Flask API
│   ├── app.py                  # Main Flask application
│   ├── waste_classifier.py     # Image classification model
│   ├── rag_system/
│   │   ├── waste_rag.py        # RAG implementation
│   │   └── __init__.py
│   ├── models/                 # Pre-trained model weights
│   ├── requirements.txt
│   └── .env.example
│
├── data/                        # Data files
│   └── waste_regulations/      # Regional regulation database
│
├── docs/                        # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   └── ARCHITECTURE.md
│
├── README.md
├── docker-compose.yml
└── Dockerfile
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run Flask server
python app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env

# Start development server
npm start
```

The app will be available at `http://localhost:3000`

## 📡 API Endpoints

### POST `/classify`
Classify waste from an image

**Request:**
```json
{
  "image": "base64_encoded_image",
  "region": "USA"
}
```

**Response:**
```json
{
  "classification": "recyclable",
  "waste_type": "plastic_bottle",
  "confidence": 0.95,
  "top_predictions": [...],
  "disposal_guide": {...},
  "regulations": {...},
  "sdg_impact": {...}
}
```

### GET `/regulations?region=USA&waste_type=plastic`
Get waste regulations for a region

### GET `/tips?type=plastic`
Get waste segregation tips

### GET `/waste-categories`
Get all supported waste categories

## 🤖 AI/ML Components

### Waste Classification Model
- **Architecture**: ResNet50 with transfer learning
- **Training Data**: Waste image dataset (placeholder)
- **Classes**: plastic, paper, glass, metal, organic, hazardous
- **Performance**: Real-time inference with confidence scores

### RAG System
- **Vector Database**: FAISS with HuggingFace embeddings
- **Knowledge Base**: Comprehensive waste regulations database
- **LLM Integration**: Ready for OpenAI/Claude integration
- **Coverage**: USA, EU, India, China, and General guidelines

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tab-based Navigation**: Capture, Results, Guide, Regulations
- **Real-time Camera Access**: Native camera API support
- **Visual Feedback**: Progress indicators and confidence meters
- **Accessible Design**: WCAG compliant color schemes
- **Mobile-first Approach**: Optimized for smartphone use

## 🔬 Waste Categories

### Recyclable
- Plastic (bottles, containers, bags)
- Paper (newspapers, cardboard, magazines)
- Glass (clear, brown, green)
- Metal (aluminum, steel, tin)

### Organic
- Food waste (fruits, vegetables, meat)
- Garden waste (leaves, grass, branches)
- Paper products (napkins, plates)

### Hazardous
- Batteries (alkaline, lithium)
- Electronics (phones, computers, cables)
- Chemicals and flammable materials

### Mixed
- Textiles (clothing, shoes)
- Ceramics (plates, pottery)
- Multi-material composite items

## 📚 Regional Regulations Supported

- **General**: Universal waste management principles
- **USA**: EPA guidelines and state-specific rules
- **EU**: EU Waste Directive and member state regulations
- **India**: Swachh Bharat Mission and SWM Rules 2016
- **China**: Solid Waste Law and classification standards

## 🔧 Configuration

### Backend (.env)
```env
FLASK_ENV=development
FLASK_PORT=5000
MODEL_PATH=models/resnet50_waste_classifier.pth
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📦 Dependencies

### Backend
- Flask & Flask-CORS
- PyTorch & Torchvision
- Langchain
- Pillow
- python-dotenv

### Frontend
- React 18+
- CSS3 (no framework needed)
- Native Camera API

## 🧪 Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:3000
```

## 🎓 Use Cases

### For Individuals
- Learn proper waste segregation habits
- Identify waste items instantly with camera
- Understand local disposal requirements

### For Educators
- Teaching waste management and sustainability
- Demonstrating real-world SDG impact
- Interactive learning tool for students

### For Communities
- Awareness campaigns at local level
- Training waste management workers
- Improving community recycling rates

### For Businesses
- Training employees on waste management
- Monitoring corporate sustainability goals
- Reducing landfill waste and costs

## 📈 Metrics & Impact

- **Environmental**: Reduced contamination, improved recycling efficiency
- **Social**: Increased awareness and behavior change
- **Economic**: Lower waste management costs, resource recovery
- **UN SDGs**: Direct support for SDG 11 & 12

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Expand waste classification categories
- Add more regional regulations
- Improve model accuracy with more training data
- Multi-language support
- Community feedback integration
- Mobile app versions (React Native, Flutter)

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- UN Sustainable Development Goals framework
- Waste management experts and researchers
- Open-source ML/AI community
- Environmental organizations

## 📞 Support & Contact

For questions, issues, or suggestions:
- Create an issue in the repository
- Contact: [Your Contact]
- Website: [Your Website]

## 🔮 Future Roadmap

- [ ] Mobile app (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] Multi-item detection
- [ ] AR visualization of disposal methods
- [ ] Gamification & rewards system
- [ ] Integration with waste collection services
- [ ] Voice-guided instructions
- [ ] Offline mode support
- [ ] Advanced ML model optimization
- [ ] Community-sourced training data

---

**Built with ❤️ for a sustainable future**
