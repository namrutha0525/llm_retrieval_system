#!/usr/bin/env python3

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
BEARER_TOKEN = "479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_api():
    """Test main API endpoint"""
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "documents": "https://example.com/test.pdf",
        "questions": [
            "What is this document about?",
            "What are the main points?"
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/hackrx/run", 
                               headers=headers, 
                               json=data)
        print(f"API Test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Answers: {result}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing LLM Retrieval API v2...")
    print("=" * 50)

    if test_health():
        print("✅ Health check passed")
    else:
        print("❌ Health check failed")
        exit(1)

    if test_api():
        print("✅ API test passed")
    else:
        print("❌ API test failed")
        exit(1)

    print("🎉 All tests passed!")
