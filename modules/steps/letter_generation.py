import json
import re
from modules.pipeline import PipelineStep
from modules.cv_optimizer import CVOptimizer
from modules.cost_controller import CostController

class LetterGenerationStep(PipelineStep):
    def __init__(self, provider="gemini", model_name=None):
        self.provider = provider
        self.model_name = model_name
        self.cost_controller = CostController()

    async def execute(self, state: dict) -> dict:
        if not state['config'].get('generate_cover_letter', True):
            return {}

        print("[*] Generando Carta de Presentación...")
        optimizer = CVOptimizer(provider=self.provider, model_name=self.model_name)
        
        try:
            content, usage = await optimizer.generate_cover_letter_raw(
                job_description=state['job_info']['content'],
                original_cv=state['original_cv']
            )
            
            # Use regex for robust extraction
            match = re.search(r'(\{.*\})', content, re.DOTALL)
            if match:
                clean_json = match.group(1).strip()
                data_dict = json.loads(clean_json)
                return {"letter_data": data_dict}
            else:
                return {"letter_data": {"content": content}} # Fallback to raw text
        except Exception as e:
            print(f"[!] Error en LetterGenerationStep: {e}")
            return {}
