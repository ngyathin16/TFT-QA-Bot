import re
import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text for better processing"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?()%]', '', text)
    
    return text

def extract_tft_terms(text: str) -> List[str]:
    """Extract TFT-specific terms from text"""
    # Common TFT terms and patterns
    tft_patterns = [
        r'\bTFT\d+\b',  # TFT set numbers
        r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b',  # CamelCase terms (likely trait names)
        r'\b(?:trait|item|champion|ability|mechanic)\b',  # TFT concepts
    ]
    
    terms = []
    for pattern in tft_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        terms.extend(matches)
    
    return list(set(terms))

def format_tft_response(response: str) -> str:
    """Format TFT response for better readability"""
    # Add line breaks for better formatting
    response = re.sub(r'\. ', '.\n\n', response)
    
    # Bold important terms
    tft_terms = extract_tft_terms(response)
    for term in tft_terms:
        response = response.replace(term, f"**{term}**")
    
    return response

def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key format"""
    if not api_key:
        return False
    
    # OpenAI API keys typically start with 'sk-' and are 51 characters long
    pattern = r'^sk-[A-Za-z0-9]{48}$'
    return bool(re.match(pattern, api_key))

def parse_tft_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and structure TFT data for better organization"""
    parsed_data = {
        'items': [],
        'traits': [],
        'champions': [],
        'mechanics': []
    }
    
    # Process items
    if 'items' in data:
        for item in data['items']:
            if item.get('apiName', '').startswith('TFT15'):
                parsed_data['items'].append({
                    'name': item.get('name', ''),
                    'description': item.get('desc', ''),
                    'api_name': item.get('apiName', ''),
                    'effects': item.get('effects', {}),
                    'associated_traits': item.get('associatedTraits', [])
                })
    
    # Process traits
    if 'traits' in data:
        for trait in data['traits']:
            if trait.get('apiName', '').startswith('TFT15'):
                parsed_data['traits'].append({
                    'name': trait.get('name', ''),
                    'description': trait.get('desc', ''),
                    'api_name': trait.get('apiName', ''),
                    'effects': trait.get('effects', [])
                })
    
    return parsed_data

def create_search_index(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Create a search index for quick lookups"""
    search_index = {
        'by_name': {},
        'by_type': {},
        'by_keyword': {}
    }
    
    # Index by name
    for item_type, items in data.items():
        for item in items:
            name = item.get('name', '') or ''
            name_lower = name.lower()
            if name_lower:
                search_index['by_name'][name_lower] = item
    
    # Index by type
    for item_type, items in data.items():
        search_index['by_type'][item_type] = [item['name'] for item in items]
    
    # Index by keywords
    for item_type, items in data.items():
        for item in items:
            # Extract keywords from name and description
            name = item.get('name', '') or ''
            description = item.get('description', '') or ''
            text = f"{name} {description}"
            keywords = extract_tft_terms(text.lower())
            
            for keyword in keywords:
                if keyword not in search_index['by_keyword']:
                    search_index['by_keyword'][keyword] = []
                search_index['by_keyword'][keyword].append(item['name'])
    
    return search_index

def get_relevant_items(query: str, search_index: Dict[str, Any], data: Dict[str, Any]) -> List[Dict]:
    """Get relevant items based on a query"""
    query_lower = query.lower()
    relevant_items = []
    
    # Search by name
    for name, item in search_index['by_name'].items():
        if query_lower in name:
            relevant_items.append(item)
    
    # Search by keywords
    for keyword, item_names in search_index['by_keyword'].items():
        if query_lower in keyword:
            for item_name in item_names:
                # Find the full item data
                for item_type, items in data.items():
                    for item in items:
                        if item['name'] == item_name and item not in relevant_items:
                            relevant_items.append(item)
    
    return relevant_items

def format_item_info(item: Dict[str, Any]) -> str:
    """Format item information for display"""
    info = f"**{item['name']}**\n\n"
    
    if item.get('description'):
        info += f"**Description:** {item['description']}\n\n"
    
    if item.get('effects'):
        info += "**Effects:**\n"
        for key, value in item['effects'].items():
            info += f"- {key}: {value}\n"
        info += "\n"
    
    if item.get('associated_traits'):
        info += f"**Associated Traits:** {', '.join(item['associated_traits'])}\n"
    
    return info

def format_trait_info(trait: Dict[str, Any]) -> str:
    """Format trait information for display"""
    info = f"**{trait['name']}**\n\n"
    
    if trait.get('description'):
        info += f"**Description:** {trait['description']}\n\n"
    
    if trait.get('effects'):
        info += "**Effects:**\n"
        for i, effect in enumerate(trait['effects']):
            info += f"Effect {i+1}:\n"
            if 'variables' in effect:
                for key, value in effect['variables'].items():
                    info += f"- {key}: {value}\n"
        info += "\n"
    
    return info

def save_conversation_history(history: List[Dict], filename: str = "conversation_history.json"):
    """Save conversation history to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        logger.info(f"Conversation history saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save conversation history: {e}")

def load_conversation_history(filename: str = "conversation_history.json") -> List[Dict]:
    """Load conversation history from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            history = json.load(f)
        logger.info(f"Conversation history loaded from {filename}")
        return history
    except FileNotFoundError:
        logger.info("No conversation history file found")
        return []
    except Exception as e:
        logger.error(f"Failed to load conversation history: {e}")
        return []

def get_system_stats() -> Dict[str, Any]:
    """Get system statistics"""
    import psutil
    import os
    
    stats = {
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent(),
        'disk_usage': psutil.disk_usage('/').percent,
        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
    }
    
    return stats

if __name__ == "__main__":
    # Test utility functions
    test_text = "The Luchador trait in TFT15 provides bonus Attack Damage and healing effects."
    print(f"Original text: {test_text}")
    print(f"Cleaned text: {clean_text(test_text)}")
    print(f"TFT terms: {extract_tft_terms(test_text)}")
    print(f"Formatted response: {format_tft_response(test_text)}") 