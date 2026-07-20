"""
Model client wrappers. Each function takes a prompt string and returns
the model's text response. Add new models by adding a new function and
registering it in MODEL_REGISTRY.
"""

import os


def call_claude(prompt: str, model: str = "claude-sonnet-4-6") -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def call_gpt(prompt: str, model: str = "gpt-4o") -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_gemini(prompt: str, model: str = "gemini-3.1-flash-lite") -> str:
    from google import genai

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text


def call_atlas_chat(prompt: str, model: str = "MBZUAI-Paris/Atlas-Chat-9B") -> str:
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=os.environ["HF_TOKEN"], provider="auto")
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content


MODEL_REGISTRY = {
    "claude": call_claude,
    "gpt4o": call_gpt,
    "gemini": call_gemini,
    "atlas-chat": call_atlas_chat,
}
