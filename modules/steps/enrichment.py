import json
from modules.pipeline import PipelineStep
from modules.github_analyzer import get_recent_github_repos

class EnrichmentStep(PipelineStep):
    """
    Optional enrichment step:
    - Fetches GitHub repositories if github_url exists.
    """
    async def execute(self, state: dict) -> dict:
        person_info = state['person_info']
        github_url = person_info.github_url
        
        if github_url and "github.com" in github_url:
            print(f"[*] Enriqueciendo datos con Repositorios de GitHub: {github_url}")
            github_projects = get_recent_github_repos(github_url)
            return {"github_projects": json.dumps(github_projects)}
        
        return {"github_projects": "[]"}
