#!/usr/bin/env python3

import asyncio
import weaviate
from openai_utils import get_embeddings
from dotenv import load_dotenv

load_dotenv()

async def test_real_embeddings():
    print("🧪 Testing real embedding insertion...")
    
    # Generate real embedding
    test_text = "This is a test summary for embedding generation."
    embedding = await get_embeddings(test_text)
    
    if not embedding:
        print("❌ Failed to generate embedding")
        return
    
    print(f"✅ Generated embedding with {len(embedding)} dimensions")
    
    # Connect to Weaviate
    try:
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
            objects = index.query.fetch_objects(limit=100)
            for obj in objects.objects:
                index.data.delete_by_id(obj.uuid)
            print(f"✅ Deleted {len(objects.objects)} objects")
        except Exception as e:
            print(f"⚠️ Error clearing data: {e}")
        
        # Test real insertion
        test_object = {
            "properties": {
                "source": "test.py",
                "code": "print('Hello World')",
                "summary": test_text,
                "vector": embedding  # Store vector in properties
            }
        }
        
        print("📝 Test object structure:")
        print(f"  Properties: {test_object['properties']}")
        print(f"  Vector length: {len(embedding)}")
        
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
                # Check vector from the correct location
                if hasattr(obj.properties, 'vector'):
                    vector = obj.properties.vector
                    print(f"  Vector length: {len(vector) if vector else 0}")
                else:
                    print("  Vector: Not found in properties")
                    
        except Exception as e:
            print(f"❌ Insertion failed: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_real_embeddings()) 