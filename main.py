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

    print(f"🚀 ATS-Master CV Generator Pro (V7.0: Multiple CV Mode - {args.mode.upper()})")
    
    if args.mode == "full":
        # Handle multiple URLs
        job_urls = config.get('job_urls', [])
        if not job_urls and config.get('job_url'):
            job_urls = [config.get('job_url')]
        
        if not job_urls:
            print("[!] Advertencia: No se encontraron URLs de ofertas en data.json")
            return

        print(f"📋 Se han detectado {len(job_urls)} ofertas para procesar.")
        
        all_results = []
        
        for index, url in enumerate(job_urls, 1):
            print(f"\n--- 🔄 PROCESANDO OFERTA {index}/{len(job_urls)} ---")
            print(f"🔗 URL: {url}")
            
            try:
                provider = config.get('llm_provider', 'gemini')
                model_name = config.get('model_name')

                if provider == "ollama":
                    target_model = model_name or "llama3.2"
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
                
                # Ejecutar pipeline con la URL actual en el estado
                final_state = await pipeline.run(initial_state={"config": config, "current_job_url": url})
                
                # PERSISTENCIA PARA RETOQUES (V7.0)
                retouch_data = {
                    "optimized_data": final_state.get('optimized_data'),
                    "letter_data": final_state.get('letter_data'),
                    "config": config,
                    "job_info": final_state.get('job_info')
                }
                
                output_dir = final_state.get('output_folder', 'output')
                retouch_path = os.path.join(output_dir, "resume_to_retouch.json")
                
                with open(retouch_path, 'w', encoding='utf-8') as f:
                    json.dump(retouch_data, f, indent=4, ensure_ascii=False)
                
                all_results.append({
                    "url": url,
                    "cv": final_state.get('cv_pdf_path'),
                    "letter": final_state.get('letter_pdf_path'),
                    "folder": output_dir
                })
                
            except Exception as e:
                print(f"[❌] Error procesando la oferta {index}: {e}")
                continue

        # Resumen Final
        print(f"\n" + "="*50)
        print(f"🏁 RESUMEN DE GENERACIÓN ({len(all_results)}/{len(job_urls)} completados)")
        print("="*50)
        for res in all_results:
            print(f"✅ EXITO: {res['url']}")
            print(f"   📂 Carpeta: {res['folder']}")
            print(f"   📄 CV: {res['cv']}")
            if res['letter']:
                print(f"   📄 Carta: {res['letter']}")
            print("-" * 30)

    else:
        # MODO RENDER (Carga desde JSON - Mantenemos compatibilidad básica para un solo archivo)
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
        
        final_state = await pipeline.run(initial_state=retouch_data)
        print(f"\n✅ Renderizado completado.")
        print(f"📄 CV: {final_state.get('cv_pdf_path')}")

if __name__ == "__main__":
    asyncio.run(main())
