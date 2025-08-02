#!/usr/bin/env python3

import os
import weaviate
from dotenv import load_dotenv

load_dotenv()

print("🧪 Testing local Weaviate connection...")

try:
    # Initialize Weaviate client for local instance
    client = weaviate.WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="http://localhost:8080",
            grpc_port=50051
        )
    )
    
    print("✅ Weaviate client created successfully")
    
    # Connect to Weaviate
    client.connect()
    print("✅ Connected to Weaviate successfully")
    
    # Check if collection exists, if not create it
    try:
        index = client.collections.get("chatpdf")
        print("✅ Collection 'chatpdf' found")
    except Exception as e:
        print(f"⚠️ Collection 'chatpdf' not found, creating it...")
        # Create the collection
        client.collections.create(
            name="chatpdf",
            properties=[
                {"name": "source", "dataType": ["text"]},
                {"name": "code", "dataType": ["text"]},
                {"name": "summary", "dataType": ["text"]}
            ],
            vectorizer_config=weaviate.config.Configure.Vectorizer.none()
        )
        index = client.collections.get("chatpdf")
        print("✅ Created and connected to Weaviate collection")
    
    # Test inserting a simple object
    test_object = {
        "properties": {
            "source": "test.py",
            "code": "print('Hello World')",
            "summary": "A simple test script"
        },
        "vector": [0.1] * 1536  # OpenAI embedding dimension
    }
    
    try:
        index.data.insert(test_object)
        print("✅ Successfully inserted test object")
        
        # Test querying
        result = index.query.fetch_objects(limit=1)
        print(f"✅ Successfully queried {len(result.objects)} objects")
        
    except Exception as e:
        print(f"⚠️ Error with data operations: {e}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Make sure Weaviate is running with: ./setup-weaviate.sh")
finally:
    if 'client' in locals():
        client.close()

print("🧪 Test completed!") 