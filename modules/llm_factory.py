import os
import asyncio
from openai import OpenAI
from google import genai
from google.genai import types
import ollama
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

class LLMProvider:
    """Interface for LLM providers."""
    async def generate(self, system: str, prompt: str) -> tuple:
        pass

class GeminiProvider(LLMProvider):
    """
    V6.4: Migrated to the new 'google-genai' SDK (v1.0).
    """
    def __init__(self, model_name="gemini-3.1-flash-lite-preview"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: 
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
        self.name = model_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def generate(self, system: str, prompt: str) -> tuple:
        if not self.client:
            raise ValueError("GEMINI_API_KEY no configurada.")
        
        # New SDK v1.0 async call pattern
        try:
            response = await self.client.aio.models.generate_content(
                model=self.name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system
                )
            )
            # Metadata is in 'usage_metadata'
            return response.text, response.usage_metadata
        except Exception as e:
            if "ResourceExhausted" in str(e) or "429" in str(e):
                print(f"[!] Gemini {self.name} Límite de Cuota superado.")
            raise e

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
            raise ValueError("OPENAI_API_KEY no configurada.")
        
        try:
            # Sync call inside async wrapper for simplicty or use actual async client
            response = self.client.chat.completions.create(
                model=self.name,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content, response.usage
        except Exception as e:
            if "AuthenticationError" in str(e):
                print(f"[!] OpenAI {self.name} Fallo de Autenticación. Revisa tu API KEY.")
            raise e

class OllamaProvider(LLMProvider):
    def __init__(self, model_name="llama3:8b"):
        self.name = model_name

    async def generate(self, system: str, prompt: str) -> tuple:
        try:
            response = ollama.chat(
                model=self.name,
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': prompt},
                ]
            )
            # Ollama doesn't return usage exactly like cloud but we can mock it
            # or extract from response['prompt_eval_count']
            usage = {
                "prompt_token_count": response.get('prompt_eval_count', 0),
                "candidates_token_count": response.get('eval_count', 0)
            }
            return response['message']['content'], usage
        except Exception as e:
            print(f"[!] Ollama {self.name} Error: {e}. ¿Está Ollama ejecutándose?")
            raise e

class LLMFactory:
    @staticmethod
    def get_provider(provider="gemini", model_name=None, use_fallback=True):
        return LLMFactory(provider, model_name, use_fallback)

    @staticmethod
    def check_and_pull_model(model_name="llama3.1:8b"):
        """Checks if a model exists in Ollama and pulls it if not."""
        print(f"[*] Verificando IA Local ({model_name})...")
        try:
            # SDK v0.4+ uses .models and m.model
            # SDK < v0.4 uses ['models'] and m['name']
            resp = ollama.list()
            models_list = []
            if hasattr(resp, 'models'):
                models_list = [m.model for m in resp.models]
            elif isinstance(resp, dict) and 'models' in resp:
                models_list = [m.get('name') or m.get('model') for m in resp['models']]

            if model_name not in models_list and f"{model_name}:latest" not in models_list:
                print(f"[!] El modelo {model_name} NO está instalado.")
                print(f"[*] Iniciando descarga de {model_name} (~4.7GB). Por favor, espera...")
                # The pull status also changed in some SDK versions, let's be safe
                for progress in ollama.pull(model_name, stream=True):
                    status = progress.get('status', '')
                    if status == 'downloading':
                        # Use get with default to avoid KeyErrors
                        completed = progress.get('completed', 0)
                        total = progress.get('total', 0)
                        if total > 0:
                            print(f"   ⏳ Descarga: {completed/1e9:.2f}GB / {total/1e9:.2f}GB", end='\r')
                print(f"\n✅ Modelo {model_name} descargado y listo.")
            else:
                print(f"✅ IA Local {model_name} lista.")
        except Exception as e:
            print(f"[!] No se pudo conectar con Ollama o procesar la descarga: {e}")
            print("👉 Asegúrate de que Ollama está instalado y abierto (https://ollama.com/)")

    def __init__(self, provider="gemini", model_name=None, use_fallback=True):
        self.providers = []
        if provider == "ollama":
            self.providers.append(OllamaProvider(model_name or "llama3:8b"))
            if use_fallback: self.providers.append(GeminiProvider())
        elif provider == "gemini":
            self.providers.append(GeminiProvider(model_name or "gemini-3.1-flash-lite-preview"))
            if use_fallback: self.providers.append(OpenAIProvider())
        elif provider == "openai":
            self.providers.append(OpenAIProvider(model_name or "gpt-4o"))
            if use_fallback: self.providers.append(GeminiProvider())

    async def generate(self, system: str, prompt: str):
        for provider in self.providers:
            try:
                return await provider.generate(system, prompt)
            except Exception as e:
                print(f"[*] Provider {provider.name} failed: {e}. Trying next...")
        raise Exception("All providers failed. Revisa tus límites, claves de API u Ollama.")

if __name__ == "__main__":
    async def test():
        try:
            factory = LLMFactory("gemini")
            print("[*] LLM Factory Inicializada (V6.5 Híbrida).")
        except Exception as e:
            print(f"[!] Error: {e}")
    asyncio.run(test())
