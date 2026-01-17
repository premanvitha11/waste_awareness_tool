# API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Waste Sorting Tool",
  "version": "1.0.0"
}
```

---

### 2. Classify Waste
**POST** `/classify`

Classify waste from an image.

**Request Body:**
```json
{
  "image": "base64_encoded_image_string",
  "region": "USA"
}
```

**Parameters:**
- `image` (required): Base64 encoded image
- `region` (optional): Geographic region (default: 'general')
  - Values: 'general', 'USA', 'EU', 'India', 'China'

**Response:**
```json
{
  "classification": "recyclable",
  "waste_type": "plastic_bottle",
  "confidence": 0.95,
  "top_predictions": [
    {
      "waste_type": "plastic",
      "confidence": 0.95
    },
    {
      "waste_type": "metal",
      "confidence": 0.04
    },
    {
      "waste_type": "glass",
      "confidence": 0.01
    }
  ],
  "disposal_guide": {
    "waste_type": "plastic",
    "category": "recyclable",
    "disposal_steps": [
      "Rinse the bottle before recycling",
      "Remove caps and labels",
      "Place in recycling bin"
    ],
    "environmental_impact": "Takes 400+ years to decompose in nature",
    "recycling_info": "Sorted, shredded, melted, and reformed into new products",
    "subtypes": ["HDPE", "LDPE", "PET", "PVC", "PP"]
  },
  "regulations": {
    "region": "USA",
    "waste_type": "plastic",
    "category": "recyclable",
    "specific_regulations": "Follow local curbside guidelines. Check municipality for accepted materials.",
    "general_regulations": {...}
  },
  "sdg_impact": {
    "SDG_11": "Sustainable Cities and Communities",
    "SDG_12": "Responsible Consumption and Production"
  }
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request (no image)
- 500: Server error

---

### 3. Get Regulations
**GET** `/regulations`

Get waste regulations for a specific region.

**Query Parameters:**
- `region` (optional): Geographic region (default: 'general')
- `waste_type` (optional): Specific waste type

**Example:**
```
GET /regulations?region=USA&waste_type=plastic
```

**Response:**
```json
{
  "region": "USA",
  "waste_type": "plastic",
  "category": "recyclable",
  "specific_regulations": "Follow local curbside guidelines...",
  "general_regulations": {
    "recyclable": "...",
    "organic": "...",
    "hazardous": "..."
  }
}
```

---

### 4. Get Waste Categories
**GET** `/waste-categories`

Get all supported waste categories and types.

**Response:**
```json
{
  "categories": {
    "recyclable": {
      "types": ["plastic", "paper", "glass", "metal"],
      "description": "Can be processed and made into new products"
    },
    "organic": {
      "types": ["food", "garden", "paper"],
      "description": "Biodegradable waste that can be composted"
    },
    "hazardous": {
      "types": ["batteries", "chemicals", "electronics"],
      "description": "Requires special handling and disposal"
    },
    "mixed": {
      "types": ["multi-material", "contaminated"],
      "description": "Mixed waste requiring special treatment"
    }
  },
  "total": 4
}
```

---

### 5. Get Segregation Tips
**GET** `/tips`

Get waste segregation tips.

**Query Parameters:**
- `type` (optional): Specific waste type

**Response:**
```json
{
  "tips": [
    {
      "title": "How to Dispose Plastic",
      "description": "Place in recycling bin. Rinse before recycling.",
      "impact": "Reduces contamination, improves recycling quality"
    },
    {
      "title": "Segregate at Source",
      "description": "Keep recyclable, organic, and hazardous waste separate...",
      "impact": "Makes processing more efficient"
    }
  ]
}
```

---

### 6. Submit Feedback
**POST** `/feedback`

Submit feedback for model improvement.

**Request Body:**
```json
{
  "image_id": "unique_image_id",
  "predicted_class": "plastic",
  "actual_class": "plastic",
  "confidence": 0.95
}
```

**Response:**
```json
{
  "status": "feedback_recorded",
  "message": "Thank you for your feedback!"
}
```

---

## Error Handling

### Error Response Format
```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 400 | No image provided | Ensure image is included in request |
| 400 | Invalid image format | Use JPEG or PNG format |
| 500 | Classifier not initialized | Restart the service |
| 500 | Classification failed | Check image quality and try again |

---

## Integration Examples

### JavaScript/Fetch API
```javascript
async function classifyWaste(imageBase64) {
  const response = await fetch('http://localhost:5000/classify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      image: imageBase64,
      region: 'USA'
    })
  });
  
  const result = await response.json();
  console.log(result);
}
```

### Python/Requests
```python
import requests
import base64

with open('waste_image.jpg', 'rb') as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode()

response = requests.post(
    'http://localhost:5000/classify',
    json={
        'image': image_base64,
        'region': 'USA'
    }
)

result = response.json()
print(result)
```

### cURL
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64_image_string",
    "region": "USA"
  }'
```

---

## Rate Limiting

Currently, no rate limiting is implemented. This should be added for production deployments.

## Authentication

Currently, no authentication is required. For production, add:
- API key authentication
- OAuth 2.0
- JWT tokens

## Performance

- Average classification time: 200-500ms
- Image processing: Up to 10MB
- Concurrent requests: Limited by server resources

---

## Version History

- **v1.0.0** (2024): Initial release with core features
