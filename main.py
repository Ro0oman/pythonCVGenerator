import asyncio
import json
import os
from dotenv import load_dotenv

from modules.llm_factory import LLMFactory
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
    # 1. Configuration and Auto-Setup (V6.5)
    provider = config.get('llm_provider', 'gemini')
    model_name = config.get('model_name')

    print("🚀 ATS-Master CV Generator Pro (V6.5: Hybrid Architecture)")
    
    if provider == "ollama":
        target_model = model_name or "llama3:8b"
        print(f"🏠 MODO LOCAL ACTIVADO: Usando {target_model}")
        print("⚠️  AVISO: Se recomiendan 6GB de RAM/VRAM para un rendimiento óptimo.")
        LLMFactory.check_and_pull_model(target_model)
    
    pipeline = JobPipeline([
        IngestStep(),
        DataExtractionStep(provider=provider, model_name=model_name),
        EnrichmentStep(),
        CVOptimizationStep(provider=provider, model_name=model_name, prompt_version="v1"),
        LetterGenerationStep(provider=provider, model_name=model_name),
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


# 1. Cargar Configuración
# 2. Ingesta (PDF + GitHub)
# 3. Extracción (Identidad + Perfiles)
# 4. Enriquecimiento (Datos de GitHub)
# 5. Optimización (CV + Carta)
# 6. Renderizado (PDFs)
# 7. Reporte (Costes + Recomendaciones)
