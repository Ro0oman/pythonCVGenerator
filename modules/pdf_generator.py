import os
import asyncio
from playwright.async_api import async_playwright
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from slugify import slugify

class PDFGenerator:
    """
    Renders HTML/CSS templates into a professional PDF using Playwright.
    """
    
    def __init__(self, template_dir="templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = "output"
        
    def create_output_folder(self, job_title, company=""):
        """
        Creates a folder for the specific job offer.
        Example: output/2024-04-01-google-software-engineer/
        """
        timestamp = datetime.now().strftime("%Y-%m-%d")
        folder_name = slugify(f"{timestamp}-{company}-{job_title}")
        path = os.path.join(self.output_dir, folder_name)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        return path

    async def generate_pdf(self, template_name, data, output_path):
        """
        Renders an HTML template with data and saves it as PDF via Playwright.
        """
        template = self.env.get_template(template_name)
        html_content = template.render(data=data)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set direct HTML content
            await page.set_content(html_content)
            
            # Wait for all resources (fonts, etc.)
            await page.wait_for_load_state("networkidle")
            
            # Print to PDF with premium settings (A4, high quality)
            await page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"}
            )
            
            await browser.close()
            print(f"[*] PDF Generado con éxito: {output_path}")

if __name__ == "__main__":
    # Mock test
    pass
