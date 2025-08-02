#!/usr/bin/env python3

import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

print("Testing Weaviate connection...")

try:
    # Initialize Weaviate client with new API
    client = weaviate.WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="https://asia-southeast1-gcp-free.weaviate.network",
            auth_client_secret=weaviate.auth.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY")),
            headers={
                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
            }
        )
    )
    
    print("✅ Weaviate client created successfully")
    
    # Try to get the collection
    try:
        index = client.collections.get("chatpdf")
        print("✅ Collection 'chatpdf' found")
    except Exception as e:
        print(f"❌ Error getting collection: {e}")
        
except Exception as e:
    print(f"❌ Error creating Weaviate client: {e}")

print("Test completed!") 