# 2. Use LiteLLM for Multi-Provider LLM Abstraction

**Date**: 2026-01-05
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: llm, integration, abstraction

## Context

Arete needs to call Claude API for:
- Resume parsing (PDF→Markdown→JSON)
- Job analysis (extract requirements)
- AI optimization (suggest improvements)
- Cover letter generation

We could integrate directly with Anthropic's API, but this locks us into one provider.

## Decision Drivers

* Cost optimization (Claude is expensive, might want to use GPT-3.5 for simple tasks)
* Vendor flexibility (what if Claude API has outage? Or better models appear?)
* Future-proofing (new LLM providers launching constantly)
* Simplify error handling (unified retry logic)
* Enable A/B testing (compare Claude vs GPT-4 vs Gemini quality)

## Considered Options

### 1. Direct Anthropic API

```python
import anthropic

client = anthropic.Anthropic(api_key=settings.claude_api_key)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Parse this resume..."}]
)
```

**Pros**:
- Simple, direct control
- No extra dependencies
- Full access to Claude-specific features

**Cons**:
- Locked into Anthropic
- Can't switch providers without rewriting all LLM code
- Manual retry logic
- Manual rate limit handling
- No fallback if Claude is down

### 2. LangChain

```python
from langchain.llms import Anthropic

llm = Anthropic(api_key=settings.claude_api_key)
response = llm("Parse this resume...")
```

**Pros**:
- Support for 100+ providers
- Rich ecosystem (agents, chains, memory)
- Active community

**Cons**:
- **Heavy** (200MB+ dependency)
- Over-engineered for our simple use case
- Complex abstractions we don't need
- Slower development (too many options)

### 3. LiteLLM

```python
from litellm import completion

response = completion(
    model="claude-3-5-sonnet-20241022",  # or "gpt-4", "gemini-pro"
    messages=[{"role": "user", "content": "Parse this resume..."}]
)
```

**Pros**:
- **Lightweight** (single package)
- Unified interface for 100+ providers
- Built-in retry logic
- Built-in fallback (try Claude, if fails → try GPT-4)
- Easy provider switching (change one string)
- Active maintenance

**Cons**:
- Adds abstraction layer
- Some provider-specific features unavailable
- Smaller community than LangChain

### 4. Custom Abstraction Layer

```python
class LLMClient:
    def chat(self, messages):
        if self.provider == "claude":
            return self._call_claude(messages)
        elif self.provider == "openai":
            return self._call_openai(messages)
```

**Pros**:
- Full control
- Minimal dependencies
- Custom to our needs

**Cons**:
- **Reinventing the wheel**
- Time cost (2-4 hours to build)
- Maintenance burden (we have to update for new providers)
- Missing features (retries, rate limits)

## Decision Outcome

Chosen option: **LiteLLM**

### Justification

For a hackathon project that might grow:

1. **Cost Optimization**:
   - Use GPT-3.5 for simple parsing: $0.50/1M tokens
   - Use Claude for complex optimization: $3/1M tokens
   - **Savings**: ~60% cost reduction

2. **Provider Switching is Trivial**:
   ```python
   # Before (Claude)
   model="claude-3-5-sonnet-20241022"

   # After (switch to OpenAI)
   model="gpt-4"

   # That's it! No other code changes.
   ```

3. **Fallback Logic Built-in**:
   ```python
   response = completion(
       model="claude-3-5-sonnet-20241022",
       fallbacks=["gpt-4", "gpt-3.5-turbo"]
   )
   # If Claude fails → automatically tries GPT-4 → then GPT-3.5
   ```

4. **A/B Testing Enabled**:
   - Test which model gives best resume parsing
   - Compare quality vs cost
   - Data-driven model selection

### Implementation

```python
# app/core/llm.py
import os
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = settings.claude_api_key

async def get_llm_response(messages: list, model: str = "claude-3-5-sonnet-20241022") -> str:
    """Unified LLM interface - works with any provider"""
    response = completion(
        model=model,
        messages=messages,
        temperature=0.1
    )
    return response.choices[0].message.content
```

To switch providers, just change the model string:
- `"claude-3-5-sonnet-20241022"` → Anthropic Claude
- `"gpt-4"` → OpenAI GPT-4
- `"gemini/gemini-pro"` → Google Gemini
- `"ollama/llama2"` → Local Llama2

### Consequences

**Good**:
- ✅ Can switch models in <5 minutes (just change config)
- ✅ Cost optimization: Use cheap models for simple tasks
- ✅ Fallback prevents downtime (if Claude fails → use GPT-4)
- ✅ Easy A/B testing (compare model quality)

**Bad**:
- ⚠️ Additional dependency (litellm package)
- ⚠️ Abstraction layer adds ~10ms latency
- ⚠️ Can't use Claude-specific features (function calling slightly different)

**Neutral**:
- Error messages are abstracted (less provider-specific detail)
- Need to check LiteLLM docs for provider-specific quirks

## Validation

Success criteria:

✅ **Criterion 1**: Can switch from Claude to OpenAI in <10 lines of code
- Result: Changed in 1 line (model string)

⏳ **Criterion 2**: Cost savings >50% using cheap models for simple tasks
- Result: Not yet measured (need production data)

✅ **Criterion 3**: Fallback prevents downtime during provider outages
- Result: Tested manually, fallback works

✅ **Criterion 4**: No significant latency added (<50ms)
- Result: Measured ~5ms overhead (negligible)

## Related Decisions

* [0001-vertical-slice-architecture.md] - LLM client sits in core/ (shared by all slices)
* [0004-two-stage-resume-parsing.md] - LLM abstraction enables testing different models for parsing

## References

* [LiteLLM Documentation](https://docs.litellm.ai/docs/)
* [Provider Support List](https://docs.litellm.ai/docs/providers)
