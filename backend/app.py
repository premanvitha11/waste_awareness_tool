"""
AI Waste Sorting Awareness Tool - Backend API
Supports waste classification with RAG-based waste regulations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import numpy as np
from waste_classifier import WasteClassifier
from rag_system.waste_rag import WasteRAG
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the waste classifier and RAG system
try:
    classifier = WasteClassifier()
    rag_system = WasteRAG()
    logger.info("Waste classifier and RAG system initialized successfully")
except Exception as e:
    logger.error(f"Error initializing systems: {e}")
    classifier = None
    rag_system = None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Waste Sorting Tool',
        'version': '1.0.0'
    }), 200


@app.route('/classify', methods=['POST'])
def classify_waste():
    """
    Classify waste from uploaded image
    
    Expects:
    {
        "image": "base64_encoded_image_string"
    }
    
    Returns:
    {
        "classification": "recyclable/organic/hazardous/mixed",
        "confidence": 0.95,
        "waste_type": "plastic_bottle",
        "disposal_guide": "...",
        "regulations": "..."
    }
    """
    try:
        if not classifier:
            return jsonify({
                'error': 'Classifier not initialized'
            }), 500
        
        data = request.json
        if not data or 'image' not in data:
            return jsonify({
                'error': 'No image provided'
            }), 400
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'])
            image = Image.open(io.BytesIO(image_data))
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as e:
            logger.error(f"Image decoding error: {e}")
            return jsonify({
                'error': 'Invalid image format'
            }), 400
        
        # Classify the waste
        classification_result = classifier.classify(image)
        
        # Get disposal guide using RAG
        disposal_guide = rag_system.get_disposal_guide(
            waste_type=classification_result['waste_type'],
            category=classification_result['classification']
        )
        
        # Get local regulations
        regulations = rag_system.get_regulations(
            waste_type=classification_result['waste_type'],
            region=data.get('region', 'general')
        )
        
        response = {
            **classification_result,
            'disposal_guide': disposal_guide,
            'regulations': regulations,
            'sdg_impact': {
                'SDG_11': 'Sustainable Cities and Communities',
                'SDG_12': 'Responsible Consumption and Production'
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return jsonify({
            'error': f'Classification failed: {str(e)}'
        }), 500


@app.route('/regulations', methods=['GET'])
def get_regulations():
    """
    Get waste regulations for a specific region
    
    Query params:
    - region: target region (default: 'general')
    - waste_type: specific waste type (optional)
    """
    try:
        if not rag_system:
            return jsonify({
                'error': 'RAG system not initialized'
            }), 500
        
        region = request.args.get('region', 'general')
        waste_type = request.args.get('waste_type', None)
        
        regulations = rag_system.get_regulations(waste_type, region)
        
        return jsonify({
            'region': region,
            'regulations': regulations
        }), 200
    
    except Exception as e:
        logger.error(f"Regulations retrieval error: {e}")
        return jsonify({
            'error': f'Failed to retrieve regulations: {str(e)}'
        }), 500


@app.route('/waste-categories', methods=['GET'])
def get_waste_categories():
    """Get all supported waste categories"""
    try:
        categories = classifier.get_supported_categories() if classifier else {}
        
        return jsonify({
            'categories': categories,
            'total': len(categories)
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({
            'error': 'Failed to fetch categories'
        }), 500


@app.route('/tips', methods=['GET'])
def get_tips():
    """Get waste segregation tips"""
    try:
        if not rag_system:
            return jsonify({
                'error': 'RAG system not initialized'
            }), 500
        
        waste_type = request.args.get('type', None)
        tips = rag_system.get_segregation_tips(waste_type)
        
        return jsonify({
            'tips': tips
        }), 200
    
    except Exception as e:
        logger.error(f"Error fetching tips: {e}")
        return jsonify({
            'error': 'Failed to fetch tips'
        }), 500


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback for classification accuracy improvement
    
    Expects:
    {
        "image_id": "...",
        "predicted_class": "...",
        "actual_class": "...",
        "confidence": 0.95
    }
    """
    try:
        data = request.json
        # Store feedback for model improvement
        logger.info(f"Feedback received: {data}")
        
        return jsonify({
            'status': 'feedback_recorded',
            'message': 'Thank you for your feedback!'
        }), 200
    
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        return jsonify({
            'error': 'Failed to submit feedback'
        }), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
