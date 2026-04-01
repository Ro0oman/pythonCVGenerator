import json
import asyncio
import os
from modules.llm_factory import LLMFactory
from modules.models import CVData

class CVOptimizer:
    """
    Core logic for CV and Cover Letter optimization using LLMs.
    """
    
    def __init__(self, provider="gemini"):
        self.llm = LLMFactory.get_provider(provider)
        self.prompts_dir = "prompts"

    def _load_prompt(self, filename):
        path = os.path.join(self.prompts_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    async def optimize_cv(self, job_description, original_cv, github_projects, portfolio_url):
        """
        Generates a structured JSON with the optimized CV content (V5: Senior Architect).
        Validated via Pydantic and external prompts.
        """
        system_prompt = self._load_prompt("cv_system_prompt.md")
        
        prompt = f"""
        OFERTA DE EMPLEO:
        {job_description}
        
        CV ORIGINAL:
        {original_cv}
        
        PROYECTOS GITHUB (ÚNICOS PERMITIDOS):
        {github_projects}
        
        PORTFOLIO:
        {portfolio_url}
        """
        
        response_text = await self.llm.generate(system_prompt, prompt)
        
        try:
            # Clean possible markdown formatting from LLM
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(clean_json)
            
            # Pydantic Validation
            validated_data = CVData(**data_dict)
            return validated_data.dict()
            
        except Exception as e:
            print(f"[!] Error de validación Pydantic o JSON: {e}")
            print(f"[DEBUG] Raw Response: {response_text[:500]}...")
            return None

    async def generate_cover_letter(self, job_description, cv_data, portfolio_url):
        """
        Generates a cover letter based on the optimized CV and Job offer.
        """
        system_prompt = """
        Eres un Experto en Reclutamiento Tech. Escribe una carta de presentación persuasiva, 
        concisa (máximo 300 palabras) y profesional.
        Enfócate en cómo el stack de PHP/Laravel y Vue del candidato encaja con la oferta.
        Menciona los proyectos de GitHub como evidencia real de habilidades.
        Evita clichés y sé directo.
        """
        
        prompt = f"""
        OFERTA: {job_description}
        DATOS OPTIMIZADOS: {json.dumps(cv_data)}
        PORTFOLIO: {portfolio_url}
        """
        
        return await self.llm.generate(system_prompt, prompt)

if __name__ == "__main__":
    # Integration test mock
    pass
