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
    """Test main API endpoint with real document"""
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/hackrx/run", 
                               headers=headers, 
                               json=data)
        
        print(f"API Test: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Got {len(result['answers'])} answers")
            print(f"Total processing time: {result['total_processing_time']:.2f}s")
            print(f"Request ID: {result['request_id']}")
            
            # Print first answer as example
            if result['answers']:
                first_answer = result['answers'][0]
                print(f"\nSample Answer:")
                print(f"Q: {first_answer['question']}")
                print(f"A: {first_answer['answer'][:200]}...")
                print(f"Confidence: {first_answer['confidence']:.2f}")
                print(f"Source chunks: {len(first_answer['source_chunks'])}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
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
