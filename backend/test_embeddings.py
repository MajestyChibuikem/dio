#!/usr/bin/env python3

import asyncio
from openai_utils import get_embeddings

async def test_embeddings():
    print("🧪 Testing embedding generation...")
    
    test_text = "This is a test summary for embedding generation."
    
    print(f"📝 Test text: {test_text}")
    
    embedding = await get_embeddings(test_text)
    
    if embedding:
        print(f"✅ Embedding generated successfully!")
        print(f"📊 Embedding length: {len(embedding)}")
        print(f"📊 First 5 values: {embedding[:5]}")
        print(f"📊 Last 5 values: {embedding[-5:]}")
    else:
        print("❌ Embedding generation failed!")
    
    return embedding

if __name__ == "__main__":
    asyncio.run(test_embeddings()) 