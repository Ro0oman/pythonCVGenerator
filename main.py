import asyncio
import json
import os
import argparse
from datetime import datetime
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
    parser = argparse.ArgumentParser(description="ATS-Master CV Generator Pro (V7.0)")
    parser.add_argument("--mode", choices=["full", "render"], default="full", help="Modo: 'full' (todo) o 'render' (solo generar PDF desde JSON)")
    parser.add_argument("--data", type=str, help="Ruta al JSON de datos optimizados (solo para modo render)")
    args = parser.parse_args()

    # 1. Load Initial Config
    if not os.path.exists('data.json'):
        print("[!] Error: No se encuentra data.json")
        return
        
    with open('data.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    print(f"🚀 ATS-Master CV Generator Pro (V7.0: Retouching Mode - {args.mode.upper()})")
    
    if args.mode == "full":
        # 1. Configuration and Auto-Setup (V6.5)
        provider = config.get('llm_provider', 'gemini')
        model_name = config.get('model_name')

        if provider == "ollama":
            target_model = model_name or "llama3:8b"
            print(f"🏠 MODO LOCAL ACTIVADO: Usando {target_model}")
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
        
        final_state = await pipeline.run(initial_state={"config": config})
        
        # PERSISTENCIA PARA RETOQUES (V7.0)
        # Guardamos el JSON de los datos optimizados para que el usuario pueda retocarlo
        retouch_data = {
            "optimized_data": final_state.get('optimized_data'),
            "letter_data": final_state.get('letter_data'),
            "config": config,
            "job_info": final_state.get('job_info')
        }
        
        # Guardamos uno fijo para "retoque rápido" y uno histórico
        output_dir = final_state.get('output_folder', 'output')
        retouch_path = os.path.join(output_dir, "resume_to_retouch.json")
        last_retouch_path = os.path.join("output", "last_cv_data.json")
        
        with open(retouch_path, 'w', encoding='utf-8') as f:
            json.dump(retouch_data, f, indent=4, ensure_ascii=False)
        with open(last_retouch_path, 'w', encoding='utf-8') as f:
            json.dump(retouch_data, f, indent=4, ensure_ascii=False)
            
        print(f"✍️  Archivo de retoque guardado: {retouch_path}")
        print(f"💡 Puedes editarlo y ejecutar: python main.py --mode render --data {retouch_path}")

    else:
        # MODO RENDER (Carga desde JSON)
        json_path = args.data or os.path.join("output", "last_cv_data.json")
        if not os.path.exists(json_path):
            print(f"[!] Error: No se encuentra el archivo de datos: {json_path}")
            return
            
        print(f"🎨 Cargando datos de retoque desde: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            retouch_data = json.load(f)
            
        pipeline = JobPipeline([
            RenderStep(),
            CostReportingStep()
        ])
        
        # Restauramos el estado desde el JSON
        final_state = await pipeline.run(initial_state=retouch_data)

    # Final Success Summary
    print(f"\n✅ Proceso completado con éxito.")
    print(f"📂 Carpeta de salida: {final_state.get('output_folder')}")
    print(f"📄 CV: {final_state.get('cv_pdf_path')}")
    if final_state.get('letter_pdf_path'):
        print(f"📄 Carta: {final_state.get('letter_pdf_path')}")

if __name__ == "__main__":
    asyncio.run(main())


# 1. Cargar Configuración
# 2. Ingesta (PDF + GitHub)
# 3. Extracción (Identidad + Perfiles)
# 4. Enriquecimiento (Datos de GitHub)
# 5. Optimización (CV + Carta)
# 6. Renderizado (PDFs)
# 7. Reporte (Costes + Recomendaciones)
