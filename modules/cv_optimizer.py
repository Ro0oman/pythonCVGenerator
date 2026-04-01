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
        Strategically repositioned for Fullstack PHP/Laravel roles.
        """
        system_prompt = """
        Eres un Experto en Reclutamiento Tech con visión de "Stack Pivoting". 
        Tu objetivo es transformar un CV de perfil mixto para que sea EL CANDIDATO IDEAL para una posición de FULLSTACK PHP/LARAVEL + VUE.
        
        ESTRATEGIA DE POSICIONAMIENTO (CRÍTICO):
        1. Resumen Profesional: Debe gritar "Fullstack Developer orientado a PHP/Laravel". Usa Python e IA solo como un "plus estratégico" o "automatización de procesos", NUNCA como el stack principal si la oferta pide PHP.
        2. Experiencia (TESI, Infoverity, etc.): 
           - Debes dar protagonismo a Laravel, PHP y arquitectura MVC.
           - Inserta evidencias de "Trabajo en equipo" y "Entorno Scrum" (Sprints, Dailies) como logros reales.
           - Usa verbos de acción (Desarrollé, Implementé, Optimicé) y métricas (€, %, ms).
        3. Honradez: Respeta las fechas originales pero optimiza la narrativa de las tareas para que encajen en el rol stack-demandado.
        4. Keywords: Prioriza Laravel, Vue.js, PHP, APIs REST, SQL y Scrum.
        
        IMPORTANTE: Devuelve la respuesta ÚNICAMENTE en formato JSON válido con la siguiente estructura:
        {
            "full_name": "Nombre Completo",
            "contact": {"email": "", "linkedin": "", "github": "", "portfolio": ""},
            "summary": "Resumen profesional empezando por Fullstack PHP/Laravel + Vue.js (+3 años si es posible narrativamente sin mentir)",
            "experience": [
                {"company": "Nombre", "role": "Cargo adaptado a Fullstack/Programador", "period": "Fechas", "achievements": ["Logro con Laravel/Vue/Teamwork", "Métrica lograda"]}
            ],
            "skills": {"hard": ["Laravel", "PHP", "Vue.js", "MySQL", "Git", "Python (Automation)"], "soft": ["Trabajo en Equipo", "Scrum / Agile", "Resolución de Problemas"]},
            "projects": [{"name": "Nombre", "tech_stack": "Stack", "description": "Descripción orientada a la oferta"}],
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
