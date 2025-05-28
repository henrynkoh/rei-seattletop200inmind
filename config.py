"""
Configuration file for Property Income Finder
Update these settings with your actual API keys and preferences
"""

# API Configuration
API_KEYS = {
    'rapidapi_key': 'YOUR_RAPIDAPI_KEY_HERE',  # For Zillow API access
    'rentspree_key': 'YOUR_RENTSPREE_KEY_HERE',  # For RentSpree API access
}

# API Endpoints
API_ENDPOINTS = {
    'zillow': 'https://zillow-com1.p.rapidapi.com/propertyExtendedSearch',
    'rentspree': 'https://api.rentspree.com/v1/properties/search',
    'redfin': 'https://api.redfin.com/v1/search',  # Future implementation
}

# Default Search Parameters
DEFAULT_PARAMS = {
    'max_properties': 1000,
    'default_api': 'rentspree',
    'confidence_threshold': 0.5,  # Minimum confidence score to include in results
    'max_description_length': 500,  # Truncate descriptions longer than this
}

# Rate Limiting (requests per minute)
RATE_LIMITS = {
    'zillow': 60,
    'rentspree': 100,
    'redfin': 50,
}

# Custom keyword categories for different investment strategies
INVESTMENT_STRATEGIES = {
    'adu_focused': [
        'adu', 'accessory dwelling unit', 'guest house', 'detached unit',
        'separate entrance', 'granny flat', 'casita', 'coach house'
    ],
    'multi_family': [
        'duplex', 'triplex', 'fourplex', 'multi-family', 'multi-unit',
        'two family', 'three family', 'apartment building'
    ],
    'garage_conversion': [
        'large garage', 'oversized garage', 'workshop', 'garage apartment',
        'bonus room above garage', 'detached garage', 'barn conversion'
    ],
    'house_hacking': [
        'in-law suite', 'mother-in-law', 'basement apartment',
        'separate living area', 'private entrance', 'two kitchens'
    ]
}

# Scoring weights for different features
SCORING_WEIGHTS = {
    'income_keyword_base': 0.3,
    'bonus_feature_base': 0.2,
    'adu_bonus': 0.4,
    'multi_family_bonus': 0.3,
    'separate_entrance_bonus': 0.2,
    'large_lot_bonus': 0.1,
    'garage_bonus': 0.15,
}

# Output formatting preferences
OUTPUT_SETTINGS = {
    'console_width': 80,
    'max_description_display': 200,
    'date_format': '%Y-%m-%d %H:%M:%S',
    'currency_format': '${:,.0f}',
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'property_finder.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
} 