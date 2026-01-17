"""
RAG (Retrieval-Augmented Generation) System for Waste Regulations
Uses LLM with retrieval of waste regulations to provide accurate disposal guidance
"""

import json
import os
from typing import Dict, List, Optional
import logging
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    from langchain.embeddings import HuggingFaceEmbeddings
try:
    from langchain_community.vectorstores import FAISS
except ImportError:
    from langchain.vectorstores import FAISS
import re

logger = logging.getLogger(__name__)


class WasteRAG:
    """RAG system for waste disposal guidance and regulations"""
    
    def __init__(self):
        """Initialize RAG system with waste regulations database"""
        self.waste_database = self._load_waste_database()
        self.regulations_db = self._load_regulations()
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("Waste RAG system initialized")
    
    def _load_waste_database(self) -> Dict:
        """Load waste database with disposal instructions"""
        database = {
            'plastic': {
                'category': 'recyclable',
                'subtypes': ['HDPE', 'LDPE', 'PET', 'PVC', 'PP'],
                'disposal': 'Place in recycling bin. Rinse before recycling.',
                'environmental_impact': 'Takes 400+ years to decompose in nature',
                'recycling_process': 'Sorted, shredded, melted, and reformed into new products'
            },
            'paper': {
                'category': 'recyclable',
                'subtypes': ['newspaper', 'cardboard', 'magazines', 'office_paper'],
                'disposal': 'Keep dry and place in paper recycling bin. Avoid contamination with food.',
                'environmental_impact': 'Biodegradable but recycling saves trees',
                'recycling_process': 'Pulped, cleaned, and formed into new paper products'
            },
            'glass': {
                'category': 'recyclable',
                'subtypes': ['clear', 'brown', 'green'],
                'disposal': 'Separate by color if required locally. Check for contamination.',
                'environmental_impact': 'Can be recycled infinitely without quality loss',
                'recycling_process': 'Melted and reformed into new glass containers'
            },
            'metal': {
                'category': 'recyclable',
                'subtypes': ['aluminum', 'steel', 'tin'],
                'disposal': 'Rinse cans. Place in recycling bin.',
                'environmental_impact': 'Aluminum recycling saves 95% energy vs. production',
                'recycling_process': 'Sorted, melted, and cast into new products'
            },
            'food_waste': {
                'category': 'organic',
                'subtypes': ['fruit', 'vegetables', 'meat', 'dairy'],
                'disposal': 'Compost if available. Otherwise, place in organic waste bin.',
                'environmental_impact': 'Produces methane in landfills; composting reduces emissions',
                'recycling_process': 'Composted to create nutrient-rich soil amendment'
            },
            'garden_waste': {
                'category': 'organic',
                'subtypes': ['leaves', 'grass', 'branches', 'flowers'],
                'disposal': 'Compost or green bin. Shred larger items.',
                'environmental_impact': 'Returns nutrients to soil when composted',
                'recycling_process': 'Shredded and composted into mulch'
            },
            'batteries': {
                'category': 'hazardous',
                'subtypes': ['alkaline', 'lithium', 'rechargeable'],
                'disposal': 'Take to battery collection center. Never throw in trash.',
                'environmental_impact': 'Heavy metals contaminate soil and water',
                'recycling_process': 'Separated by chemistry, smelted to recover metals'
            },
            'electronics': {
                'category': 'hazardous',
                'subtypes': ['phones', 'computers', 'TVs', 'cables'],
                'disposal': 'Take to e-waste recycling facility. Do not discard as trash.',
                'environmental_impact': 'Contains toxic materials and valuable metals',
                'recycling_process': 'Disassembled and sorted for material recovery'
            },
            'textiles': {
                'category': 'mixed',
                'subtypes': ['clothing', 'shoes', 'bags'],
                'disposal': 'Donate if usable. Otherwise, textile recycling programs.',
                'environmental_impact': 'Fast fashion contributes to 92 million tons waste/year',
                'recycling_process': 'Shredded into fibers or used in insulation'
            },
            'ceramics': {
                'category': 'mixed',
                'subtypes': ['plates', 'pots', 'tiles'],
                'disposal': 'Most ceramics go to landfill. Check local pottery/clay programs.',
                'environmental_impact': 'Non-biodegradable but stable in landfills',
                'recycling_process': 'Can be crushed for aggregate or pottery clay'
            }
        }
        return database
    
    def _load_regulations(self) -> Dict:
        """Load regional waste regulations"""
        regulations = {
            'general': {
                'recyclable': 'Should be cleaned and dry before recycling. Separate by material type if possible.',
                'organic': 'Home composting reduces methane emissions. Use in garden or compost bin.',
                'hazardous': 'Must be taken to special collection centers. Never mix with regular waste.',
                'fines': 'Illegal dumping can result in fines and penalties.'
            },
            'USA': {
                'recyclable': 'Follow local curbside guidelines. Check municipality for accepted materials.',
                'organic': 'Many states mandate organics composting. Find local programs via state database.',
                'hazardous': 'EPA regulates hazardous waste. Use Household Hazardous Waste facilities.',
                'standards': 'Follow EPA guidelines (40 CFR Part 261)'
            },
            'EU': {
                'recyclable': 'EU Waste Directive requires 55% recycling by 2025. Extended Producer Responsibility applies.',
                'organic': 'Bio-waste must be separately collected by 2023 per EU directive.',
                'hazardous': 'Basel Convention: hazardous waste cannot be exported to non-OECD countries.',
                'standards': 'Follow EN standards and CE marking requirements'
            },
            'India': {
                'recyclable': 'Swachh Bharat Mission promotes segregation at source.',
                'organic': 'Wet waste (biodegradable) must be segregated from dry waste.',
                'hazardous': 'Biomedical Waste Management Rules 2016 specify handling procedures.',
                'standards': 'Follow Solid Waste Management Rules 2016'
            },
            'China': {
                'recyclable': 'New Solid Waste Law (2020) emphasizes waste reduction and recycling.',
                'organic': 'Organic waste classified as "wet waste" must be separately collected.',
                'hazardous': 'Hazardous waste subject to strict tracking and handling requirements.',
                'standards': 'Follow GB 18599 standards for hazardous waste'
            }
        }
        return regulations
    
    def get_disposal_guide(self, waste_type: str, category: str) -> Dict:
        """
        Get disposal guide for specific waste type
        
        Args:
            waste_type: Type of waste (e.g., 'plastic', 'paper')
            category: Category (e.g., 'recyclable', 'organic')
        
        Returns:
            Disposal guide with steps and tips
        """
        try:
            waste_info = self.waste_database.get(waste_type, {})
            
            if not waste_info:
                return {
                    'disposal': 'Check with local waste management authority',
                    'environmental_impact': 'Unknown',
                    'recycling_process': 'Unknown'
                }
            
            return {
                'waste_type': waste_type,
                'category': category,
                'disposal_steps': waste_info.get('disposal', '').split('.'),
                'environmental_impact': waste_info.get('environmental_impact', ''),
                'recycling_info': waste_info.get('recycling_process', ''),
                'subtypes': waste_info.get('subtypes', [])
            }
        
        except Exception as e:
            logger.error(f"Error getting disposal guide: {e}")
            return {'error': str(e)}
    
    def get_regulations(self, waste_type: Optional[str] = None, region: str = 'general') -> Dict:
        """
        Get waste regulations for a region
        
        Args:
            waste_type: Optional specific waste type
            region: Geographic region ('general', 'USA', 'EU', 'India', 'China', etc.)
        
        Returns:
            Applicable regulations and guidelines
        """
        try:
            regional_regs = self.regulations_db.get(region, self.regulations_db['general'])
            
            if waste_type:
                waste_info = self.waste_database.get(waste_type, {})
                category = waste_info.get('category', 'unknown')
                
                return {
                    'region': region,
                    'waste_type': waste_type,
                    'category': category,
                    'specific_regulations': regional_regs.get(category, ''),
                    'general_regulations': regional_regs,
                    'compliance': f"Follow {region} regulations for {waste_type} disposal"
                }
            
            return {
                'region': region,
                'regulations': regional_regs
            }
        
        except Exception as e:
            logger.error(f"Error getting regulations: {e}")
            return {'error': str(e)}
    
    def get_segregation_tips(self, waste_type: Optional[str] = None) -> List[Dict]:
        """
        Get waste segregation tips
        
        Args:
            waste_type: Optional specific waste type for targeted tips
        
        Returns:
            List of segregation tips
        """
        general_tips = [
            {
                'title': 'Segregate at Source',
                'description': 'Keep recyclable, organic, and hazardous waste separate from the start',
                'impact': 'Makes processing more efficient'
            },
            {
                'title': 'Clean Your Recyclables',
                'description': 'Rinse plastic, glass, and metal containers before recycling',
                'impact': 'Reduces contamination, improves recycling quality'
            },
            {
                'title': 'Compost Organic Waste',
                'description': 'Use food and garden waste for composting to create soil',
                'impact': 'Reduces methane emissions from landfills'
            },
            {
                'title': 'Know What\'s Hazardous',
                'description': 'Never put batteries, chemicals, or electronics in regular bins',
                'impact': 'Prevents environmental contamination'
            },
            {
                'title': 'Flatten Large Items',
                'description': 'Crush boxes and flatten containers to save bin space',
                'impact': 'Optimizes collection efficiency'
            },
            {
                'title': 'Check Local Guidelines',
                'description': 'Waste rules vary by location. Know your local requirements.',
                'impact': 'Ensures proper disposal per local standards'
            }
        ]
        
        if waste_type and waste_type in self.waste_database:
            waste_info = self.waste_database[waste_type]
            return [
                {
                    'title': f"How to Dispose {waste_type.title()}",
                    'description': waste_info.get('disposal', 'See local guidelines'),
                    'impact': waste_info.get('environmental_impact', '')
                },
                *general_tips
            ]
        
        return general_tips
    
    def search_similar_items(self, query: str) -> List[Dict]:
        """
        Search for similar waste items in database
        
        Args:
            query: Search query (e.g., 'plastic bottle')
        
        Returns:
            List of similar waste items
        """
        try:
            results = []
            query_lower = query.lower()
            
            for waste_type, info in self.waste_database.items():
                if query_lower in waste_type or any(query_lower in subtype for subtype in info.get('subtypes', [])):
                    results.append({
                        'waste_type': waste_type,
                        'category': info.get('category'),
                        'subtypes': info.get('subtypes'),
                        'disposal': info.get('disposal')
                    })
            
            return results
        
        except Exception as e:
            logger.error(f"Error searching items: {e}")
            return []
