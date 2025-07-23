import requests
import json
import pandas as pd
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TFTDataProcessor:
    """Processes TFT Set 15 data from Community Dragon API"""
    
    def __init__(self):
        self.base_url = "https://raw.communitydragon.org/pbe/cdragon/tft/en_us.json"
        self.data = None
        
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch data from Community Dragon API"""
        try:
            logger.info("Fetching TFT data from Community Dragon API...")
            response = requests.get(self.base_url)
            response.raise_for_status()
            self.data = response.json()
            logger.info("Successfully fetched TFT data")
            return self.data
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            raise
    
    def filter_tft15_data(self) -> Dict[str, Any]:
        """Filter data to only include TFT15 (Set 15) content"""
        if not self.data:
            self.fetch_data()
            
        tft15_data = {
            'items': [],
            'traits': []
        }
        
        # Filter items
        if 'items' in self.data:
            for item in self.data['items']:
                if 'apiName' in item and item['apiName'].startswith('TFT15'):
                    tft15_data['items'].append(item)
        
        # Filter traits
        if 'traits' in self.data:
            for trait in self.data['traits']:
                if 'apiName' in trait and trait['apiName'].startswith('TFT15'):
                    tft15_data['traits'].append(trait)
        
        logger.info(f"Filtered {len(tft15_data['items'])} TFT15 items and {len(tft15_data['traits'])} TFT15 traits")
        return tft15_data
    
    def process_items(self, items: List[Dict]) -> List[Dict]:
        """Process and clean item data"""
        processed_items = []
        
        for item in items:
            processed_item = {
                'type': 'item',
                'name': item.get('name', 'Unknown Item'),
                'api_name': item.get('apiName', ''),
                'description': item.get('desc', ''),
                'icon': item.get('icon', ''),
                'effects': item.get('effects', {}),
                'associated_traits': item.get('associatedTraits', []),
                'tags': item.get('tags', [])
            }
            processed_items.append(processed_item)
        
        return processed_items
    
    def process_traits(self, traits: List[Dict]) -> List[Dict]:
        """Process and clean trait data"""
        processed_traits = []
        
        for trait in traits:
            processed_trait = {
                'type': 'trait',
                'name': trait.get('name', 'Unknown Trait'),
                'api_name': trait.get('apiName', ''),
                'description': trait.get('desc', ''),
                'icon': trait.get('icon', ''),
                'effects': trait.get('effects', []),
                'associated_traits': trait.get('associatedTraits', [])
            }
            processed_traits.append(processed_trait)
        
        return processed_traits
    
    def create_documents(self) -> List[Dict]:
        """Create documents for vector store indexing"""
        tft15_data = self.filter_tft15_data()
        
        documents = []
        
        # Process items
        processed_items = self.process_items(tft15_data['items'])
        for item in processed_items:
            doc = {
                'content': f"Item: {item['name']}\nDescription: {item['description']}\nAssociated Traits: {', '.join(item['associated_traits'])}",
                'metadata': {
                    'type': 'item',
                    'name': item['name'],
                    'api_name': item['api_name'],
                    'description': item['description']
                }
            }
            documents.append(doc)
        
        # Process traits
        processed_traits = self.process_traits(tft15_data['traits'])
        for trait in processed_traits:
            # Create description from effects
            effects_text = ""
            if trait['effects']:
                for i, effect in enumerate(trait['effects']):
                    if 'variables' in effect:
                        effects_text += f"\nEffect {i+1}: "
                        for key, value in effect['variables'].items():
                            effects_text += f"{key}: {value}, "
            
            doc = {
                'content': f"Trait: {trait['name']}\nDescription: {trait['description']}{effects_text}",
                'metadata': {
                    'type': 'trait',
                    'name': trait['name'],
                    'api_name': trait['api_name'],
                    'description': trait['description']
                }
            }
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} documents for vector store")
        return documents
    
    def save_processed_data(self, filename: str = 'tft15_data.json'):
        """Save processed data to JSON file"""
        tft15_data = self.filter_tft15_data()
        processed_items = self.process_items(tft15_data['items'])
        processed_traits = self.process_traits(tft15_data['traits'])
        
        data_to_save = {
            'items': processed_items,
            'traits': processed_traits
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved processed data to {filename}")
    
    def get_searchable_content(self) -> List[str]:
        """Get all searchable content as text"""
        documents = self.create_documents()
        return [doc['content'] for doc in documents]

if __name__ == "__main__":
    # Test the data processor
    processor = TFTDataProcessor()
    documents = processor.create_documents()
    processor.save_processed_data()
    
    print(f"Processed {len(documents)} documents")
    print("Sample document:")
    if documents:
        print(documents[0]['content'][:200] + "...") 