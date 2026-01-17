"""
Waste Classification Module using pre-trained models
Classifies waste into categories: Recyclable, Organic, Hazardous, Mixed
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
from PIL import Image
import logging
from typing import Dict, Tuple
import os

logger = logging.getLogger(__name__)


class WasteClassifier:
    """
    Waste classification model using transfer learning
    Supported waste types: plastic, paper, glass, metal, food, hazardous, etc.
    """
    
    def __init__(self, model_name: str = 'resnet50', num_classes: int = 6):
        """
        Initialize waste classifier
        
        Args:
            model_name: Pre-trained model to use
            num_classes: Number of waste categories
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_classes = num_classes
        
        # Class mappings
        self.class_names = [
            'plastic',
            'paper',
            'glass',
            'metal',
            'organic',
            'hazardous'
        ]
        
        # Category mapping
        self.category_mapping = {
            'plastic': 'recyclable',
            'paper': 'recyclable',
            'glass': 'recyclable',
            'metal': 'recyclable',
            'organic': 'organic',
            'hazardous': 'hazardous'
        }
        
        # Load model
        self.model = self._load_model(model_name)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        logger.info(f"Waste Classifier initialized with {model_name}")
    
    def _load_model(self, model_name: str) -> nn.Module:
        """Load pre-trained model with custom classification head"""
        try:
            if model_name == 'resnet50':
                # Load without weights first to avoid SSL issues
                try:
                    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
                except Exception as e:
                    logger.warning(f"Could not load ImageNet weights: {e}. Using uninitialized weights.")
                    model = models.resnet50(weights=None)
                
                num_features = model.fc.in_features
                model.fc = nn.Linear(num_features, self.num_classes)
            
            elif model_name == 'mobilenet':
                # Load without weights first to avoid SSL issues
                try:
                    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
                except Exception as e:
                    logger.warning(f"Could not load ImageNet weights: {e}. Using uninitialized weights.")
                    model = models.mobilenet_v2(weights=None)
                
                model.classifier[1] = nn.Linear(1280, self.num_classes)
            else:
                raise ValueError(f"Model {model_name} not supported")
            
            model = model.to(self.device)
            
            # Try to load pre-trained waste classifier weights
            model_path = f'models/{model_name}_waste_classifier.pth'
            if os.path.exists(model_path):
                try:
                    state_dict = torch.load(model_path, map_location=self.device)
                    model.load_state_dict(state_dict)
                    logger.info(f"Loaded pre-trained weights from {model_path}")
                except Exception as e:
                    logger.warning(f"Could not load weights from {model_path}: {e}")
            else:
                logger.info(f"Pre-trained waste classifier weights not found at {model_path}")
            
            return model
        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def classify(self, image: Image.Image) -> Dict:
        """
        Classify waste in an image
        
        Args:
            image: PIL Image object
        
        Returns:
            Dictionary with classification results
        """
        try:
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
            
            class_idx = predicted_class.item()
            waste_type = self.class_names[class_idx]
            category = self.category_mapping[waste_type]
            conf_score = float(confidence.item())
            
            # Get top-3 predictions
            top3_probs, top3_indices = torch.topk(probabilities[0], 3)
            top_predictions = [
                {
                    'waste_type': self.class_names[idx],
                    'confidence': float(prob)
                }
                for prob, idx in zip(top3_probs, top3_indices)
            ]
            
            return {
                'classification': category,
                'waste_type': waste_type,
                'confidence': conf_score,
                'top_predictions': top_predictions,
                'model_version': '1.0.0'
            }
        
        except Exception as e:
            logger.error(f"Classification error: {e}")
            raise
    
    def get_supported_categories(self) -> Dict:
        """Get all supported waste categories"""
        return {
            'recyclable': {
                'types': ['plastic', 'paper', 'glass', 'metal'],
                'description': 'Can be processed and made into new products'
            },
            'organic': {
                'types': ['food', 'garden', 'paper'],
                'description': 'Biodegradable waste that can be composted'
            },
            'hazardous': {
                'types': ['batteries', 'chemicals', 'electronics'],
                'description': 'Requires special handling and disposal'
            },
            'mixed': {
                'types': ['multi-material', 'contaminated'],
                'description': 'Mixed waste requiring special treatment'
            }
        }
