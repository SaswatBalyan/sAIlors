#!/usr/bin/env python3
"""
Test script for sAIlors Business Feasibility Analyzer
This script tests the webapp functionality without requiring a browser
"""

import requests
import json
import time
import sys

def test_webapp():
    """Test the webapp endpoints and functionality"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing sAIlors Business Feasibility Analyzer")
    print("=" * 50)
    
    # Test 1: Check if webapp is running
    print("1. Testing webapp availability...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("   ✅ Webapp is running successfully")
        else:
            print(f"   ❌ Webapp returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Cannot connect to webapp: {e}")
        return False
    
    # Test 2: Check if the main page loads with correct content
    print("2. Testing main page content...")
    try:
        response = requests.get(base_url)
        content = response.text
        
        # Check for key elements
        checks = [
            ("sAIlors", "Brand name"),
            ("Business Feasibility Analyzer", "Main title"),
            ("Empowering Startups", "Hero section"),
            ("Location (lat,lng)", "Form field"),
            ("Business Type", "Form field"),
            ("Budget (in INR Lakhs)", "Form field")
        ]
        
        all_passed = True
        for check_text, description in checks:
            if check_text in content:
                print(f"   ✅ {description} found")
            else:
                print(f"   ❌ {description} not found")
                all_passed = False
        
        if not all_passed:
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking content: {e}")
        return False
    
    # Test 3: Test form submission (without API key, should show error)
    print("3. Testing form submission...")
    try:
        form_data = {
            'location': '28.6139,77.2090',
            'business': 'restaurant',
            'budget': '5',
            'extra_notes': 'Test submission'
        }
        
        response = requests.post(base_url, data=form_data, timeout=30)
        
        if response.status_code == 200:
            print("   ✅ Form submission successful")
            
            # Check if error message is shown (expected without API key)
            if "Error" in response.text or "API" in response.text:
                print("   ✅ Error handling working (expected without API key)")
            else:
                print("   ⚠️  No error message shown (API key might be configured)")
        else:
            print(f"   ❌ Form submission failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing form submission: {e}")
        return False
    
    print("\n🎉 All tests passed! The webapp is working correctly.")
    print("\n📝 Note: To test with full functionality, add your Google API key to business_feasibility/.env")
    print("   Get your free API key from: https://console.cloud.google.com/")
    
    return True

def main():
    """Main test function"""
    print("Starting webapp tests...")
    print("Make sure the webapp is running (./run_webapp.sh)")
    print()
    
    # Wait a moment for webapp to be ready
    time.sleep(2)
    
    success = test_webapp()
    
    if success:
        print("\n✅ Webapp test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Webapp test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
