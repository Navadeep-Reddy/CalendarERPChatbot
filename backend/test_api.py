#!/usr/bin/env python3
"""
Simple test script for the RAG chatbot API
"""
import requests
import json

def test_chat_endpoint():
    """Test the chat endpoint with sample queries"""
    url = "http://localhost:8000/chat"
    
    queries = [
        "When are the mid-term exams for Fall 2024?",
        "When does the Spring semester start?",
        "Are there any holidays in November?",
        "When is the final exam period?"
    ]
    
    print("🧪 Testing RAG Chatbot API\n")
    print("=" * 80)
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 80)
        
        try:
            response = requests.post(
                url,
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Answer: {data['answer']}\n")
                
                if data.get('sources'):
                    print(f"📚 Sources ({len(data['sources'])} documents):")
                    for idx, source in enumerate(data['sources'][:2], 1):  # Show first 2 sources
                        print(f"\n  Source {idx}:")
                        print(f"  Title: {source['metadata'].get('title', 'N/A')}")
                        print(f"  Date: {source['metadata'].get('start_date', 'N/A')}")
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to server. Is it running on http://localhost:8000?")
            return
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("✅ Testing complete!\n")


def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"🏥 Health Check: {data['status']}")
            print(f"📦 Version: {data['version']}")
            print(f"⏰ Timestamp: {data['timestamp']}\n")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8000")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Calendar ERP Chatbot - API Test Suite")
    print("=" * 80 + "\n")
    
    if test_health_endpoint():
        test_chat_endpoint()
    else:
        print("\n⚠️  Server is not running. Please start it first with:")
        print("   cd backend && python -m uvicorn app.main:app --reload\n")
