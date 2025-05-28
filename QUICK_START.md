# ⚡ Quick Start Guide - Property Income Finder

## 🚀 Get Started in 2 Minutes

### Step 1: Launch (30 seconds)
```bash
cd property-income-finder
python3 app.py
```
Open browser: `http://localhost:3000`

### Step 2: Search (1 minute)
1. **Enter ZIP Code**: `98101`
2. **Click Strategy**: "ADU-Focused Investment"
3. **Click**: "Search Properties"

### Step 3: Analyze (30 seconds)
- **Green badges** (80%+): Investigate immediately
- **Yellow badges** (60-79%): Add to watchlist
- **Red badges** (<60%): Consider if other factors align

## 🎯 Investment Strategies (Choose One)

| Strategy | Best For | Expected ROI | Investment Level |
|----------|----------|--------------|------------------|
| **ADU-Focused** | Immediate rental income | 15-25% | $50K-$150K |
| **Multi-Family** | Experienced investors | 8-15% | $200K-$500K+ |
| **Garage Conversion** | DIY investors | 20-30% | $30K-$80K |
| **House Hacking** | First-time investors | Offset mortgage | $10K-$50K |
| **RV/Boat Storage** | Passive income | $100-$300/month | $5K-$20K |

## 🔍 Quick Commands

### Web Interface
- **Select All Strategies**: Ctrl+A
- **Clear All**: Ctrl+C
- **Submit Search**: Enter

### Command Line
```bash
# Basic search
python3 property_income_finder.py 98101

# Custom keywords
python3 property_income_finder.py 98101 --keywords "adu" "duplex"

# Save results
python3 property_income_finder.py 98101 --output results.json
```

## 📊 Understanding Results

### Confidence Scores
- **90-100%**: 🟢 Excellent - Investigate immediately
- **80-89%**: 🟢 Very good - High priority
- **70-79%**: 🟡 Good - Worth investigating
- **60-69%**: 🟡 Moderate - Secondary priority
- **50-59%**: 🔴 Low - Consider other factors
- **<50%**: 🔴 Minimal potential

### Key Income Keywords
- **ADU**: accessory dwelling unit, guest house, casita
- **Multi-Family**: duplex, triplex, fourplex
- **Conversion**: large garage, basement, workshop
- **Hacking**: separate entrance, in-law suite
- **Storage**: RV parking, boat storage, large lot

## 💡 Quick Tips

### ✅ Do This
- Start with 100 property limit
- Use specific keywords
- Focus on 70%+ confidence scores
- Research local rental laws
- Calculate ROI before buying

### ❌ Avoid This
- Searching too many properties at once
- Using vague keywords like "nice"
- Ignoring confidence scores
- Skipping due diligence
- Emotional decision making

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| No results | Try different ZIP code or fewer keywords |
| Slow search | Reduce property limit to 50-100 |
| Port error | Kill existing process: `pkill -f "python3 app.py"` |
| API errors | Switch to demo mode (RentSpree) |

## 📱 Next Steps

1. **Complete Tutorial**: See [TUTORIAL.md](TUTORIAL.md)
2. **Read Manual**: Check [MANUAL.md](MANUAL.md)
3. **Join Community**: Connect with other investors
4. **Start Investing**: Begin with one property

---

**Ready to find your first income property?** 🏠💰

**Need help?** Check the full documentation or contact support. 