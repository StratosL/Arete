import os

from litellm import completion

from app.core.config import settings

# Set API key for LiteLLM
os.environ["ANTHROPIC_API_KEY"] = settings.claude_api_key

async def get_llm_response(messages: list, model: str = "claude-sonnet-4-5") -> str:
    """Get response from Claude via LiteLLM"""
    try:
        response = completion(
            model=model,
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"LLM request failed: {e!s}")

async def stream_llm_response(messages: list, model: str = "claude-sonnet-4-5"):
    """Stream response from Claude via LiteLLM"""
    try:
        response = completion(
            model=model,
            messages=messages,
            temperature=0.1,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {e!s}"
