import json
import os
from modules.pipeline import PipelineStep
from modules.cv_optimizer import CVOptimizer
from modules.cost_controller import CostController
from modules.models import CVData
from pydantic import ValidationError

class CVOptimizationStep(PipelineStep):
    def __init__(self, provider="gemini", prompt_version="v1"):
        self.provider = provider
        self.prompt_version = prompt_version
        self.cost_controller = CostController()

    async def execute(self, state: dict) -> dict:
        optimizer = CVOptimizer(provider=self.provider)
        optimizer.prompts_dir = os.path.join("prompts", self.prompt_version)
        
        person_info = state['person_info']
        job_info = state['job_info']
        original_cv = state['original_cv']
        github_projects = state.get('github_projects', "[]")
        portfolio_url = person_info.portfolio_url or state['config'].get('portfolio_url', "")

        # 1. Load and Replace Placeholders in System Prompt
        sys_prompt = optimizer._load_prompt("cv_system_prompt.md")
        replacements = {
            "{{FULL_NAME}}": person_info.full_name,
            "{{EMAIL}}": person_info.email,
            "{{GITHUB}}": person_info.github_url or "NO GitHub URL provided",
            "{{LINKEDIN}}": person_info.linkedin_url or "NO LinkedIn URL provided",
            "{{PORTFOLIO}}": person_info.portfolio_url or "NO Portfolio URL provided",
            "{{TARGET_STACK_DETECTED}}": person_info.target_stack_detected
        }
        for key, val in replacements.items():
            sys_prompt = sys_prompt.replace(key, str(val))

        print(f"[*] Optimizando CV para: {person_info.full_name}...")
        
        # 2. Execution Logic (with possible retry)
        result = await self._try_optimize(optimizer, sys_prompt, job_info, original_cv, github_projects, portfolio_url)
        
        if not result['success']:
            print(f"[!] Error de validación Pydantic. Reintentando...")
            error_msg = f"Tu respuesta anterior falló la validación: {result['error']}. Asegúrate de usar JSON puro."
            result = await self._try_optimize(optimizer, sys_prompt + f"\n\nERROR_CONTEXT: {error_msg}", job_info, original_cv, github_projects, portfolio_url)

        if not result['success']:
             raise Exception(f"Fallo crítico en optimización: {result['error']}")

        # 3. Cost Tracking
        if result['usage']:
            t_in = getattr(result['usage'], 'prompt_token_count', 0)
            t_out = getattr(result['usage'], 'candidates_token_count', 0)
            self.cost_controller.track_request(self.provider, t_in, t_out)

        return {"optimized_data": result['data']}

    async def _try_optimize(self, optimizer, sys_prompt, job_info, original_cv, github_projects, portfolio_url):
        try:
            # We bypass the standard optimize_cv if we want to pass the substituted sys_prompt directly
            # For simplicity, we just inject it into the prompt or modify optimizer to accept it
            # Let's adjust CVOptimizer to accept a custom sys_prompt
            prompt = f"OFERTA: {job_info['content']}\n\nORIGINAL: {original_cv}\n\nGITHUB: {github_projects}\n\nPORTFOLIO: {portfolio_url}"
            response_text, usage = await optimizer.llm.generate(sys_prompt, prompt)
            
            clean_json = response_text.replace("```json", "").replace("```", "").strip()
            data_dict = json.loads(clean_json)
            validated_data = CVData(**data_dict)
            return {"success": True, "data": validated_data.dict(), "usage": usage}
        except Exception as e:
            return {"success": False, "error": str(e), "usage": None}
