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
        Generates a structured JSON with the optimized CV content (V4: No Hallucinations).
        """
        system_prompt = f"""
        Eres un Experto en Reclutamiento Tech con una política de "CERO ALUCINACIONES". 
        Tu objetivo es transformar el CV para que el candidato sea el ANALISTA PROGRAMADOR FULLSTACK PHP/LARAVEL + VUE ideal, pero basándote ÚNICAMENTE en datos reales proporcionados.
        
        REGLAS CRÍTICAS (NIVEL TOP):
        1. NO INVENTES PROYECTOS: Usa exclusivamente los repositorios listados en el input de GitHub. Si un proyecto no está ahí, NO lo menciones.
        2. Email: DEBE ser "romainot99@gmail.com".
        3. Educación: Para cada curso/grado, describe brevemente qué se hizo/aprendió y añade una lista de 'hard_skills' específicas obtenidas.
        4. Resumen: "Fullstack Developer con +3 años de experiencia en desarrollo web con PHP (Laravel) y Vue.js, especializado en aplicaciones escalables y APIs REST. Experiencia adicional en Python para automatización."
        5. Experiencia: Prioriza PHP/Laravel/Vue y evidencias de Scrum/Teamwork (con Code Reviews) basándote en su historial real de TESI e Infoverity.
        6. Proyectos Reales: Describe los repos descriptos en el input de forma que resalten las tecnologías demandadas (PHP/Laravel/Vue/Python).
        
        IMPORTANTE: Devuelve la respuesta ÚNICAMENTE en formato JSON válido:
        {{
            "full_name": "Nombre Completo",
            "contact": {{"email": "romainot99@gmail.com", "linkedin": "", "github": "", "portfolio": ""}},
            "summary": "Resumen profesional nivel top enfocado en Fullstack PHP/Laravel + Vue.js",
            "experience": [
                {{"company": "Nombre", "role": "Analista Programador Fullstack", "period": "Fechas", "achievements": ["Logros con keywords PHP/Laravel/Vue/Scrum", "Evidencia de análisis y diseño"]}}
            ],
            "skills": {{"hard": ["PHP (Laravel)", "Vue.js", "MySQL", "APIs REST", "Docker", "Python"], "soft": ["Trabajo en Equipo (Scrum & Code Reviews)", "Análisis Técnico"]}},
            "projects": [{{
                "name": "Nombre del repo real", 
                "tech_stack": "Stack real", 
                "url": "URL real de GitHub", 
                "description": "Descripción adaptada a la oferta basada en el README real"
            }}],
            "education": [{{
                "degree": "Grado", 
                "institution": "Univ", 
                "year": "Año", 
                "description": "Qué se hizo en el curso",
                "hard_skills": ["Skill 1", "Skill 2"]
            }}]
        }}
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
