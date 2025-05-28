#!/usr/bin/env python3
"""
Flask Web Application for Property Income Finder
Provides a modern web interface for finding income-generating properties
"""

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
import json
import os
from datetime import datetime, timedelta
import logging
import sqlite3
import hashlib
from property_income_finder import PropertyIncomeFilter, RealEstateAPIClient, PropertyMatch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'property-income-finder-secret-key-2025'

# Initialize components
api_client = RealEstateAPIClient()
property_filter = PropertyIncomeFilter()

# Database initialization
def init_db():
    """Initialize SQLite database for user data"""
    conn = sqlite3.connect('property_finder.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Portfolio table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            property_address TEXT NOT NULL,
            purchase_price REAL,
            current_value REAL,
            monthly_rent REAL,
            monthly_expenses REAL,
            purchase_date DATE,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Saved searches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            search_name TEXT NOT NULL,
            zip_code TEXT,
            keywords TEXT,
            api_choice TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Market analysis cache
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_code TEXT NOT NULL,
            avg_price REAL,
            avg_rent REAL,
            cap_rate REAL,
            appreciation_rate REAL,
            analysis_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Create demo user if it doesn't exist
    demo_password_hash = hashlib.sha256('demo123'.encode()).hexdigest()
    try:
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                      ('demo', 'demo@propertyincomefinder.com', demo_password_hash))
        demo_user_id = cursor.lastrowid
        
        # Add sample portfolio properties for demo user
        sample_properties = [
            ('123 Rental Ave, Seattle, WA 98092', 450000, 475000, 3200, 800, '2023-01-15', 'Single family home with ADU potential'),
            ('456 Investment St, Bellevue, WA 98004', 650000, 680000, 4500, 1200, '2023-06-20', 'Duplex with excellent cash flow'),
            ('789 Income Blvd, Tacoma, WA 98402', 320000, 340000, 2800, 600, '2024-02-10', 'Townhome in growing neighborhood')
        ]
        
        for prop in sample_properties:
            cursor.execute('''
                INSERT INTO portfolio (user_id, property_address, purchase_price, current_value, 
                                     monthly_rent, monthly_expenses, purchase_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (demo_user_id,) + prop)
        
        # Add sample saved searches
        sample_searches = [
            ('ADU Properties 98092', '98092', 'adu,accessory dwelling unit', 'rentspree'),
            ('Multi-family Bellevue', '98004', 'duplex,triplex', 'rentspree'),
            ('House Hacking Opportunities', '98115', 'in-law suite,basement apartment', 'rentspree')
        ]
        
        for search in sample_searches:
            cursor.execute('''
                INSERT INTO saved_searches (user_id, search_name, zip_code, keywords, api_choice)
                VALUES (?, ?, ?, ?, ?)
            ''', (demo_user_id,) + search)
        
        conn.commit()
        print("✅ Demo user created with sample data")
        
    except sqlite3.IntegrityError:
        # Demo user already exists
        pass
    
    conn.close()

@app.route('/')
def index():
    """Main page with search interface"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard with portfolio overview"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user portfolio data
    conn = sqlite3.connect('property_finder.db')
    cursor = conn.cursor()
    
    # Portfolio summary
    cursor.execute('''
        SELECT COUNT(*), SUM(current_value), SUM(monthly_rent), SUM(monthly_expenses)
        FROM portfolio WHERE user_id = ?
    ''', (session['user_id'],))
    
    portfolio_summary = cursor.fetchone()
    
    # Recent searches
    cursor.execute('''
        SELECT search_name, zip_code, created_at
        FROM saved_searches WHERE user_id = ?
        ORDER BY created_at DESC LIMIT 5
    ''', (session['user_id'],))
    
    recent_searches = cursor.fetchall()
    
    # Portfolio properties
    cursor.execute('''
        SELECT property_address, purchase_price, current_value, monthly_rent, monthly_expenses
        FROM portfolio WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (session['user_id'],))
    
    properties = cursor.fetchall()
    conn.close()
    
    dashboard_data = {
        'portfolio_count': portfolio_summary[0] or 0,
        'total_value': portfolio_summary[1] or 0,
        'monthly_income': portfolio_summary[2] or 0,
        'monthly_expenses': portfolio_summary[3] or 0,
        'recent_searches': recent_searches,
        'properties': properties
    }
    
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Hash password for comparison
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = sqlite3.connect('property_finder.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users WHERE username = ? AND password_hash = ?', 
                      (username, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'All fields required'}), 400
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = sqlite3.connect('property_finder.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                          (username, email, password_hash))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            session['user_id'] = user_id
            session['username'] = username
            return jsonify({'success': True, 'redirect': '/dashboard'})
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username or email already exists'}), 400
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/calculator', methods=['POST'])
def investment_calculator():
    """Investment analysis calculator"""
    try:
        data = request.get_json()
        
        # Input parameters
        purchase_price = float(data.get('purchase_price', 0))
        down_payment_percent = float(data.get('down_payment_percent', 20))
        interest_rate = float(data.get('interest_rate', 6.5))
        loan_term = int(data.get('loan_term', 30))
        monthly_rent = float(data.get('monthly_rent', 0))
        monthly_expenses = float(data.get('monthly_expenses', 0))
        closing_costs = float(data.get('closing_costs', 0))
        renovation_costs = float(data.get('renovation_costs', 0))
        
        # Calculations
        down_payment = purchase_price * (down_payment_percent / 100)
        loan_amount = purchase_price - down_payment
        monthly_rate = (interest_rate / 100) / 12
        num_payments = loan_term * 12
        
        # Monthly mortgage payment
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        else:
            monthly_payment = loan_amount / num_payments
        
        # Cash flow analysis
        total_monthly_expenses = monthly_expenses + monthly_payment
        monthly_cash_flow = monthly_rent - total_monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Initial investment
        total_initial_investment = down_payment + closing_costs + renovation_costs
        
        # Return metrics
        if total_initial_investment > 0:
            cash_on_cash_return = (annual_cash_flow / total_initial_investment) * 100
        else:
            cash_on_cash_return = 0
        
        if purchase_price > 0:
            cap_rate = (annual_cash_flow + monthly_payment * 12) / purchase_price * 100
        else:
            cap_rate = 0
        
        # 1% rule check
        one_percent_rule = (monthly_rent / purchase_price) * 100
        
        results = {
            'purchase_price': purchase_price,
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'monthly_cash_flow': monthly_cash_flow,
            'annual_cash_flow': annual_cash_flow,
            'total_initial_investment': total_initial_investment,
            'cash_on_cash_return': round(cash_on_cash_return, 2),
            'cap_rate': round(cap_rate, 2),
            'one_percent_rule': round(one_percent_rule, 2),
            'meets_one_percent': one_percent_rule >= 1.0
        }
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        logger.error(f"Calculator error: {str(e)}")
        return jsonify({'error': f'Calculation failed: {str(e)}'}), 500

@app.route('/api/market-analysis/<zip_code>')
def market_analysis(zip_code):
    """Get market analysis for a ZIP code"""
    try:
        # Check cache first
        conn = sqlite3.connect('property_finder.db')
        cursor = conn.cursor()
        
        # Look for recent analysis (within 7 days)
        cursor.execute('''
            SELECT avg_price, avg_rent, cap_rate, appreciation_rate
            FROM market_analysis 
            WHERE zip_code = ? AND analysis_date > date('now', '-7 days')
            ORDER BY created_at DESC LIMIT 1
        ''', (zip_code,))
        
        cached_data = cursor.fetchone()
        
        if cached_data:
            conn.close()
            return jsonify({
                'success': True,
                'zip_code': zip_code,
                'avg_price': cached_data[0],
                'avg_rent': cached_data[1],
                'cap_rate': cached_data[2],
                'appreciation_rate': cached_data[3],
                'data_source': 'cached'
            })
        
        # Generate new analysis (mock data for demonstration)
        import random
        
        base_price = 400000 + random.randint(-100000, 200000)
        avg_price = base_price + random.randint(-50000, 100000)
        avg_rent = (avg_price * 0.008) + random.randint(-200, 500)  # Rough 0.8% rule
        cap_rate = (avg_rent * 12 / avg_price) * 100
        appreciation_rate = 3.5 + random.uniform(-1.5, 2.5)
        
        # Cache the results
        cursor.execute('''
            INSERT INTO market_analysis (zip_code, avg_price, avg_rent, cap_rate, appreciation_rate, analysis_date)
            VALUES (?, ?, ?, ?, ?, date('now'))
        ''', (zip_code, avg_price, avg_rent, cap_rate, appreciation_rate))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'zip_code': zip_code,
            'avg_price': round(avg_price, 0),
            'avg_rent': round(avg_rent, 0),
            'cap_rate': round(cap_rate, 2),
            'appreciation_rate': round(appreciation_rate, 2),
            'data_source': 'fresh'
        })
        
    except Exception as e:
        logger.error(f"Market analysis error: {str(e)}")
        return jsonify({'error': f'Market analysis failed: {str(e)}'}), 500

@app.route('/api/portfolio', methods=['GET', 'POST'])
def portfolio_management():
    """Portfolio management endpoints"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    conn = sqlite3.connect('property_finder.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Add property to portfolio
        data = request.get_json()
        
        cursor.execute('''
            INSERT INTO portfolio (user_id, property_address, purchase_price, current_value, 
                                 monthly_rent, monthly_expenses, purchase_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session['user_id'],
            data.get('address'),
            data.get('purchase_price'),
            data.get('current_value'),
            data.get('monthly_rent'),
            data.get('monthly_expenses'),
            data.get('purchase_date'),
            data.get('notes')
        ))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Property added to portfolio'})
    
    else:
        # Get portfolio
        cursor.execute('''
            SELECT id, property_address, purchase_price, current_value, monthly_rent, 
                   monthly_expenses, purchase_date, notes, created_at
            FROM portfolio WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (session['user_id'],))
        
        properties = []
        for row in cursor.fetchall():
            properties.append({
                'id': row[0],
                'address': row[1],
                'purchase_price': row[2],
                'current_value': row[3],
                'monthly_rent': row[4],
                'monthly_expenses': row[5],
                'purchase_date': row[6],
                'notes': row[7],
                'created_at': row[8]
            })
        
        conn.close()
        return jsonify({'success': True, 'properties': properties})

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
    print("🏠 Property Income Finder Web App")
    print("🌐 Starting server on http://localhost:3001")
    print("📊 Ready to find income-generating properties!")
    
    # Initialize database
    init_db()
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    os.makedirs('docs/screenshots', exist_ok=True)
    
    print("💾 Database initialized")
    print("🔐 User authentication enabled")
    print("📈 Portfolio management active")
    print("🧮 Investment calculator ready")
    print("📊 Market analysis available")
    
    app.run(host='0.0.0.0', port=3001, debug=True) 