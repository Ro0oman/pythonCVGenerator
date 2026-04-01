import asyncio
import json
import os
from dotenv import load_dotenv
from modules.scraper import scrape_job_offer
from modules.github_analyzer import get_recent_github_repos
from modules.pdf_parser import parse_cv
from modules.cv_optimizer import CVOptimizer
from modules.pdf_generator import PDFGenerator

load_dotenv()

async def main():
    print("🚀 Iniciando ATS-Master CV Generator Pro...")
    
    # 1. Cargar Configuración
    if not os.path.exists('data.json'):
        print("[!] Error: No se encuentra data.json")
        return
        
    with open('data.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    cv_path = "cv_original.pdf" if os.path.exists("cv_original.pdf") else "cv_original.txt"
    if not os.path.exists(cv_path):
        print(f"[!] Error: No se encuentra {cv_path}")
        # Creamos un placeholder para evitar que rompa el script en el primer run
        with open("cv_original.txt", "w") as f: f.write("Tu CV base va aquí.")
        cv_path = "cv_original.txt"

    # 2. Scrapping de la oferta
    job_info = await scrape_job_offer(config['job_url'])
    if not job_info:
        print("[!] Error al obtener la oferta. Abortando.")
        return

    # 3. Análisis de GitHub
    github_projects = get_recent_github_repos(config['github_url'])

    # 4. Parsing del CV Original
    original_cv_text = parse_cv(cv_path)

    # 5. Optimización con LLM
    print(f"[*] Optimizando contenido con {config.get('llm_provider', 'gemini')}...")
    optimizer = CVOptimizer(provider=config.get('llm_provider', 'gemini'))
    
    optimized_data = await optimizer.optimize_cv(
        job_description=job_info['content'],
        original_cv=original_cv_text,
        github_projects=json.dumps(github_projects),
        portfolio_url=config['portfolio_url']
    )
    
    if not optimized_data:
        print("[!] Fallo en la optimización del LLM.")
        return

    # 6. Generación de PDF y Carpetas
    generator = PDFGenerator()
    folder_path = generator.create_output_folder(
        job_title=job_info['title'][:50], 
        company="Job"
    )
    
    # Render CV
    cv_output = os.path.join(folder_path, "CV_Optimizado.pdf")
    await generator.generate_pdf("cv_template.html", optimized_data, cv_output)

    # Render Cover Letter (Optional)
    if config.get('generate_cover_letter'):
        print("[*] Generando Carta de Presentación...")
        letter_content = await optimizer.generate_cover_letter(
            job_description=job_info['content'],
            cv_data=optimized_data,
            portfolio_url=config['portfolio_url']
        )
        
        letter_data = {
            "full_name": optimized_data['full_name'],
            "contact": optimized_data['contact'],
            "letter_body": letter_content,
            "portfolio": config['portfolio_url']
        }
        
        letter_output = os.path.join(folder_path, "Carta_Presentacion.pdf")
        await generator.generate_pdf("cover_letter_template.html", letter_data, letter_output)

    print("\n✅ Proceso completado con éxito.")
    print(f"📂 Archivos generados en: {folder_path}")

if __name__ == "__main__":
    asyncio.run(main())
