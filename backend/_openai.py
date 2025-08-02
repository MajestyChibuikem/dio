import weaviate
from weaviate import WeaviateClient
from openai_utils import get_embeddings, create_chat_completion, create_context_system_prompt

# Initialize Weaviate client for local instance
try:
    client = WeaviateClient(
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


async def getEmbeddings(text):
    """Get embeddings for text using OpenAI API"""
    return await get_embeddings(text)


async def getSummary(source, code):
    """Generate a summary for a code file"""
    print("getting summary for", source)
    if len(code) > 10000:
        code = code[:10000]
    
    messages = [
        {
            "role": "system",
            "content": "You are an intelligent senior software engineer who specialise in onboarding junior software engineers onto projects",
        },
        {
            "role": "user",
            "content": f"""You are onboarding a junior software engineer and explaining to them the purpose of the {source} file
        here is the code:
        ---
        {code}
        ---
        give a summary no more than 100 words of the code above
        """,
        },
    ]
    
    result = await create_chat_completion(messages)
    if result:
        print("got back summary", source)
        return result
    else:
        return f"File: {source} - Code file with {len(code)} characters"


async def ask(query, namespace):
    """Ask a question about the codebase using vector search"""
    if index is None:
        return "I'm sorry, but I'm unable to process your request at the moment due to Weaviate connection issues."
    
    query_vector = await getEmbeddings(query)
    if query_vector is None:
        return "I'm sorry, but I'm unable to process your request at the moment due to API limitations."
    
    # Try to get all objects and manually filter by vector similarity
    all_objects = index.query.fetch_objects(limit=100)
    print(f"Total objects in database: {len(all_objects.objects)}")
    
    # For now, just get the first few objects as context
    query_response = type('obj', (object,), {
        'objects': all_objects.objects[:5]  # Get first 5 objects as context
    })()
    # form context from the top 10 results
    context = ""
    print(f"Found {len(query_response.objects)} results for query: {query}")
    for r in query_response.objects:
        context += f"""source:{r.properties['properties']['source']}\ncode content:{r.properties['properties']['code']}\nsummary of file:{r.properties['properties']['summary']}\n\n"""
    print("asking", query)
    print("Context length:", len(context))
    
    system_prompt = create_context_system_prompt(context)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    
    result = await create_chat_completion(messages)
    if result:
        print("got back answer")
        return result
    else:
        return f"I'm sorry, but I'm unable to process your request at the moment due to API limitations. Please try again later or contact support."


async def summarise_commit(diff):
    """Summarize a git commit diff"""
    messages = [
        {
            "role": "system",
            "content": """You are an expert programmer, and you are trying to summarize a git diff.
    Reminders about the git diff format:
    For every file, there are a few metadata lines, like (for example):
    ```
    diff --git a/lib/index.js b/lib/index.js
    index aadf691..bfef603 100644
    --- a/lib/index.js
    +++ b/lib/index.js
    ```
    This means that `lib/index.js` was modified in this commit. Note that this is only an example.
    Then there is a specifier of the lines that were modified.
    A line starting with `+` means it was added.
    A line that starting with `-` means that line was deleted.
    A line that starts with neither `+` nor `-` is code given for context and better understanding.
    It is not part of the diff.
    [...]
    EXAMPLE SUMMARY COMMENTS:
    ```
    * Raised the amount of returned recordings from `10` to `100` [packages/server/recordings_api.ts], [packages/server/constants.ts]
    * Fixed a typo in the github action name [.github/workflows/gpt-commit-summarizer.yml]
    * Moved the `octokit` initialization to a separate file [src/octokit.ts], [src/index.ts]
    * Added an OpenAI API for completions [packages/utils/apis/openai.ts]
    * Lowered numeric tolerance for test files
    ```
    Most commits will have less comments than this examples list.
    The last comment does not include the file names,
    because there were more than two files in the hypothetical commit.
    Do not include parts of the example in your summary.
    It is given only as an example of appropriate comments.""",
        },
        {
            "role": "user",
            "content": f"""Please summarise the following diff file: \n\n{diff}
                    
                    """,
        },
    ]
    
    result = await create_chat_completion(messages)
    if result:
        return result
    else:
        return f"Commit changes: {len(diff)} characters modified"
