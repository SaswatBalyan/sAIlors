#!/usr/bin/env python3
"""
sAIlor API Test Script
Tests the backend API endpoints to ensure functionality
"""

import requests
import json
import time
import sys

# Configuration
API_BASE = "http://localhost:8000"
TEST_TIMEOUT = 30

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Geospatial available: {data['geospatial_available']}")
            print(f"   Requests available: {data['requests_available']}")
            print(f"   Model loaded: {data['model_loaded']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_analyze():
    """Test the analyze endpoint"""
    print("\n🔍 Testing analyze endpoint...")
    
    test_payload = {
        "business_type": "cafe",
        "city": "Vellore",
        "lat": 12.9698,
        "lon": 79.1559,
        "radius_m": 500,
        "budget_lakh": 10.0,
        "seating_capacity": 30,
        "open_hours": "08:00-22:00",
        "use_population_density": True,
        "consider_competition": True,
        "notes": "Test analysis for sAIlor"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/analyze", 
            json=test_payload, 
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis endpoint working")
            print(f"   Summary: {data['summary'][:100]}...")
            print(f"   Scores: Demand={data['scores']['demand']}, Risk={data['scores']['risk']}, Competition={data['scores']['competition']}")
            print(f"   Pros: {len(data['pros'])} items")
            print(f"   Cons: {len(data['cons'])} items")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Analysis request failed: {e}")
        return False

def test_predict():
    """Test the predict endpoint"""
    print("\n🔍 Testing predict endpoint...")
    
    test_payload = {
        "business_type": "cafe",
        "city": "Vellore",
        "budget_lakh": 10.0,
        "seating_capacity": 30,
        "radius_m": 500,
        "demand_score": 75.0
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/predict", 
            json=test_payload, 
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction endpoint working")
            print(f"   Prediction: {data['prediction']}")
            print(f"   Confidence: {data['confidence']:.2f}")
            if 'probabilities' in data:
                print(f"   Probabilities: {data['probabilities']}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction request failed: {e}")
        return False

def test_root():
    """Test the root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root request failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 sAIlor API Test Suite")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE}/health", timeout=2)
            if response.status_code == 200:
                break
        except:
            pass
        if i < max_retries - 1:
            print(f"   Retry {i+1}/{max_retries}...")
            time.sleep(2)
    else:
        print("❌ API not responding after maximum retries")
        print("   Make sure the backend is running: uvicorn app.main:app --app-dir backend --reload --port 8000")
        sys.exit(1)
    
    # Run tests
    tests = [
        test_root,
        test_health,
        test_analyze,
        test_predict
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! sAIlor API is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
