# 📖 Property Income Finder - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Web Interface Guide](#web-interface-guide)
3. [Investment Strategies](#investment-strategies)
4. [Search Configuration](#search-configuration)
5. [Understanding Results](#understanding-results)
6. [Command Line Usage](#command-line-usage)
7. [API Integration](#api-integration)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Features](#advanced-features)

## Getting Started

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM
- **Storage**: 100MB free space
- **Internet**: Stable connection required

### Installation Steps

1. **Download the Application**
   ```bash
   git clone https://github.com/yourusername/property-income-finder.git
   cd property-income-finder
   ```

2. **Install Dependencies**
   ```bash
   pip install flask requests
   ```

3. **Verify Installation**
   ```bash
   python3 app.py
   ```
   You should see: "🏠 Property Income Finder Web App"

## Web Interface Guide

### Main Dashboard

The web interface provides an intuitive way to search for income-generating properties:

#### 1. Search Form
- **ZIP Code Field**: Enter the target area (required)
- **Data Source**: Choose between RentSpree or Zillow
- **Property Limit**: Set how many properties to analyze (50-500)

#### 2. Investment Strategy Selection
Choose from 5 pre-built strategies or create custom keywords:

**Strategy Buttons**:
- Click to activate/deactivate strategies
- Multiple strategies can be selected simultaneously
- Auto-populates relevant keywords

**Quick Actions**:
- **Select All**: Activates all 5 strategies
- **Clear All**: Deactivates all strategies
- **Keyboard Shortcuts**: Ctrl+A (Select All), Ctrl+C (Clear)

#### 3. Custom Keywords
- Add specific terms not covered by strategies
- Separate multiple keywords with commas
- Case-insensitive matching

### Search Results Interface

#### Statistics Dashboard
- **Total Properties**: Number of properties analyzed
- **Income Matches**: Properties with income potential
- **Average Confidence**: Overall match quality
- **High Confidence**: Properties with 70%+ confidence scores

#### Property Cards
Each property displays:
- **Confidence Score**: Color-coded percentage (Green: 80%+, Yellow: 60-79%, Red: <60%)
- **Property Details**: Price, bedrooms, bathrooms, square footage
- **Income Keywords**: Matched terms that indicate income potential
- **Bonus Features**: Additional valuable characteristics
- **Property Description**: Full listing description
- **External Link**: Direct link to original listing

## Investment Strategies

### 1. ADU-Focused Investment
**Best For**: Investors seeking immediate rental income

**Target Properties**:
- Existing accessory dwelling units
- Guest houses and casitas
- In-law suites with separate entrances
- Properties with ADU permits

**Keywords Searched**:
- "adu", "accessory dwelling unit"
- "guest house", "guest cottage"
- "casita", "in-law suite"
- "mother-in-law", "granny flat"

**Expected ROI**: 15-25% annually
**Investment Level**: Medium ($50K-$150K for improvements)

### 2. Multi-Family Properties
**Best For**: Experienced investors with larger budgets

**Target Properties**:
- Duplexes, triplexes, fourplexes
- Properties with multiple units
- Converted single-family homes

**Keywords Searched**:
- "duplex", "triplex", "fourplex"
- "multi-family", "multi-unit"
- "separate units", "two kitchens"

**Expected ROI**: 8-15% annually
**Investment Level**: High ($200K-$500K+)

### 3. Garage Conversion Potential
**Best For**: DIY investors and contractors

**Target Properties**:
- Oversized garages (3+ cars)
- High-ceiling garages
- Detached garages with utilities

**Keywords Searched**:
- "large garage", "oversized garage"
- "three car garage", "workshop"
- "high ceiling", "detached garage"

**Expected ROI**: 20-30% on conversion investment
**Investment Level**: Medium ($30K-$80K for conversion)

### 4. House Hacking Opportunities
**Best For**: First-time investors and owner-occupants

**Target Properties**:
- Properties with basement apartments
- Homes with separate entrances
- Large homes suitable for roommates

**Keywords Searched**:
- "separate entrance", "private entrance"
- "basement apartment", "finished basement"
- "two master suites"

**Expected ROI**: Reduced living costs + rental income
**Investment Level**: Low to Medium ($10K-$50K for improvements)

### 5. RV/Boat Storage Income
**Best For**: Investors in recreational vehicle markets

**Target Properties**:
- Large lots with RV access
- Properties with boat storage
- Commercial-zoned residential

**Keywords Searched**:
- "rv parking", "boat storage"
- "large lot", "commercial zoning"
- "storage building", "warehouse"

**Expected ROI**: $100-$300/month per space
**Investment Level**: Low ($5K-$20K for setup)

## Search Configuration

### Data Sources

#### RentSpree (Default)
- **Coverage**: Major metropolitan areas
- **Update Frequency**: Daily
- **Property Types**: Single-family, condos, townhomes
- **Demo Mode**: Includes sample data for testing

#### Zillow
- **Coverage**: Nationwide
- **Update Frequency**: Real-time
- **Property Types**: All residential types
- **API Key Required**: For production use

### Property Limits
- **50 Properties**: Quick searches, specific areas
- **100 Properties**: Balanced speed and coverage (recommended)
- **250 Properties**: Comprehensive area analysis
- **500 Properties**: Maximum coverage (slower processing)

### Custom Keywords

#### Best Practices
1. **Use Specific Terms**: "guest house" vs "house"
2. **Include Variations**: "adu", "accessory dwelling unit"
3. **Consider Synonyms**: "in-law suite", "mother-in-law"
4. **Avoid Common Words**: "nice", "beautiful", "great"

#### Keyword Categories
- **Income Features**: adu, duplex, rental unit
- **Structural Elements**: separate entrance, two kitchens
- **Zoning/Legal**: permitted, legal, conforming
- **Size Indicators**: large, oversized, spacious

## Understanding Results

### Confidence Scoring Algorithm

The confidence score (0-100%) is calculated based on:

#### Primary Factors (60% of score)
- **Income Keywords**: +30 points per match
- **Multiple Matches**: Bonus for 2+ keywords
- **High-Value Terms**: ADU, duplex get extra weight

#### Secondary Factors (25% of score)
- **Bonus Features**: +20 points per feature
- **Property Type**: Multi-family gets bonus
- **Lot Size**: Larger lots score higher

#### Context Factors (15% of score)
- **Description Quality**: Detailed descriptions score higher
- **Keyword Density**: Multiple mentions increase score
- **Negative Indicators**: Certain terms reduce score

### Score Interpretation
- **90-100%**: Excellent income potential, investigate immediately
- **80-89%**: Very good potential, high priority
- **70-79%**: Good potential, worth investigating
- **60-69%**: Moderate potential, secondary priority
- **50-59%**: Low potential, consider if other factors align
- **Below 50%**: Minimal income potential

### Property Analysis Tips

#### Red Flags to Watch For
- Properties with "no rental" restrictions
- HOA rules prohibiting rentals
- Zoning that doesn't allow multi-family use
- Properties in poor condition requiring major repairs

#### Green Flags to Prioritize
- Existing rental permits
- Separate utilities for units
- Recent renovations or updates
- Properties in rental-friendly neighborhoods

## Command Line Usage

### Basic Commands

#### Simple Search
```bash
python3 property_income_finder.py 98101
```

#### Custom Keywords
```bash
python3 property_income_finder.py 98101 --keywords "adu" "guest house" "duplex"
```

#### API Selection
```bash
python3 property_income_finder.py 98101 --api zillow
```

#### Output to File
```bash
python3 property_income_finder.py 98101 --output results.json
```

### Advanced Commands

#### Comprehensive Search
```bash
python3 property_income_finder.py 98101 \
  --keywords "adu" "duplex" "large garage" \
  --limit 500 \
  --api rentspree \
  --output comprehensive_search.json \
  --show-limit 25
```

#### Batch Processing
```bash
# Search multiple ZIP codes
for zip in 98101 98102 98103; do
  python3 property_income_finder.py $zip --output "results_$zip.json"
done
```

### Command Line Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `zip_code` | Target ZIP code (required) | - | `98101` |
| `--keywords` | Custom search keywords | Built-in list | `"adu" "duplex"` |
| `--limit` | Max properties to fetch | 1000 | `500` |
| `--api` | Data source API | rentspree | `zillow` |
| `--output` | Output file path | None | `results.json` |
| `--show-limit` | Console results limit | 10 | `20` |

## API Integration

### Setting Up Real APIs

#### RentSpree API
1. Register at [RentSpree Developer Portal](https://www.rentspree.com/api)
2. Obtain API key
3. Update `app.py`:
   ```python
   RENTSPREE_API_KEY = "your_api_key_here"
   ```

#### Zillow API (via RapidAPI)
1. Subscribe to [Zillow API on RapidAPI](https://rapidapi.com/apimaker/api/zillow-com1/)
2. Get RapidAPI key
3. Update `app.py`:
   ```python
   RAPIDAPI_KEY = "your_rapidapi_key_here"
   ```

### Custom API Integration

To add a new real estate API:

1. **Create API Client Method**:
   ```python
   def fetch_custom_api_data(self, zip_code, limit):
       # Implement API call
       pass
   ```

2. **Update Web Interface**:
   Add new option to API dropdown in `templates/index.html`

3. **Test Integration**:
   ```bash
   python3 property_income_finder.py 98101 --api custom
   ```

## Troubleshooting

### Common Issues

#### "Address already in use" Error
**Problem**: Port 3000 is occupied
**Solution**:
```bash
# Kill existing process
pkill -f "python3 app.py"
# Or use different port
python3 app.py --port 3001
```

#### No Results Found
**Problem**: Search returns empty results
**Solutions**:
1. Try different ZIP code
2. Reduce keyword specificity
3. Increase property limit
4. Check internet connection

#### Slow Performance
**Problem**: Searches take too long
**Solutions**:
1. Reduce property limit
2. Use fewer keywords
3. Check system resources
4. Use faster internet connection

#### API Errors
**Problem**: API calls failing
**Solutions**:
1. Verify API keys
2. Check API rate limits
3. Ensure internet connectivity
4. Switch to demo mode for testing

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid ZIP code" | Malformed ZIP | Use 5-digit format |
| "API key missing" | No API credentials | Add API key to config |
| "Rate limit exceeded" | Too many API calls | Wait or upgrade plan |
| "Network timeout" | Connection issues | Check internet |

### Performance Optimization

#### For Large Searches
1. **Use Appropriate Limits**: Start with 100 properties
2. **Optimize Keywords**: Use specific, relevant terms
3. **Batch Processing**: Split large areas into smaller ZIP codes
4. **Cache Results**: Save and reuse previous searches

#### System Requirements
- **Memory**: 8GB+ for 500+ property searches
- **CPU**: Multi-core recommended for large datasets
- **Storage**: 1GB+ for extensive result caching

## Advanced Features

### Export Functionality

#### JSON Export
- Complete property data
- Search parameters
- Confidence scores
- Matched keywords

#### CSV Export (Coming Soon)
- Spreadsheet-compatible format
- Customizable columns
- Bulk analysis ready

### Property Detail Pages

Access detailed property information:
- **URL Format**: `/property/<property_id>`
- **Investment Analysis**: ROI calculations
- **Market Comparisons**: Similar properties
- **Historical Data**: Price trends

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all strategies |
| `Ctrl+C` | Clear all strategies |
| `Enter` | Submit search |
| `Esc` | Clear search form |

### Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 80+ | Full |
| Firefox | 75+ | Full |
| Safari | 13+ | Full |
| Edge | 80+ | Full |

---

**Need Help?** Contact support@propertyincomefinder.com 