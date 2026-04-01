import json
import asyncio
from modules.llm_factory import LLMFactory

class CVOptimizer:
    """
    Core logic for CV and Cover Letter optimization using LLMs.
    """
    
    def __init__(self, provider="gemini"):
        self.llm = LLMFactory(provider)
        
    async def optimize_cv(self, job_description, original_cv, github_projects, portfolio_url):
        """
        Generates a structured JSON with the optimized CV content.
        """
        system_prompt = """
        Eres un Experto en Reclutamiento Tech y Desarrollador Senior. 
        Tu objetivo es reescribir un CV para que supere los filtros ATS con una puntuación >95%.
        Debes usar verbos de acción, métricas cuantificables y asegurar que las Hard Skills aparezcan de forma natural.
        
        IMPORTANTE: Devuelve la respuesta ÚNICAMENTE en formato JSON válido con la siguiente estructura:
        {
            "full_name": "Nombre Completo",
            "contact": {"email": "", "linkedin": "", "github": "", "portfolio": ""},
            "summary": "Resumen profesional de 3-4 líneas altamente optimizado",
            "experience": [
                {"company": "Nombre", "role": "Cargo", "period": "Fechas", "achievements": ["Logro 1 con métricas", "Logro 2"]}
            ],
            "skills": {"hard": ["Skill 1", "Skill 2"], "soft": ["Skill 1", "Skill 2"]},
            "projects": [{"name": "Nombre", "tech_stack": "Tech", "description": "Descripción adaptada de GitHub/Portfolio"}],
            "education": [{"degree": "Grado", "institution": "Univ", "year": "Año"}]
        }
        """
        
        prompt = f"""
        OFERTA DE EMPLEO:
        {job_description}
        
        CV ORIGINAL:
        {original_cv}
        
        PROYECTOS GITHUB:
        {github_projects}
        
        PORTFOLIO: {portfolio_url}
        
        Instrucciones:
        1. Identifica las keywords más críticas de la oferta.
        2. Adapta la experiencia para resaltar esas keywords.
        3. Integra los proyectos de GitHub si son relevantes.
        4. No inventes información, pero optimiza la redacción para que sea impactante.
        """
        
        response = await self.llm.generate_response(prompt, system_prompt)
        
        # Guard against LLM adding extra text
        try:
            # Find the first { and last } to extract JSON
            start = response.find("{")
            end = response.rfind("}") + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except Exception as e:
            print(f"[!] Error al parsear JSON del LLM: {e}")
            return None

    async def generate_cover_letter(self, job_description, cv_data, portfolio_url):
        """
        Generates a 300-word cover letter.
        """
        system_prompt = "Eres un Experto en Reclutamiento Tech que redacta cartas de presentación persuasivas."
        
        prompt = f"""
        Redacta una carta de presentación de 300 palabras para esta oferta:
        {job_description}
        
        Basada en este perfil:
        {json.dumps(cv_data, indent=2)}
        
        Portfolio: {portfolio_url}
        
        REQUISITO: Conecta directamente un proyecto del portfolio o GitHub con el problema principal que la empresa intenta resolver.
        """
        
        return await self.llm.generate_response(prompt, system_prompt)

if __name__ == "__main__":
    # Integration test mock
    pass
