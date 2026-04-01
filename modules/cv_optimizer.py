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
        Strategically repositioned for Fullstack PHP/Laravel roles (Nivel Top).
        """
        system_prompt = """
        Eres un Experto en Reclutamiento Tech con visión estratégica "Nivel Top". 
        Tu objetivo es transformar el CV para que el candidato parezca un ANALISTA PROGRAMADOR FULLSTACK PHP/LARAVEL nativo.
        
        REGLAS CRÍTICAS DE REPOSICIONAMIENTO:
        1. Corrección de Datos: El email DEBE ser "romainot99@gmail.com" (corrige cualquier error de "gmai.com").
        2. Resumen: "Fullstack Developer con +3 años de experiencia en desarrollo web con PHP (Laravel) y Vue.js, especializado en aplicaciones escalables y APIs REST. Experiencia adicional en Python para automatización."
        3. Experiencia (TESI): Usa el bullet: "Desarrollo Fullstack con PHP (Laravel) y Vue.js en una plataforma de alto tráfico (+1M usuarios)". Añade análisis de requisitos y diseño de soluciones.
        4. Experiencia (Infoverity): Enfoca el backend como "Diseño de APIs REST consumidas por aplicaciones frontend, facilitando la integración Fullstack".
        5. Persona Analista: Inyecta bullets sobre "Diseño de arquitectura escalable" y "Análisis técnico de requisitos".
        6. Proyectos: El proyecto PHP/Laravel debe destacar "Implementación de Autenticación, CRUDs avanzados y Gestión de Usuarios".
        7. Soft Skills: Añade "Code Reviews" y "Mejores prácticas" dentro del entorno Scrum.
        
        IMPORTANTE: Devuelve la respuesta ÚNICAMENTE en formato JSON válido con la siguiente estructura:
        {
            "full_name": "Nombre Completo",
            "contact": {"email": "romainot99@gmail.com", "linkedin": "", "github": "", "portfolio": ""},
            "summary": "Resumen profesional nivel top enfocado en Fullstack PHP/Laravel + Vue.js",
            "experience": [
                {"company": "Nombre", "role": "Analista Programador Fullstack", "period": "Fechas", "achievements": ["Logros con keywords PHP/Laravel/Vue/Scrum", "Evidencia de análisis y diseño"]}
            ],
            "skills": {"hard": ["PHP (Laravel)", "Vue.js", "MySQL", "APIs REST", "Docker", "Python (Optimization)"], "soft": ["Trabajo en Equipo (Scrum & Code Reviews)", "Análisis Técnico", "Resolución de Problemas"]},
            "projects": [{"name": "Nombre", "tech_stack": "Stack", "url": "URL", "description": "Descripción funcional/empresarial activa"}],
            "education": [{"degree": "Grado", "institution": "Univ", "year": "Año", "description": "Lo aprendido enfocado al rol"}]
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
