# System Architecture

## Overview

The AI Waste Sorting Awareness Tool is built with a modern, scalable microservices architecture consisting of a React frontend and Python Flask backend.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Device                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          React.js Web Application (Port 3000)        │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Camera/Upload Interface                        │ │  │
│  │  │  - Capture images from device camera           │ │  │
│  │  │  - Upload images from device storage           │ │  │
│  │  │  - Preview and crop functionality              │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  UI Components                                  │ │  │
│  │  │  - ClassificationResult: Display predictions   │ │  │
│  │  │  - WasteGuide: Educational content             │ │  │
│  │  │  - RegulationsPanel: Regional guidelines       │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       ↓
┌──────────────────────────────────────────────────────────────┐
│              Flask Backend API (Port 5000)                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  API Endpoints                                         │  │
│  │  ├─ POST /classify          (Waste classification)     │  │
│  │  ├─ GET /regulations        (Regional guidelines)      │  │
│  │  ├─ GET /waste-categories   (Supported categories)     │  │
│  │  ├─ GET /tips              (Segregation guidance)      │  │
│  │  └─ POST /feedback         (User feedback)             │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Image Processing Layer                                │  │
│  │  ├─ Base64 decode & validation                        │  │
│  │  ├─ Image format conversion                           │  │
│  │  └─ Preprocessing & normalization                     │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Waste Classification Model                            │  │
│  │  ├─ Architecture: ResNet50 with Transfer Learning      │  │
│  │  ├─ Input: 224x224 RGB image                          │  │
│  │  ├─ Output: Classification + Confidence score         │  │
│  │  └─ Classes: [plastic, paper, glass, metal,           │  │
│  │              organic, hazardous]                       │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  RAG (Retrieval-Augmented Generation) System           │  │
│  │  ├─ Vector Database (FAISS)                           │  │
│  │  │  └─ Embeddings: HuggingFace Sentence Transformers  │  │
│  │  ├─ Knowledge Base                                     │  │
│  │  │  ├─ Waste disposal guidelines                       │  │
│  │  │  ├─ Regional regulations                            │  │
│  │  │  └─ Environmental impact data                       │  │
│  │  └─ LLM Integration Ready                              │  │
│  │     └─ For advanced guidance (future)                  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend (React.js)

```
src/
├── App.jsx                          # Main application component
│   └── State: classificationResult, loading, selectedRegion
│   └── Routes: capture, result, guide, regulations tabs
│
├── components/
│   ├── CameraCapture.jsx            # Camera & upload interface
│   │   ├── Video stream management
│   │   ├── Canvas-based photo capture
│   │   └── File upload handling
│   │
│   ├── ClassificationResult.jsx     # Display classification output
│   │   ├── Category badge with color coding
│   │   ├── Confidence meter visualization
│   │   ├── Top predictions list
│   │   └── Disposal guide display
│   │
│   ├── WasteGuide.jsx               # Educational content
│   │   ├── Waste category cards (clickable)
│   │   ├── Segregation tips
│   │   └── Best practices list
│   │
│   └── RegulationsPanel.jsx         # Regional regulations
│       ├─ Fetch regulations by region
│       ├─ Display category-specific rules
│       └─ Resource links
│
├── styles/
│   ├── App.css                      # Main app styles
│   ├── CameraCapture.css
│   ├── ClassificationResult.css
│   ├── WasteGuide.css
│   └── RegulationsPanel.css
│
└── index.jsx                        # React entry point
```

### Backend (Flask)

```
backend/
├── app.py                           # Main Flask application
│   ├── CORS configuration
│   ├── Route definitions
│   ├── Error handling
│   └── Request/response processing
│
├── waste_classifier.py              # ML Model wrapper
│   ├── WasteClassifier class
│   ├── Model loading (ResNet50)
│   ├── Image preprocessing
│   ├── Inference logic
│   └── Confidence calculation
│
├── rag_system/
│   ├── __init__.py
│   └── waste_rag.py                 # RAG system
│       ├── WasteRAG class
│       ├── Knowledge base loading
│       ├── Vector database operations
│       ├── Regulation retrieval
│       └── Disposal guidance generation
│
└── models/                          # Pre-trained weights
    └── resnet50_waste_classifier.pth
```

## Data Flow

### Classification Workflow

```
1. User captures/uploads image
   ↓
2. Image converted to Base64
   ↓
3. Send POST /classify with Base64 + region
   ↓
4. Backend receives request
   ├─ Decode Base64 → PIL Image
   ├─ Validate image format
   └─ Convert to RGB if needed
   ↓
5. Waste Classifier processes image
   ├─ Resize to 224x224
   ├─ Normalize with ImageNet stats
   ├─ Run inference through ResNet50
   ├─ Get softmax probabilities
   └─ Extract top predictions
   ↓
6. RAG System provides guidance
   ├─ Retrieve disposal guidelines for waste_type
   ├─ Get regulations for region + category
   └─ Compile environmental impact data
   ↓
7. Format response with:
   ├─ classification (recyclable/organic/hazardous/mixed)
   ├─ waste_type (plastic/paper/glass/etc)
   ├─ confidence score (0-1)
   ├─ top_predictions list
   ├─ disposal_guide
   ├─ regulations
   └─ sdg_impact
   ↓
8. Send JSON response to frontend
   ↓
9. Frontend displays results in ClassificationResult component
   ├─ Color-coded category badge
   ├─ Confidence meter
   ├─ Disposal instructions
   ├─ Regional regulations
   └─ SDG impact info
```

### Regulations Query Workflow

```
1. User selects region in header
   ↓
2. Frontend calls GET /regulations?region=USA&waste_type=plastic
   ↓
3. Backend RAG system retrieves:
   ├─ Regional regulations from database
   ├─ Category-specific guidelines
   └─ Compliance standards
   ↓
4. Format response with region-specific rules
   ↓
5. Frontend displays in RegulationsPanel
```

## Technology Stack

### Frontend
- **Framework**: React 18+
- **Styling**: CSS3 (no external UI framework)
- **APIs**: Fetch API, Camera API, File API
- **Build**: Create React App
- **Deployment**: Static hosting (Vercel, Netlify, etc.)

### Backend
- **Framework**: Flask 2.3+
- **CORS**: Flask-CORS
- **ML Framework**: PyTorch
- **Vision**: Torchvision (pre-trained models)
- **Image Processing**: Pillow
- **NLP**: Langchain, Sentence Transformers
- **Vector DB**: FAISS
- **Environment**: python-dotenv

### Data & Models
- **Model Type**: Transfer Learning (ResNet50)
- **Dataset**: COCO (pre-trained), fine-tuned on waste images
- **Vector Embeddings**: Sentence-BERT (384-dimensional)
- **Storage**: File-based (scalable to cloud)

## Security Architecture

```
┌─────────────────────────────────────┐
│  Frontend Security                   │
├─────────────────────────────────────┤
│ ✓ Client-side image validation      │
│ ✓ No sensitive data in localStorage │
│ ✓ HTTPS-only in production          │
│ ✓ CORS enforcement                  │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  API Security                        │
├─────────────────────────────────────┤
│ ✓ Input validation & sanitization   │
│ ✓ Image size limits (10MB max)      │
│ ✓ Error handling (no stack traces)  │
│ ✓ Logging for audit trail           │
│ TODO: API authentication             │
│ TODO: Rate limiting                  │
│ TODO: Request signing                │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Model Security                      │
├─────────────────────────────────────┤
│ ✓ Model weights versioning          │
│ ✓ Input sanitization                │
│ ✓ Output validation                 │
│ TODO: Model encryption               │
│ TODO: Adversarial robustness testing │
└─────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- **Frontend**: Static files, CDN distribution
- **Backend**: Load balancer + multiple Flask instances
- **Database**: Cloud storage for regulations, Vector DB in cloud

### Performance Optimization
- **Model**: Quantization, ONNX optimization
- **API**: Caching, response compression
- **Frontend**: Code splitting, lazy loading
- **Images**: Compression before transmission

### Future Enhancements
```
Phase 1 (Current): Single-tier, local deployment
Phase 2: Cloud deployment with auto-scaling
Phase 3: Advanced caching with Redis
Phase 4: Distributed inference with model serving
Phase 5: Real-time analytics & monitoring
```

## Error Handling Strategy

```
Frontend:
├─ Network errors → User-friendly message
├─ Image validation → Retry/reupload prompt
└─ API errors → Display error + suggest fix

Backend:
├─ Invalid image → 400 Bad Request
├─ Model error → 500 Internal Server Error
├─ Rate limit → 429 Too Many Requests
└─ Logging → All errors logged for debugging
```

## Deployment Architecture

### Development
```
localhost:3000 (Frontend) ←→ localhost:5000 (Backend)
```

### Production (Docker)
```
Docker Compose:
├─ waste-frontend (port 3000)
├─ waste-backend (port 5000)
└─ Shared network for internal communication
```

### Cloud Deployment (Future)
```
┌──────────────────────────────────────┐
│  CDN / Load Balancer                 │
└────────────┬─────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │  Frontend Container      │
  │  (Static React build)    │
  └──────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │  Backend Container Cluster │
  │  (Flask + model)         │
  └──────────────────────────┘
             ↓
  ┌──────────────────────────┐
  │  Cloud Storage           │
  │  (Models, regulations)   │
  └──────────────────────────┘
```

## Monitoring & Logging

```
Backend Logging:
├─ Classification requests
├─ Model inference time
├─ API response times
├─ Error tracking
└─ User feedback submission

Metrics to Track:
├─ Model accuracy
├─ API response time
├─ Error rate
├─ User engagement
└─ Regional usage patterns
```

---

This architecture enables:
- ✅ Fast image classification (200-500ms)
- ✅ Regional compliance & regulations
- ✅ Easy feature additions
- ✅ Scalable to millions of users
- ✅ Integration with future AI models
- ✅ Support for SDG monitoring
