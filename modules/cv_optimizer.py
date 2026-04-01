import json
import asyncio
import os
from modules.llm_factory import LLMFactory
from modules.models import CVData

class CVOptimizer:
    """
    Core logic for CV and Cover Letter optimization using LLMs.
    """
    
    def __init__(self, provider="gemini", model_name=None):
        self.llm = LLMFactory.get_provider(provider, model_name=model_name)
        self.prompts_dir = "prompts/v1"

    def _load_prompt(self, filename):
        path = os.path.join(self.prompts_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    async def optimize_cv(self, job_description, original_cv, github_projects, portfolio_url, error_context=""):
        """
        Generates a structured JSON with the optimized CV content (V6: Senior Production).
        """
        system_prompt = self._load_prompt("cv_system_prompt.md")
        if error_context:
            system_prompt += f"\n\nATENCIÓN: Tu intento anterior falló con este error: {error_context}. Por favor, corrígelo."

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
        
        response_text, usage = await self.llm.generate(system_prompt, prompt)
        
        try:
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(clean_json)
            validated_data = CVData(**data_dict)
            return validated_data.dict(), usage
        except Exception as e:
            raise e

    async def generate_cover_letter_raw(self, job_description: str, original_cv: str) -> tuple:
        sys_prompt = self._load_prompt("letter_system_prompt.md")
        prompt = f"OFERTA: {job_description}\n\nCV ORIGINAL: {original_cv}"
        return await self.llm.generate(sys_prompt, prompt)

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
