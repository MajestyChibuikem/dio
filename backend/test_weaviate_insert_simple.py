#!/usr/bin/env python3

import weaviate
from dotenv import load_dotenv

load_dotenv()

print("🧪 Testing simple Weaviate insertion...")

try:
    # Initialize Weaviate client
    client = weaviate.WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="http://localhost:8080",
            grpc_port=50051
        )
    )
    
    client.connect()
    index = client.collections.get("chatpdf")
    
    # Clear existing data
    print("🗑️ Clearing existing data...")
    try:
        # Get all objects and delete them
        objects = index.query.fetch_objects(limit=100)
        for obj in objects.objects:
            index.data.delete_by_id(obj.uuid)
        print(f"✅ Deleted {len(objects.objects)} objects")
    except Exception as e:
        print(f"⚠️ Error clearing data: {e}")
    
    # Test simple insertion
    test_object = {
        "properties": {
            "source": "test.py",
            "code": "print('Hello World')",
            "summary": "A simple test script"
        },
        "vector": [0.1] * 1536
    }
    
    print("📝 Test object structure:")
    print(test_object)
    
    # Try insertion
    try:
        result = index.data.insert(test_object)
        print(f"✅ Insertion successful: {result}")
        
        # Check if data was inserted
        objects = index.query.fetch_objects(limit=5)
        print(f"📊 Found {len(objects.objects)} objects")
        
        for i, obj in enumerate(objects.objects):
            print(f"Object {i}:")
            print(f"  UUID: {obj.uuid}")
            print(f"  Properties: {obj.properties}")
            print(f"  Vector length: {len(obj.vector) if obj.vector else 0}")
            
    except Exception as e:
        print(f"❌ Insertion failed: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()

print("🧪 Test completed!") 