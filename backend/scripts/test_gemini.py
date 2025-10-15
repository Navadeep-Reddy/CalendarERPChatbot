#!/usr/bin/env python3
"""
Test script to verify Google Gemini API connection
Run this to make sure your API key is working before starting the server
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_gemini_connection():
    """Test the Gemini API connection"""
    print("🔍 Testing Google Gemini API Connection...")
    print("=" * 50)
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            print("❌ ERROR: GOOGLE_API_KEY not found in environment")
            print("   Please add it to your .env file")
            print("   Get your free key from: https://aistudio.google.com/app/apikey")
            return False
        
        if api_key == "your_google_api_key_here":
            print("❌ ERROR: Please replace the placeholder API key in .env")
            print("   Get your free key from: https://aistudio.google.com/app/apikey")
            return False
        
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
        
        # Try to import required packages
        print("\n📦 Checking dependencies...")
        try:
            from google import genai
            print("✅ google-genai installed")
        except ImportError:
            print("❌ google-genai not installed")
            print("   Run: pip install -r requirements.txt")
            return False
        
        # Try to initialize the client
        print("\n🤖 Initializing Gemini client...")
        try:
            client = genai.Client(api_key=api_key)
            print("✅ Client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize client: {str(e)}")
            return False
        
        # Try a simple query
        print("\n💬 Testing with a simple query...")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Say 'Hello, I am working!' in one sentence."
            )
            print(f"✅ Response received: {response.text}")
        except Exception as e:
            print(f"❌ Query failed: {str(e)}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Gemini API is working correctly!")
        print("=" * 50)
        print("\n✨ You're all set! You can now:")
        print("   1. Initialize the vector store: python scripts/initialize_db.py")
        print("   2. Start the server: ./run.sh")
        print("   3. Test the chatbot at: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_gemini_connection()
    sys.exit(0 if success else 1)
