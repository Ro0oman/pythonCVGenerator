import asyncio
import json
import os
from dotenv import load_dotenv

from modules.pipeline import JobPipeline
from modules.steps.ingest import IngestStep
from modules.steps.extraction import DataExtractionStep
from modules.steps.enrichment import EnrichmentStep
from modules.steps.optimization import CVOptimizationStep
from modules.steps.letter_generation import LetterGenerationStep
from modules.steps.render import RenderStep
from modules.steps.reporting import CostReportingStep

load_dotenv()

async def main():
    print("🚀 ATS-Master CV Generator Pro (V6: Production Architecture)")
    
    # 1. Load Initial Config
    if not os.path.exists('data.json'):
        print("[!] Error: No se encuentra data.json")
        return
        
    with open('data.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 2. Define Pipeline
    # Using 'v1' for prompt versioning by default
    pipeline = JobPipeline([
        IngestStep(),
        DataExtractionStep(provider=config.get('llm_provider', 'gemini')),
        EnrichmentStep(),
        CVOptimizationStep(provider=config.get('llm_provider', 'gemini'), prompt_version="v1"),
        LetterGenerationStep(provider=config.get('llm_provider', 'gemini')),
        RenderStep(),
        CostReportingStep()
    ])

    # 3. Run Pipeline
    try:
        final_state = await pipeline.run(initial_state={"config": config})
        
        # 4. Final Success Summary
        print(f"\n✅ Proceso completado con éxito.")
        print(f"📂 Carpeta de salida: {final_state.get('output_folder')}")
        print(f"📄 CV: {final_state.get('cv_pdf_path')}")
        if final_state.get('letter_pdf_path'):
            print(f"📄 Carta: {final_state.get('letter_pdf_path')}")
            
    except Exception as e:
        print(f"\n❌ El Pipeline ha fallado: {e}")

if __name__ == "__main__":
    asyncio.run(main())
