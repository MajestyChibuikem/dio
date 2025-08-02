#!/usr/bin/env python3

import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

print("Testing simple Weaviate connection...")

try:
    # Initialize Weaviate client with new API
    client = weaviate.WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="https://asia-southeast1-gcp-free.weaviate.network",
            grpc_port=50051
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