#!/usr/bin/env python3
"""
Flask Web Application for Property Income Finder
Provides a modern web interface for finding income-generating properties
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
import logging
from property_income_finder import PropertyIncomeFilter, RealEstateAPIClient, PropertyMatch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'property-income-finder-secret-key'

# Initialize components
api_client = RealEstateAPIClient()
property_filter = PropertyIncomeFilter()

@app.route('/')
def index():
    """Main page with search interface"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_properties():
    """API endpoint for property search"""
    try:
        data = request.get_json()
        zip_code = data.get('zip_code', '').strip()
        custom_keywords = data.get('keywords', [])
        api_choice = data.get('api', 'rentspree')
        limit = int(data.get('limit', 100))
        
        if not zip_code:
            return jsonify({'error': 'ZIP code is required'}), 400
        
        # Fetch property data
        logger.info(f"Searching properties in {zip_code} using {api_choice}")
        
        if api_choice == 'rentspree':
            properties = api_client.fetch_rentspree_data(zip_code, limit)
        elif api_choice == 'zillow':
            properties = api_client.fetch_zillow_data(zip_code, limit)
        else:
            return jsonify({'error': 'Invalid API choice'}), 400
        
        if not properties:
            return jsonify({'error': 'No properties found or API error'}), 404
        
        # Filter properties for income potential
        matches = property_filter.filter_properties(properties, custom_keywords)
        
        # Convert PropertyMatch objects to dictionaries
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
        
        # Calculate statistics
        stats = {
            'total_properties': len(properties),
            'total_matches': len(matches),
            'avg_confidence': round(sum(m.confidence_score for m in matches) / len(matches), 2) if matches else 0,
            'high_confidence_count': len([m for m in matches if m.confidence_score >= 0.7])
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'statistics': stats,
            'search_params': {
                'zip_code': zip_code,
                'api': api_choice,
                'custom_keywords': custom_keywords,
                'limit': limit,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export_results():
    """Export search results to JSON file"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        zip_code = data.get('zip_code', 'unknown')
        
        filename = f"property_search_{zip_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join('exports', filename)
        
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Save results
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

@app.route('/api/strategies')
def get_strategies():
    """Get predefined investment strategies"""
    strategies = {
        'adu_focused': {
            'name': 'ADU-Focused Investment',
            'description': 'Properties with Accessory Dwelling Units and guest houses',
            'keywords': ['adu', 'accessory dwelling unit', 'guest house', 'detached unit', 'separate entrance']
        },
        'multi_family': {
            'name': 'Multi-Family Properties',
            'description': 'Duplexes, triplexes, and multi-unit buildings',
            'keywords': ['duplex', 'triplex', 'fourplex', 'multi-family', 'multi-unit']
        },
        'garage_conversion': {
            'name': 'Garage Conversion Potential',
            'description': 'Properties with large garages suitable for conversion',
            'keywords': ['large garage', 'oversized garage', 'workshop', 'garage apartment', 'detached garage']
        },
        'house_hacking': {
            'name': 'House Hacking Opportunities',
            'description': 'Properties suitable for owner-occupied rental strategies',
            'keywords': ['in-law suite', 'mother-in-law', 'basement apartment', 'separate living area', 'private entrance']
        },
        'rv_boat_storage': {
            'name': 'RV/Boat Storage Income',
            'description': 'Properties with RV parking and storage rental potential',
            'keywords': ['rv garage', 'rv parking', 'boat garage', 'heightened garage', 'commercial garage']
        }
    }
    
    return jsonify(strategies)

@app.route('/download/<filename>')
def download_file(filename):
    """Download exported files"""
    try:
        filepath = os.path.join('exports', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    """Display detailed property information"""
    # Mock property data for demonstration
    property_data = {
        'id': property_id,
        'address': f"{1000 + property_id} Example St, City, State 98092",
        'price': f"${450000 + (property_id * 25000):,}",
        'bedrooms': 3 + (property_id % 3),
        'bathrooms': 2.0 + (property_id % 2) * 0.5,
        'sqft': 1800 + (property_id * 100),
        'lot_size': f"{0.25 + (property_id % 4) * 0.1:.2f} acres",
        'property_type': ['Single Family', 'Duplex', 'Townhome'][property_id % 3],
        'year_built': 1990 + (property_id % 30),
        'description': "Beautiful single-family home with detached ADU perfect for rental income. Features include a large 3-car garage with high ceilings and workshop space. The accessory dwelling unit has a separate entrance and full kitchen.",
        'features': [
            'Detached ADU with separate entrance',
            'Large 3-car garage with high ceilings',
            'Workshop space in garage',
            'Full kitchen in ADU',
            'Private entrance to ADU',
            'Large lot with expansion potential'
        ],
        'images': [
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
            'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800'
        ]
    }
    
    return render_template('property_detail.html', property=property_data)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    
    print("🏠 Property Income Finder Web App")
    print("🌐 Starting server on http://localhost:3000")
    print("📊 Ready to find income-generating properties!")
    
    app.run(host='0.0.0.0', port=3000, debug=True) 