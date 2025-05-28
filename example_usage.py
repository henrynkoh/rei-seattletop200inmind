#!/usr/bin/env python3
"""
Example usage script for Property Income Finder
Demonstrates different investment strategies and search patterns
"""

import subprocess
import sys
from config import INVESTMENT_STRATEGIES

def run_search(zip_code, strategy_name, keywords=None, output_file=None):
    """Run a property search with specific parameters"""
    cmd = ['python', 'property_income_finder.py', zip_code]
    
    if keywords:
        cmd.extend(['--keywords'] + keywords)
    
    if output_file:
        cmd.extend(['--output', output_file])
    
    cmd.extend(['--show-limit', '5'])  # Show fewer results for demo
    
    print(f"\n{'='*60}")
    print(f"RUNNING SEARCH: {strategy_name.upper()}")
    print(f"ZIP Code: {zip_code}")
    print(f"Keywords: {keywords if keywords else 'Default'}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running search: {e}")

def main():
    """Run example searches for different investment strategies"""
    
    # Example ZIP codes (you can change these)
    zip_codes = ['98101', '90210', '78701']  # Seattle, Beverly Hills, Austin
    
    print("Property Income Finder - Example Usage")
    print("This script demonstrates different investment strategies")
    
    for zip_code in zip_codes:
        print(f"\n\nSEARCHING IN ZIP CODE: {zip_code}")
        print("="*80)
        
        # 1. ADU-Focused Strategy
        run_search(
            zip_code=zip_code,
            strategy_name="ADU-Focused Investment",
            keywords=INVESTMENT_STRATEGIES['adu_focused'][:5],  # Use first 5 keywords
            output_file=f"adu_results_{zip_code}.json"
        )
        
        # 2. Multi-Family Strategy
        run_search(
            zip_code=zip_code,
            strategy_name="Multi-Family Investment",
            keywords=INVESTMENT_STRATEGIES['multi_family'][:5],
            output_file=f"multifamily_results_{zip_code}.json"
        )
        
        # 3. Garage Conversion Strategy
        run_search(
            zip_code=zip_code,
            strategy_name="Garage Conversion Potential",
            keywords=INVESTMENT_STRATEGIES['garage_conversion'][:5],
            output_file=f"garage_results_{zip_code}.json"
        )
        
        # 4. House Hacking Strategy
        run_search(
            zip_code=zip_code,
            strategy_name="House Hacking Opportunities",
            keywords=INVESTMENT_STRATEGIES['house_hacking'][:5],
            output_file=f"househack_results_{zip_code}.json"
        )
        
        # 5. Custom High-Value Search
        custom_keywords = [
            "revenue generating", "rental income", "investment property",
            "cash flow", "tenant occupied"
        ]
        run_search(
            zip_code=zip_code,
            strategy_name="High-Value Investment Properties",
            keywords=custom_keywords,
            output_file=f"highvalue_results_{zip_code}.json"
        )

def demo_single_search():
    """Run a single demonstration search"""
    print("\nRunning single demonstration search...")
    
    # Get ZIP code from user or use default
    zip_code = input("Enter ZIP code (or press Enter for 98101): ").strip()
    if not zip_code:
        zip_code = "98101"
    
    # Run basic search
    run_search(
        zip_code=zip_code,
        strategy_name="Basic Income Property Search",
        keywords=None,
        output_file=f"demo_results_{zip_code}.json"
    )

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_single_search()
    else:
        main()
        
        print("\n" + "="*80)
        print("EXAMPLE SEARCHES COMPLETED")
        print("="*80)
        print("\nResults have been saved to JSON files for each strategy.")
        print("You can also run a single demo search with:")
        print("python example_usage.py --demo")
        print("\nTo run your own custom searches, use:")
        print("python property_income_finder.py [ZIP_CODE] [OPTIONS]")
        print("\nSee README.md for more detailed usage instructions.") 