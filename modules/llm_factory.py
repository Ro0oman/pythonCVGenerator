import os
import google.generativeai as genai
from openai import OpenAI
import anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMFactory:
    """
    Factory for handling multiple LLM providers: Gemini, OpenAI, Anthropic.
    Ensures a consistent interface for the application.
    """
    
    @staticmethod
    def get_provider(provider="gemini"):
        return LLMFactory(provider)

    def __init__(self, provider="gemini"):
        self.provider = provider.lower()
        self.model = None
        
        if self.provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key: raise ValueError("GEMINI_API_KEY no encontrada")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
            
        elif self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key: raise ValueError("OPENAI_API_KEY no encontrada")
            self.client = OpenAI(api_key=api_key)
            
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key: raise ValueError("ANTHROPIC_API_KEY no encontrada")
            self.client = anthropic.Anthropic(api_key=api_key)
            
    async def generate(self, system_instruction: str, prompt: str):
        """
        Sends a prompt to the selected LLM and returns the response.
        """
        if self.provider == "gemini":
            # Gemini handles system instructions in the model config or combined
            full_prompt = f"{system_instruction}\n\n{prompt}"
            response = await self.model.generate_content_async(full_prompt)
            return response.text
            
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=2048,
                system=system_instruction,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
            
        return ""

if __name__ == "__main__":
    # Mock test (requires API keys)
    import asyncio
    try:
        factory = LLMFactory("gemini")
        print("[*] LLM Factory Inicializada.")
    except Exception as e:
        print(f"[!] Error: {e}")
