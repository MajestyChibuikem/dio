#!/usr/bin/env python3
"""
Test script to verify OpenAI fixes work correctly
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_openai_fixes():
    """Test the OpenAI utility functions"""
    print("Testing OpenAI fixes...")
    
    # Test imports
    try:
        from openai_utils import get_embeddings, create_chat_completion
        from _openai import getSummary, ask, summarise_commit
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test embeddings
    try:
        embedding = await get_embeddings("test text")
        if embedding and len(embedding) > 0:
            print("✅ Embeddings function works")
        else:
            print("❌ Embeddings function returned empty result")
    except Exception as e:
        print(f"❌ Embeddings error: {e}")
    
    # Test chat completion
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello"}
        ]
        result = await create_chat_completion(messages)
        if result and "hello" in result.lower():
            print("✅ Chat completion works")
        else:
            print("❌ Chat completion returned unexpected result")
    except Exception as e:
        print(f"❌ Chat completion error: {e}")
    
    # Test summary function
    try:
        summary = await getSummary("test.py", "print('hello world')")
        if summary and len(summary) > 0:
            print("✅ Summary function works")
        else:
            print("❌ Summary function returned empty result")
    except Exception as e:
        print(f"❌ Summary error: {e}")
    
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_openai_fixes()) 