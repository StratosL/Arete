from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_globals, safe_builtins, guarded_unpack_sequence
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, BinaryContent
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from httpx import AsyncClient
from supabase import Client
import base64
import json
import sys
import os
import re

embedding_model = os.getenv("EMBEDDING_MODEL_CHOICE") or "text-embedding-3-small"


async def get_embedding(text: str, embedding_client: AsyncOpenAI) -> List[float]:
    """Get embedding vector from OpenAI."""
    try:
        response = await embedding_client.embeddings.create(model=embedding_model, input=text)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return [0] * 1536  # Return zero vector on error


async def retrieve_relevant_documents_tool(
    supabase: Client,
    embedding_client: AsyncOpenAI,
    user_query: str,
    file_id: Optional[str] = None,
    tag: Optional[str] = None,
) -> str:
    """
    Function to retrieve relevant document chunks with RAG.
    This is called by the retrieve_relevant_documents tool for the agent.

    Args:
        supabase: Supabase client instance
        embedding_client: OpenAI client for embeddings
        user_query: The user's search query
        file_id: Optional file ID to filter results to a specific file
        tag: Optional tag to filter results to documents with that tag

    Returns:
        str: Formatted string of relevant document chunks with metadata
    """
    try:
        # Get the embedding for the query
        query_embedding = await get_embedding(user_query, embedding_client)

        # Build filter object
        filter_obj = {}
        if file_id:
            filter_obj["file_id"] = file_id
        elif tag:
            # First get document IDs with this tag
            tagged_docs = await get_documents_by_tag_tool(supabase, tag)
            if not tagged_docs:
                return f"No documents found with tag '{tag}'."

            # We need to query chunks from documents with this tag
            # Since we can't do IN clause directly in the RPC, we'll need to do multiple queries
            # or modify the approach to use the file_ids
            all_chunks = []
            for doc in tagged_docs[:10]:  # Limit to prevent too many queries
                result = supabase.rpc(
                    "match_documents",
                    {
                        "query_embedding": query_embedding,
                        "match_count": 1,
                        "filter": {"file_id": doc["id"]},
                    },
                ).execute()
                if result.data:
                    all_chunks.extend(result.data)

            # Sort by similarity and take top 4
            all_chunks.sort(key=lambda x: x.get("similarity", 0), reverse=True)
            result_data = all_chunks[:4]
        else:
            # No filtering, standard query
            result = supabase.rpc(
                "match_documents",
                {"query_embedding": query_embedding, "match_count": 4, "filter": filter_obj},
            ).execute()
            result_data = result.data

        if not result_data:
            return "No relevant documents found."

        # Format the results
        formatted_chunks = []
        for doc in result_data:
            chunk_text = f"""
# Document ID: {doc["metadata"].get("file_id", "unknown")}      
# Document Tilte: {doc["metadata"].get("file_title", "unknown")}
# Document URL: {doc["metadata"].get("file_url", "unknown")}
# Document Tags: {doc["metadata"].get("tags", "unknown")}

{doc["content"]}
"""
            formatted_chunks.append(chunk_text)

        # Join all chunks with a separator
        return "\n\n---\n\n".join(formatted_chunks)

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return f"Error retrieving documents: {str(e)}"


async def list_documents_tool(supabase: Client) -> List[str]:
    """
    Function to retrieve a list of all available documents.
    This is called by the list_documents tool for the agent.

    Returns:
        List[str]: List of documents including their metadata (URL/path, schema if applicable, etc.)
    """
    try:
        # Query Supabase for unique documents
        result = (
            supabase.from_("document_metadata").select("id, title, schema, url, tags").execute()
        )

        return str(result.data)

    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return str([])


async def get_document_content_tool(supabase: Client, document_id: str) -> str:
    """
    Retrieve the full content of a specific document by combining all its chunks.
    This is called by the get_document_content tool for the agent.

    Returns:
        str: The complete content of the document with all chunks combined in order
    """
    try:
        # Query Supabase for all chunks for this document
        result = (
            supabase.from_("documents")
            .select("id, content, metadata")
            .eq("metadata->>file_id", document_id)
            .order("id")
            .execute()
        )

        if not result.data:
            return f"No content found for document: {document_id}"

        # Format the document with its title and all chunks
        document_title = result.data[0]["metadata"]["file_title"].split(" - ")[
            0
        ]  # Get the main title
        formatted_content = [f"# {document_title}\n"]

        # Add each chunk's content
        for chunk in result.data:
            formatted_content.append(chunk["content"])

        # Join everything together but limit the characters in case the document is massive
        return "\n\n".join(formatted_content)[:20000]

    except Exception as e:
        print(f"Error retrieving document content: {e}")
        return f"Error retrieving document content: {str(e)}"


async def list_available_tags_tool(supabase: Client) -> List[str]:
    """
    Get all unique tags from document metadata that appear in at least 2 documents.

    Args:
        supabase: Supabase client instance

    Returns:
        List[str]: Sorted list of unique tags found in 2+ documents
    """
    try:
        # Query all tags from document_metadata table
        result = supabase.table("document_metadata").select("tags").execute()

        # Count tag occurrences
        tag_counts = {}
        for doc in result.data:
            if doc.get("tags"):
                # Handle both JSON string and list formats
                tags = doc["tags"]
                if isinstance(tags, str):
                    try:
                        tags = json.loads(tags)
                    except:
                        continue
                if isinstance(tags, list):
                    for tag in tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Filter tags that appear in at least 2 documents
        common_tags = [tag for tag, count in tag_counts.items() if count >= 2]

        # Return sorted list
        return sorted(common_tags)
    except Exception as e:
        print(f"Error fetching tags: {e}")
        return []


async def get_documents_by_tag_tool(supabase: Client, tag: str) -> List[Dict[str, Any]]:
    """
    Get document titles and IDs that contain a specified tag.

    Args:
        supabase: Supabase client instance
        tag: The tag to search for

    Returns:
        List[Dict]: List of documents with id, title, url, and tags
    """
    try:
        # Query documents containing the specified tag
        result = supabase.table("document_metadata").select("id, title, url, tags").execute()

        # Filter documents that contain the tag
        matching_docs = []
        for doc in result.data:
            if doc.get("tags"):
                # Handle both JSON string and list formats
                tags = doc["tags"]
                if isinstance(tags, str):
                    try:
                        tags = json.loads(tags)
                    except:
                        continue
                if isinstance(tags, list) and tag in tags:
                    matching_docs.append(
                        {"id": doc["id"], "title": doc["title"], "url": doc["url"], "tags": tags}
                    )

        return matching_docs
    except Exception as e:
        print(f"Error fetching documents by tag: {e}")
        return []
