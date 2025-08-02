"""
Shared OpenAI utilities to eliminate redundancy between modules
"""
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client once for the entire application
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Shared system prompt for AI assistant
AI_ASSISTANT_SYSTEM_PROMPT = """
AI assistant is a brand new, powerful, human-like artificial intelligence.
The traits of AI include expert knowledge, helpfulness, cleverness, and articulateness.
AI is a well-behaved and well-mannered individual.
AI will answer all questions in the HTML format. including code snippets, proper HTML formatting
AI is always friendly, kind, and inspiring, and he is eager to provide vivid and thoughtful responses to the user.
AI has the sum of all knowledge in their brain, and is able to accurately answer nearly any question about any topic in conversation.
If the question is asking about code or a specific file, AI will provide the detailed answer, giving step by step instructions, including code snippets.
AI assistant will not apologize for previous responses, but instead will indicated new information was gained.
AI assistant will not invent anything that is not drawn directly from the context.
"""

def create_context_system_prompt(context):
    """Create a system prompt with context"""
    return f"""
{AI_ASSISTANT_SYSTEM_PROMPT}
START CONTEXT BLOCK
{context}
END OF CONTEXT BLOCK
AI assistant will take into account any CONTEXT BLOCK that is provided in a conversation.
If the context does not provide the answer to question, the AI assistant will say, "I'm sorry, but I don't know the answer to that question".
"""

async def create_chat_completion(messages, model="gpt-3.5-turbo"):
    """Create a chat completion with error handling"""
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"I'm sorry, but I'm unable to process your request at the moment due to API limitations. Please try again later."

async def get_embeddings(text):
    """Get embeddings for text using OpenAI API"""
    try:
        response = openai_client.embeddings.create(
            input=text.replace("\n", ""), model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"OpenAI embeddings error: {e}")
        return None 