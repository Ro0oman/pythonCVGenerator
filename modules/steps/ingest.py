import json
import os
from modules.pipeline import PipelineStep
from modules.scraper import scrape_job_offer
from modules.github_analyzer import get_recent_github_repos
from modules.pdf_parser import parse_cv

class IngestStep(PipelineStep):
    """
    Handles all data ingestion:
    - Scrapes Job Offer (with cache).
    - Fetches GitHub repositories.
    - Parses the original CV/TXT.
    """
    async def execute(self, state: dict) -> dict:
        config = state['config']
        
        # 1. Scraping Job Offer
        job_url = state.get('current_job_url') or config.get('job_url')
        if not job_url:
            raise Exception("No se proporcionó 'job_url' o 'job_urls' en data.json")
            
        print(f"[*] Escaneando oferta: {job_url}")
        job_info = await scrape_job_offer(job_url)
        if not job_info:
            raise Exception(f"No se pudo obtener la información de: {job_url}")
            
        # 2. Reading Original CV
        cv_path = "cv_original.pdf" if os.path.exists("cv_original.pdf") else "cv_original.txt"
        if not os.path.exists(cv_path):
            with open("cv_original.txt", "w") as f: f.write("CV Base.")
            cv_path = "cv_original.txt"
            
        original_cv = parse_cv(cv_path)
        
        return {
            "job_info": job_info,
            "original_cv": original_cv
        }
