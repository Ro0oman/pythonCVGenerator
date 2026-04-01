import json
from modules.pipeline import PipelineStep
from modules.cv_optimizer import CVOptimizer
from modules.cost_controller import CostController

class LetterGenerationStep(PipelineStep):
    def __init__(self, provider="gemini"):
        self.provider = provider
        self.cost_controller = CostController()

    async def execute(self, state: dict) -> dict:
        config = state['config']
        if not config.get('generate_cover_letter'):
            return {}

        print("[*] Generando Carta de Presentación...")
        optimizer = CVOptimizer(provider=self.provider)
        
        content, usage = await optimizer.generate_cover_letter(
            job_description=state['job_info']['content'],
            cv_data=state['optimized_data'],
            portfolio_url=config['portfolio_url']
        )
        
        # Track cost
        if usage:
            t_in = getattr(usage, 'prompt_token_count', 0)
            t_out = getattr(usage, 'candidates_token_count', 0)
            self.cost_controller.track_request(self.provider, t_in, t_out)

        return {"letter_content": content}
