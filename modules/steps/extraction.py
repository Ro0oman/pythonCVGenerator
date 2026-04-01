import json
import re
from modules.pipeline import PipelineStep
from modules.llm_factory import LLMFactory
from modules.models import PersonInfo
from modules.cost_controller import CostController

class DataExtractionStep(PipelineStep):
    """
    Extracts personal info and professional URLs from the original CV.
    Falls back to data.json if not found.
    """
    def __init__(self, provider="gemini", model_name=None):
        self.provider = provider
        self.model_name = model_name
        self.cost_controller = CostController()

    async def execute(self, state: dict) -> dict:
        llm = LLMFactory.get_provider(self.provider, model_name=self.model_name)
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
        
        response_text, _ = await llm.generate(system_prompt, f"CV TEXT:\n{original_cv}")
        
        try:
            # More robust JSON extraction using regex
            match = re.search(r'(\{.*\})', response_text, re.DOTALL)
            if match:
                clean_json = match.group(1).strip()
                extracted_data = json.loads(clean_json)
            else:
                raise ValueError("No se encontró un objeto JSON en la respuesta.")
        except Exception as e:
            print(f"[!] Error al parsear JSON del CV: {e}")
            print(f"[*] Respuesta raw: {response_text[:100]}...")
            extracted_data = {}

        # Merge with data.json (Fallback and Identity Guard)
        extracted_name = extracted_data.get("full_name", "").strip()
        # Identity Guard: Clean spaced letters if LLM was "too creative" (R O M A N -> ROMAN)
        if re.search(r'([A-Z] ){3,}', extracted_name):
            extracted_name = extracted_name.replace(" ", "")
        
        # Priority: Config (User explicit) > Extracted (if not placeholder) > Default
        final_name = config.get("full_name") or (extracted_name if (extracted_name and "Candidato" not in extracted_name) else "Roman Myziuk")

        merged_info = {
            "full_name": final_name,
            "email": extracted_data.get("email") or config.get("email", "romainot99@gmail.com"),
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
