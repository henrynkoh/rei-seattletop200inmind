# Property Income Finder - Screenshot Guide

This guide provides detailed instructions for capturing, editing, and maintaining screenshots for the Property Income Finder application.

## 📸 Screenshot Requirements

### Technical Specifications
- **Resolution**: 1920x1080 (Full HD) minimum
- **Format**: PNG with transparency support
- **Quality**: High-resolution, crisp text
- **Browser**: Chrome or Safari for consistency
- **Device**: Desktop/laptop (mobile screenshots separate)

### Visual Standards
- **Clean Interface**: Remove test data, use realistic property information
- **Professional Data**: Use actual Seattle/Bellevue area properties when possible
- **Consistent Branding**: Maintain color scheme (#667eea primary, #764ba2 secondary)
- **Privacy**: Blur or anonymize personal information
- **Lighting**: Consistent lighting and contrast

## 🖼️ Required Screenshots

### 1. Main Interface (`main-interface.png`)
**Purpose**: Show the primary property search interface

**Content to Include**:
- Header with Property Income Finder branding
- ZIP code search input (example: "98092")
- Investment strategy dropdown (showing "ADU-Focused Investment")
- Property type filters (Single Family, Duplex, etc.)
- Search button prominently displayed
- Clean, modern gradient background

**Sample Data**:
```
ZIP Code: 98092
Strategy: ADU-Focused Investment
Property Types: ☑ Single Family ☑ Duplex ☐ Condo
```

### 2. Search Results (`search-results.png`)
**Purpose**: Display property search results with investment analysis

**Content to Include**:
- Search results header showing "23 properties found"
- 3-4 property cards visible
- Each card showing:
  - Property address (e.g., "1234 Maple St, Auburn, WA 98092")
  - Price ($450,000 - $650,000 range)
  - Confidence score (80%+, 60-79%, <60% examples)
  - Investment metrics (Cash flow, Cap rate)
  - Property details (beds/baths/sqft)
- Export button visible
- Professional card layout with hover effects

**Sample Properties**:
```
Property 1: 1234 Maple St, Auburn, WA 98092
Price: $485,000 | 3BR/2BA | 1,850 sqft
Confidence: 87% | Cash Flow: +$650/month

Property 2: 5678 Oak Ave, Federal Way, WA 98003
Price: $425,000 | 4BR/2.5BA | 2,100 sqft
Confidence: 72% | Cash Flow: +$450/month
```

### 3. Property Details (`property-details.png`)
**Purpose**: Show detailed property information and investment analysis

**Content to Include**:
- Property header with address and price
- Property statistics (beds, baths, sqft, lot size)
- Photo gallery (3-4 property images)
- Property description
- Key features list with checkmarks
- Investment potential sidebar
- Contact information
- Back to search button

**Sample Property**:
```
Address: 1234 Maple Street, Auburn, WA 98092
Price: $485,000
Type: Single Family Home
Beds: 3 | Baths: 2 | Sqft: 1,850 | Lot: 0.25 acres
Year Built: 1995

Features:
✓ Detached ADU with separate entrance
✓ Large 3-car garage with high ceilings
✓ Workshop space in garage
✓ Full kitchen in ADU
```

### 4. User Dashboard (`dashboard.png`)
**Purpose**: Display user portfolio and dashboard functionality

**Content to Include**:
- Sidebar navigation (Dashboard, Search, Calculator, Portfolio, etc.)
- Welcome message with user name
- Portfolio metrics cards:
  - Total Portfolio Value: $1,420,000
  - Properties Owned: 3
  - Monthly Income: $8,400
  - Net Margin: 68.2%
- Portfolio properties table
- Recent searches section
- Quick action buttons

**Sample Portfolio Data**:
```
Property 1: 123 Rental Ave, Seattle, WA 98092
Purchase: $450,000 | Current: $475,000 | Rent: $3,200

Property 2: 456 Investment St, Bellevue, WA 98004
Purchase: $650,000 | Current: $680,000 | Rent: $4,500

Property 3: 789 Income Blvd, Tacoma, WA 98402
Purchase: $320,000 | Current: $340,000 | Rent: $2,800
```

### 5. Investment Calculator (`investment-calculator.png`)
**Purpose**: Show the investment calculator modal/interface

**Content to Include**:
- Calculator modal overlay
- Input fields:
  - Purchase Price: $485,000
  - Down Payment: 20%
  - Interest Rate: 6.5%
  - Monthly Rent: $3,500
  - Monthly Expenses: $800
- Results section showing:
  - Monthly Cash Flow: +$1,100
  - Cash-on-Cash Return: 13.2%
  - Cap Rate: 7.2%
  - 1% Rule: 0.72% ❌
- Professional form styling

### 6. Login Interface (`login-page.png`)
**Purpose**: Show the authentication interface

**Content to Include**:
- Split-screen layout
- Left side: Login form with username/password fields
- Right side: Platform features list
- Demo account credentials visible
- Gradient background
- Professional branding
- "Back to Property Search" link

**Demo Credentials**:
```
Username: demo
Password: demo123
```

## 📱 Mobile Screenshots (Optional)

### Mobile Interface (`mobile-interface.png`)
- Responsive design on mobile device
- Touch-friendly interface elements
- Collapsed navigation menu
- Mobile-optimized property cards

## 🛠️ Screenshot Capture Process

### Step 1: Environment Setup
1. Open Chrome browser in incognito mode
2. Set browser window to 1920x1080 resolution
3. Navigate to `http://localhost:3001`
4. Clear any existing data/cookies

### Step 2: Data Preparation
1. Login with demo account (username: demo, password: demo123)
2. Perform sample searches to populate recent activity
3. Ensure portfolio has sample properties
4. Use realistic Seattle-area property data

### Step 3: Capture Process
1. Navigate to target page/interface
2. Ensure all elements are loaded
3. Remove any loading indicators
4. Use browser's built-in screenshot tool or:
   - macOS: Cmd+Shift+4, then spacebar, click window
   - Windows: Windows+Shift+S
   - Linux: Use Gnome Screenshot or similar

### Step 4: Post-Processing
1. Crop to remove browser chrome if needed
2. Ensure text is crisp and readable
3. Verify colors match brand guidelines
4. Compress for web (keep under 500KB per image)
5. Save as PNG with descriptive filename

## 🔧 Tools and Software

### Screenshot Capture
- **Browser Built-in**: Chrome DevTools, Firefox Screenshot
- **macOS**: Cmd+Shift+4, CleanShot X, Skitch
- **Windows**: Snipping Tool, Greenshot, LightShot
- **Linux**: Gnome Screenshot, Shutter, Flameshot

### Image Editing
- **Professional**: Adobe Photoshop, Sketch, Figma
- **Free**: GIMP, Paint.NET, Canva
- **Online**: Photopea, Pixlr, Remove.bg

### Optimization
- **Compression**: TinyPNG, ImageOptim, Squoosh
- **Format Conversion**: CloudConvert, Online-Convert
- **Batch Processing**: ImageMagick, XnConvert

## 📋 Quality Checklist

Before publishing screenshots, verify:

- [ ] Resolution is 1920x1080 or higher
- [ ] Text is crisp and readable
- [ ] Colors match brand guidelines
- [ ] No personal/sensitive information visible
- [ ] Realistic property data used
- [ ] All UI elements properly loaded
- [ ] File size under 500KB
- [ ] Filename follows naming convention
- [ ] Alt text provided in documentation

## 🔄 Update Schedule

Screenshots should be updated when:
- Major UI changes are implemented
- New features are added
- Branding/design changes occur
- User feedback indicates confusion
- Quarterly review (minimum)

## 📞 Contact

For questions about screenshot standards or assistance:
- **Technical Lead**: Property Income Finder Team
- **Documentation**: docs@propertyincomefinder.com
- **Design Review**: design@propertyincomefinder.com

---

*Last Updated: December 2024*
*Version: 1.0* 