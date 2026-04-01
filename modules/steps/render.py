import os
from datetime import datetime
from slugify import slugify
from modules.pipeline import PipelineStep
from modules.pdf_generator import PDFGenerator

class RenderStep(PipelineStep):
    """
    Handles PDF generation and folder organization.
    """
    async def execute(self, state: dict) -> dict:
        config = state['config']
        optimized_data = state['optimized_data']
        job_info = state['job_info']
        
        generator = PDFGenerator()
        timestamp = datetime.now().strftime("%Y-%m-%d")
        user_name_slug = slugify(optimized_data['full_name'])
        job_title_slug = slugify(job_info['title'][:50])
        
        folder_path = generator.create_output_folder(
            job_title=job_info['title'][:50], 
            company="Job"
        )
        
        # 1. Render CV
        cv_filename = f"CV-{user_name_slug}-{job_title_slug}-{timestamp}.pdf"
        cv_output = os.path.join(folder_path, cv_filename)
        await generator.generate_pdf("cv_template.html", optimized_data, cv_output)
        
        # 2. Render Cover Letter (If exists in state)
        letter_pdf_path = None
        if 'letter_content' in state:
            letter_data = {
                "full_name": optimized_data['full_name'],
                "contact": optimized_data['contact'],
                "letter_body": state['letter_content'],
                "portfolio": config['portfolio_url']
            }
            letter_filename = f"Carta-Presentacion-{user_name_slug}-{job_title_slug}-{timestamp}.pdf"
            letter_output = os.path.join(folder_path, letter_filename)
            await generator.generate_pdf("cover_letter_template.html", letter_data, letter_output)
            letter_pdf_path = letter_output

        return {
            "cv_pdf_path": cv_output,
            "letter_pdf_path": letter_pdf_path,
            "output_folder": folder_path
        }
