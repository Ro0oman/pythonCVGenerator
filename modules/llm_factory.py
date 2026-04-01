import os
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

class LLMProvider:
    """Interface for LLM providers."""
    async def generate(self, system: str, prompt: str) -> tuple:
        pass

class GeminiProvider(LLMProvider):
    def __init__(self, model_name="gemini-flash-latest"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: raise ValueError("GEMINI_API_KEY no encontrada")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate(self, system: str, prompt: str) -> tuple:
        full_p = f"{system}\n\n{prompt}"
        response = await self.model.generate_content_async(full_p)
        usage = getattr(response, 'usage_metadata', None)
        return response.text, usage

class OpenAIProvider(LLMProvider):
    def __init__(self, model_name="gpt-4o"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key: 
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        self.name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate(self, system: str, prompt: str) -> tuple:
        if not self.client:
            raise ValueError("OPENAI_API_KEY no configurada para fallback.")
        response = self.client.chat.completions.create(
            model=self.name,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content, response.usage

class LLMFactory:
    @staticmethod
    def get_provider(provider="gemini", use_fallback=True):
        return LLMFactory(provider, use_fallback)

    def __init__(self, provider="gemini", use_fallback=True):
        self.providers = []
        if provider == "gemini":
            self.providers.append(GeminiProvider())
            if use_fallback: self.providers.append(OpenAIProvider())
        elif provider == "openai":
            self.providers.append(OpenAIProvider())
            if use_fallback: self.providers.append(GeminiProvider())

    async def generate(self, system: str, prompt: str):
        for provider in self.providers:
            try:
                return await provider.generate(system, prompt)
            except Exception as e:
                print(f"[*] Provider {provider.name} failed: {e}. Trying next...")
        raise Exception("All providers failed.")
