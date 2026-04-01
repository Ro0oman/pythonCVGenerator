import json
import re
from modules.pipeline import PipelineStep
from modules.llm_factory import LLMFactory
from modules.models import PersonInfo

class DataExtractionStep(PipelineStep):
    """
    Extracts personal info and professional URLs from the original CV.
    Falls back to data.json if not found.
    """
    def __init__(self, provider="gemini"):
        self.llm = LLMFactory.get_provider(provider)

    async def execute(self, state: dict) -> dict:
        original_cv = state['original_cv']
        config = state['config']
        
        print("[*] Escaneando CV para extraer identidad y perfiles...")
        
        system_prompt = """
        Eres un extractor de datos profesional. Del siguiente texto de un CV, extrae:
        - Nombre completo
        - Email
        - GitHub URL
        - LinkedIn URL
        - Portfolio URL
        - Stack tecnológico principal (ej. "Fullstack PHP", "Backend Python", "C# Developer")
        
        Devuelve ÚNICAMENTE un JSON válido con esta estructura:
        {
            "full_name": "",
            "email": "",
            "github_url": "",
            "linkedin_url": "",
            "portfolio_url": "",
            "target_stack_detected": ""
        }
        """
        
        response_text, _ = await self.llm.generate(system_prompt, f"CV TEXT:\n{original_cv}")
        
        try:
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            extracted_data = json.loads(clean_json)
        except Exception as e:
            print(f"[!] Error al extraer datos del CV: {e}. Usando datos de respaldo.")
            extracted_data = {}

        # Merge with data.json (Fallback)
        merged_info = {
            "full_name": extracted_data.get("full_name") or config.get("full_name", "Candidato"),
            "email": extracted_data.get("email") or config.get("email", "info@example.com"),
            "github_url": extracted_data.get("github_url") or config.get("github_url"),
            "linkedin_url": extracted_data.get("linkedin_url") or config.get("linkedin_url"),
            "portfolio_url": extracted_data.get("portfolio_url") or config.get("portfolio_url"),
            "target_stack_detected": extracted_data.get("target_stack_detected") or "Software Developer"
        }

        # Check for missing GitHub
        github_missing = not merged_info.get("github_url")
        
        return {
            "person_info": PersonInfo(**merged_info),
            "github_missing": github_missing
        }
