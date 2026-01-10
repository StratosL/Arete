"""
Unit tests for LLM wrapper
"""
from unittest.mock import patch, Mock
import pytest

from app.core.llm import get_llm_response, stream_llm_response


class TestLLMWrapper:
    """Test LLM wrapper functions"""

    @pytest.mark.asyncio
    async def test_get_llm_response_success(self):
        """Test successful LLM response"""
        messages = [{"role": "user", "content": "Test message"}]
        expected_response = "Test response from Claude"

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = expected_response

        with patch('app.core.llm.completion', return_value=mock_response):
            result = await get_llm_response(messages)
            assert result == expected_response

    @pytest.mark.asyncio
    async def test_get_llm_response_with_custom_model(self):
        """Test LLM response with custom model"""
        messages = [{"role": "user", "content": "Test"}]
        custom_model = "claude-haiku-4"

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Response"

        with patch('app.core.llm.completion') as mock_completion:
            mock_completion.return_value = mock_response
            
            await get_llm_response(messages, model=custom_model)
            
            mock_completion.assert_called_once_with(
                model=custom_model,
                messages=messages,
                temperature=0.1
            )

    @pytest.mark.asyncio
    async def test_get_llm_response_error(self):
        """Test LLM response error handling"""
        messages = [{"role": "user", "content": "Test"}]

        with patch('app.core.llm.completion', side_effect=Exception("API Error")):
            with pytest.raises(Exception, match="LLM request failed: API Error"):
                await get_llm_response(messages)

    @pytest.mark.asyncio
    async def test_stream_llm_response_success(self):
        """Test successful streaming LLM response"""
        messages = [{"role": "user", "content": "Test"}]
        
        # Mock streaming chunks
        mock_chunks = [
            Mock(choices=[Mock(delta=Mock(content="Hello"))]),
            Mock(choices=[Mock(delta=Mock(content=" world"))]),
            Mock(choices=[Mock(delta=Mock(content="!"))])
        ]

        with patch('app.core.llm.completion', return_value=mock_chunks):
            chunks = []
            async for chunk in stream_llm_response(messages):
                chunks.append(chunk)
            
            assert chunks == ["Hello", " world", "!"]

    @pytest.mark.asyncio
    async def test_stream_llm_response_with_none_content(self):
        """Test streaming response with None content chunks"""
        messages = [{"role": "user", "content": "Test"}]
        
        mock_chunks = [
            Mock(choices=[Mock(delta=Mock(content="Hello"))]),
            Mock(choices=[Mock(delta=Mock(content=None))]),  # None content
            Mock(choices=[Mock(delta=Mock(content="world"))])
        ]

        with patch('app.core.llm.completion', return_value=mock_chunks):
            chunks = []
            async for chunk in stream_llm_response(messages):
                chunks.append(chunk)
            
            # Should skip None content
            assert chunks == ["Hello", "world"]

    @pytest.mark.asyncio
    async def test_stream_llm_response_error(self):
        """Test streaming response error handling"""
        messages = [{"role": "user", "content": "Test"}]

        with patch('app.core.llm.completion', side_effect=Exception("Stream Error")):
            chunks = []
            async for chunk in stream_llm_response(messages):
                chunks.append(chunk)
            
            assert len(chunks) == 1
            assert "Error: Stream Error" in chunks[0]

    @pytest.mark.asyncio
    async def test_stream_llm_response_custom_model(self):
        """Test streaming with custom model"""
        messages = [{"role": "user", "content": "Test"}]
        custom_model = "claude-opus-4"
        
        mock_chunks = [Mock(choices=[Mock(delta=Mock(content="test"))])]

        with patch('app.core.llm.completion') as mock_completion:
            mock_completion.return_value = mock_chunks
            
            async for _ in stream_llm_response(messages, model=custom_model):
                break
            
            mock_completion.assert_called_once_with(
                model=custom_model,
                messages=messages,
                temperature=0.1,
                stream=True
            )