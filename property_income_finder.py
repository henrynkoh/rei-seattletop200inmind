#!/usr/bin/env python3
"""
Property Income Finder - A tool to find income-generating properties
using real estate APIs with natural language filtering.

This script searches for properties that have potential for generating rental income
through features like ADUs, multi-generational layouts, large garages, etc.
"""

import requests
import json
import re
import argparse
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PropertyMatch:
    """Data class to store property information and match details"""
    address: str
    price: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[float]
    sqft: Optional[int]
    lot_size: Optional[str]
    description: str
    matched_keywords: List[str]
    bonus_features: List[str]
    confidence_score: float
    property_type: Optional[str]
    listing_url: Optional[str]

class PropertyIncomeFilter:
    """Main class for filtering properties based on income-generating potential"""
    
    def __init__(self):
        self.income_keywords = [
            'multi-gen', 'multi-generational', 'multigenerational',
            'revenue generating', 'income generating', 'rental income',
            'adu', 'accessory dwelling unit', 'guest house', 'guest cottage',
            'in-law suite', 'mother-in-law', 'granny flat', 'casita',
            'duplex', 'triplex', 'fourplex', 'multi-family',
            'separate entrance', 'private entrance', 'two kitchens',
            'basement apartment', 'carriage house', 'coach house',
            'detached unit', 'studio apartment', 'efficiency unit'
        ]
        
        self.bonus_keywords = [
            'large garage', 'oversized garage', 'three car garage', '3 car garage',
            'four car garage', '4 car garage', 'workshop', 'shop space',
            'heightened garage', 'tall garage', 'high ceiling garage',
            'rv garage', 'rv parking', 'boat garage', 'recreational vehicle',
            'commercial garage', 'mechanic bay', 'lift garage',
            'detached garage', 'barn', 'outbuilding', 'storage building',
            'warehouse space', 'flex space', 'bonus room above garage'
        ]
    
    def calculate_confidence_score(self, text: str, matched_keywords: List[str], bonus_features: List[str]) -> float:
        """Calculate confidence score based on keyword matches and context"""
        base_score = len(matched_keywords) * 0.3
        bonus_score = len(bonus_features) * 0.2
        
        # Additional scoring based on context
        text_lower = text.lower()
        
        # High-value indicators
        if any(keyword in text_lower for keyword in ['adu', 'accessory dwelling', 'guest house']):
            base_score += 0.4
        
        if any(keyword in text_lower for keyword in ['duplex', 'triplex', 'multi-family']):
            base_score += 0.3
            
        if 'separate entrance' in text_lower or 'private entrance' in text_lower:
            base_score += 0.2
            
        # Normalize score to 0-1 range
        total_score = min(base_score + bonus_score, 1.0)
        return round(total_score, 2)
    
    def find_keywords_in_text(self, text: str) -> tuple[List[str], List[str]]:
        """Find income and bonus keywords in property description"""
        text_lower = text.lower()
        
        matched_income = [keyword for keyword in self.income_keywords 
                         if keyword in text_lower]
        matched_bonus = [keyword for keyword in self.bonus_keywords 
                        if keyword in text_lower]
        
        return matched_income, matched_bonus
    
    def filter_properties(self, properties: List[Dict], custom_keywords: List[str] = None) -> List[PropertyMatch]:
        """Filter properties based on income-generating potential"""
        if custom_keywords:
            self.income_keywords.extend(custom_keywords)
        
        matches = []
        
        for prop in properties:
            # Extract property information
            description = str(prop.get('description', '')) + ' ' + str(prop.get('remarks', ''))
            address = prop.get('address', 'Unknown Address')
            
            # Find keyword matches
            matched_keywords, bonus_features = self.find_keywords_in_text(description)
            
            # Only include properties with at least one income keyword match
            if matched_keywords:
                confidence_score = self.calculate_confidence_score(
                    description, matched_keywords, bonus_features
                )
                
                property_match = PropertyMatch(
                    address=address,
                    price=prop.get('price'),
                    bedrooms=prop.get('bedrooms'),
                    bathrooms=prop.get('bathrooms'),
                    sqft=prop.get('sqft'),
                    lot_size=prop.get('lot_size'),
                    description=description[:500] + '...' if len(description) > 500 else description,
                    matched_keywords=matched_keywords,
                    bonus_features=bonus_features,
                    confidence_score=confidence_score,
                    property_type=prop.get('property_type'),
                    listing_url=prop.get('url')
                )
                
                matches.append(property_match)
        
        # Sort by confidence score (highest first)
        matches.sort(key=lambda x: x.confidence_score, reverse=True)
        return matches

class RealEstateAPIClient:
    """Client for fetching real estate data from various APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PropertyIncomeFinder/1.0'
        })
    
    def fetch_rentspree_data(self, zip_code: str, limit: int = 1000) -> List[Dict]:
        """Fetch data from RentSpree API (free tier available)"""
        logger.info(f"Fetching RentSpree data for zip code: {zip_code}")
        
        # RentSpree API endpoint (this is a mock implementation)
        # In practice, you'd need to register for an API key
        url = "https://api.rentspree.com/v1/properties/search"
        
        params = {
            'zip_code': zip_code,
            'limit': min(limit, 1000),
            'property_type': 'all'
        }
        
        try:
            # This is a mock response since we don't have real API access
            # In practice, you'd make the actual API call here
            mock_properties = self._generate_mock_data(zip_code, limit)
            return mock_properties
            
        except requests.RequestException as e:
            logger.error(f"Error fetching RentSpree data: {e}")
            return []
    
    def fetch_zillow_data(self, zip_code: str, limit: int = 1000) -> List[Dict]:
        """Fetch data from Zillow (requires RapidAPI subscription)"""
        logger.info(f"Fetching Zillow data for zip code: {zip_code}")
        
        # Note: This requires a RapidAPI subscription to Zillow API
        url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
        
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE",  # Replace with actual key
            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
        }
        
        params = {
            "location": zip_code,
            "status_type": "ForSale",
            "home_type": "Houses,Townhomes,Condos,Apartments"
        }
        
        try:
            # Mock implementation - replace with actual API call when you have a key
            mock_properties = self._generate_mock_data(zip_code, limit)
            return mock_properties
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Zillow data: {e}")
            return []
    
    def _generate_mock_data(self, zip_code: str, limit: int) -> List[Dict]:
        """Generate mock property data for demonstration purposes"""
        logger.info("Generating mock property data for demonstration")
        
        mock_descriptions = [
            "Beautiful single-family home with detached ADU perfect for rental income. Features include a large 3-car garage with high ceilings and workshop space. The accessory dwelling unit has a separate entrance and full kitchen.",
            "Multi-generational home with in-law suite featuring private entrance. Large garage with RV parking capability. Perfect for extended family or rental income opportunity.",
            "Spacious duplex with excellent rental potential. Each unit has 2 bedrooms and 1 bathroom. Large lot with room for additional parking or storage building.",
            "Custom home with guest house and oversized garage. The casita features full kitchen and bathroom, perfect for Airbnb or long-term rental. Workshop space in garage.",
            "Traditional home with basement apartment featuring separate entrance. Large garage with heightened ceilings suitable for boat or RV storage. Great investment opportunity.",
            "Single-family residence with detached garage and bonus room above. Property includes a small cottage perfect for rental income or multi-generational living.",
            "Charming home with carriage house and large workshop. The guest cottage has been updated with modern amenities and generates steady rental income.",
            "Investment property with main house and two additional units. Large garage with commercial-grade doors and lift capability. Excellent cash flow potential.",
            "Family home with mother-in-law suite and three-car garage. The in-law unit has its own kitchen and entrance, perfect for rental or family use.",
            "Property with main residence and detached studio apartment. Large garage with RV access and storage space. Great for income generation."
        ]
        
        # Real estate websites for functional links
        real_estate_sites = [
            "https://www.zillow.com/homes/for_sale/",
            "https://www.realtor.com/realestateandhomes-search/",
            "https://www.redfin.com/city/",
            "https://www.homes.com/for-sale/",
            "https://www.trulia.com/for_sale/"
        ]
        
        properties = []
        for i in range(min(limit, len(mock_descriptions) * 10)):
            desc_index = i % len(mock_descriptions)
            site_index = i % len(real_estate_sites)
            
            # Create functional URLs that point to real estate search pages
            base_url = real_estate_sites[site_index]
            if i % 3 == 0:  # Every third property gets a local detail page
                functional_url = f"/property/{1000 + i}"
            elif "zillow.com" in base_url:
                functional_url = f"{base_url}{zip_code}_rb/"
            elif "realtor.com" in base_url:
                functional_url = f"{base_url}{zip_code}/"
            elif "redfin.com" in base_url:
                functional_url = f"{base_url}{zip_code}/"
            elif "homes.com" in base_url:
                functional_url = f"{base_url}{zip_code}/"
            elif "trulia.com" in base_url:
                functional_url = f"{base_url}{zip_code}_rb/"
            else:
                functional_url = f"/property/{1000 + i}"  # Local fallback
            
            properties.append({
                'address': f"{1000 + i} Example St, City, State {zip_code}",
                'price': f"${450000 + (i * 25000):,}",
                'bedrooms': 3 + (i % 3),
                'bathrooms': 2.0 + (i % 2) * 0.5,
                'sqft': 1800 + (i * 100),
                'lot_size': f"{0.25 + (i % 4) * 0.1:.2f} acres",
                'description': mock_descriptions[desc_index],
                'property_type': ['Single Family', 'Duplex', 'Townhome'][i % 3],
                'url': functional_url
            })
        
        return properties

def save_results_to_file(matches: List[PropertyMatch], filename: str):
    """Save filtered results to a JSON file"""
    results = []
    for match in matches:
        results.append({
            'address': match.address,
            'price': match.price,
            'bedrooms': match.bedrooms,
            'bathrooms': match.bathrooms,
            'sqft': match.sqft,
            'lot_size': match.lot_size,
            'description': match.description,
            'matched_keywords': match.matched_keywords,
            'bonus_features': match.bonus_features,
            'confidence_score': match.confidence_score,
            'property_type': match.property_type,
            'listing_url': match.listing_url
        })
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {filename}")

def print_results(matches: List[PropertyMatch], limit: int = 10):
    """Print filtered results to console"""
    print(f"\n{'='*80}")
    print(f"INCOME-GENERATING PROPERTY SEARCH RESULTS")
    print(f"{'='*80}")
    print(f"Found {len(matches)} properties with income potential")
    print(f"Showing top {min(limit, len(matches))} results:\n")
    
    for i, match in enumerate(matches[:limit], 1):
        print(f"{i}. {match.address}")
        print(f"   Price: {match.price}")
        print(f"   Beds/Baths: {match.bedrooms}/{match.bathrooms}")
        print(f"   Sqft: {match.sqft:,}" if match.sqft else "   Sqft: N/A")
        print(f"   Confidence Score: {match.confidence_score}")
        print(f"   Income Keywords: {', '.join(match.matched_keywords)}")
        if match.bonus_features:
            print(f"   Bonus Features: {', '.join(match.bonus_features)}")
        print(f"   Description: {match.description[:200]}...")
        if match.listing_url:
            print(f"   URL: {match.listing_url}")
        print("-" * 80)

def main():
    """Main function to run the property income finder"""
    parser = argparse.ArgumentParser(description='Find income-generating properties')
    parser.add_argument('zip_code', help='ZIP code to search in')
    parser.add_argument('--keywords', nargs='*', help='Additional custom keywords to search for')
    parser.add_argument('--limit', type=int, default=1000, help='Maximum number of properties to fetch')
    parser.add_argument('--api', choices=['rentspree', 'zillow'], default='rentspree', 
                       help='API to use for property data')
    parser.add_argument('--output', help='Output file to save results (JSON format)')
    parser.add_argument('--show-limit', type=int, default=10, 
                       help='Number of results to display in console')
    
    args = parser.parse_args()
    
    # Initialize components
    api_client = RealEstateAPIClient()
    property_filter = PropertyIncomeFilter()
    
    # Fetch property data
    print(f"Searching for properties in ZIP code: {args.zip_code}")
    print(f"Using API: {args.api}")
    print(f"Fetching up to {args.limit} properties...")
    
    if args.api == 'rentspree':
        properties = api_client.fetch_rentspree_data(args.zip_code, args.limit)
    elif args.api == 'zillow':
        properties = api_client.fetch_zillow_data(args.zip_code, args.limit)
    
    if not properties:
        print("No properties found or API error occurred.")
        return
    
    print(f"Fetched {len(properties)} properties")
    
    # Filter properties for income potential
    print("Filtering properties for income-generating potential...")
    matches = property_filter.filter_properties(properties, args.keywords)
    
    # Display results
    print_results(matches, args.show_limit)
    
    # Save results if output file specified
    if args.output:
        save_results_to_file(matches, args.output)
    
    # Summary statistics
    if matches:
        avg_confidence = sum(match.confidence_score for match in matches) / len(matches)
        high_confidence = len([m for m in matches if m.confidence_score >= 0.7])
        
        print(f"\nSUMMARY STATISTICS:")
        print(f"Total matches: {len(matches)}")
        print(f"Average confidence score: {avg_confidence:.2f}")
        print(f"High confidence matches (≥0.7): {high_confidence}")

if __name__ == "__main__":
    main() 