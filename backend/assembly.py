# Start by making sure the `assemblyai` package is installed.
import os
import weaviate
from openai_utils import get_embeddings, create_chat_completion, create_context_system_prompt

# Initialize Weaviate client for local instance
try:
    client = weaviate.WeaviateClient(
        connection_params=weaviate.connect.ConnectionParams.from_url(
            url="http://localhost:8080",
            grpc_port=50051
        )
    )
    
    # Connect to Weaviate
    client.connect()
    
    # Check if collection exists, if not create it
    try:
        index = client.collections.get("chatpdf")
        print("✅ Connected to Weaviate successfully")
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
        
except Exception as e:
    print(f"⚠️ Warning: Could not connect to Weaviate: {e}")
    print("💡 Make sure Weaviate is running with: docker-compose -f weaviate-docker-compose.yml up")
    index = None


def serialise_url(url):
    return url.replace("/", "_")


# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.
def ms_to_time(ms):
    seconds = ms / 1000
    minutes = seconds / 60
    seconds = seconds % 60
    minutes = minutes % 60
    # format time
    return "%02d:%02d" % (minutes, seconds)


import assemblyai as aai

# Replace with your API token
aai.settings.api_key = os.getenv("AAI_TOKEN")


async def transcribe_file(url):
    config = aai.TranscriptionConfig(auto_chapters=True)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(url)
    summaries = []
    for chapter in transcript.chapters:
        summaries.append(
            {
                "start": ms_to_time(chapter.start),
                "end": ms_to_time(chapter.end),
                "gist": chapter.gist,
                "headline": chapter.headline,
                "summary": chapter.summary,
            }
        )

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=130)
    docs = splitter.create_documents([transcript.text])
    import asyncio

    embeddings = await asyncio.gather(
        *[get_embeddings(doc.page_content) for doc in docs]
    )
    print("getting embeddings for audio")
    
    # Check if any embeddings failed
    if any(emb is None for emb in embeddings):
        print("Warning: Some audio embeddings failed, skipping Weaviate insertion")
        return summaries
    
    for i, doc in enumerate(docs):
        doc.metadata["embeddings"] = embeddings[i]
    import hashlib

    # Prepare data for upsert
    objects_to_upsert = []
    for doc in docs:
        objects_to_upsert.append({
            "properties": {
                "page_content": doc.page_content,
                "vector": doc.metadata["embeddings"]
            }
        })
    
    # Upsert the objects using the correct method
    if index is None:
        print("⚠️ Warning: Weaviate not connected, skipping audio data insertion")
    else:
        try:
            index.data.insert_many(objects_to_upsert)
        except Exception as e:
            print(f"Error inserting data into Weaviate: {e}")
            # Fallback: insert one by one
            for obj in objects_to_upsert:
                try:
                    index.data.insert(obj)
                except Exception as insert_error:
                    print(f"Error inserting individual object: {insert_error}")
    print("upserted audio embeddings")
    return summaries


async def ask_meeting(url, query, quote):
    namespace = serialise_url(url)

    if index is None:
        return "I'm sorry, but I'm unable to process your question at the moment due to Weaviate connection issues."
    
    query_vector = await get_embeddings(query)
    if query_vector is None:
        return "I'm sorry, but I'm unable to process your question at the moment due to API limitations."
    
    query_response = index.query.near_vector(
        query_vector,
        limit=10,
        return_properties=["page_content"]
    )
    context = ""
    for r in query_response.objects:
        context += f"""meeting snippet: {r.properties["page_content"]}\n"""
    system_prompt = create_context_system_prompt(context)
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"I am asking a question in regards to this quote in the meeting: {quote}\n here is the question:"
            + query,
        },
    ]
    
    result = await create_chat_completion(messages)
    if result:
        print("got back answer for", query)
        return result
    else:
        return f"I'm sorry, but I'm unable to process your question at the moment due to API limitations. Please try again later."
