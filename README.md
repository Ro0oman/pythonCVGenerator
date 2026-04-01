# 🚀 ATS-Master CV Generator Pro

Un generador de currículums de nivel "Senior" diseñado para superar los filtros **ATS (Applicant Tracking Systems)** con una puntuación de coincidencia superior al 95%. Automatiza todo el proceso: desde el scraping de la oferta hasta la generación de un PDF premium.

## 🌟 Características

- **Scraping Dinámico**: Extrae descripciones de empleo de LinkedIn, InfoJobs y otros portales usando Playwright (manejando JS y renderizado dinámico).
- **Análisis de GitHub**: Lee los READMEs de tus 3 repositorios más recientes para integrar evidencias técnicas reales en tu CV.
- **Multi-LLM Native**: Soporte integrado para **Google Gemini**, **OpenAI (GPT-4o)** y **Anthropic (Claude 3.5)**.
- **Optimización ATS**: Redacción basada en palabras clave, verbos de acción y métricas cuantificables.
- **PDF Premium**: Generación directa de PDFs profesionales (con texto seleccionable) a partir de plantillas HTML/CSS.
- **Organización por Oferta**: Crea automáticamente una carpeta en `output/` para cada aplicación con su CV y Carta de Presentación.

## 🛠️ Requisitos Técnicos

- Python 3.10+
- [Playwright](https://playwright.dev/python/) para scraping y renderizado.
- API Key de Gemini, OpenAI o Anthropic.

## 🚀 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Ro0oman/pythonCVGenerator.git
   cd pythonCVGenerator
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. **Configurar variables de entorno**:
   Crea un archivo `.env` basado en `.env.example`:
   ```env
   GEMINI_API_KEY=tu_clave_aqui
   OPENAI_API_KEY=tu_clave_aqui
   ANTHROPIC_API_KEY=tu_clave_aqui
   GITHUB_TOKEN=opcional_pero_recomendado
   ```

4. **Configurar tus datos**:
   Edita `data.json` con la URL de la oferta y tus perfiles sociales:
   ```json
   {
     "job_url": "URL_DE_LA_OFERTA",
     "portfolio_url": "TU_PORTFOLIO",
     "github_url": "TU_GITHUB",
     "linkedin_url": "TU_LINKEDIN",
     "generate_cover_letter": true,
     "llm_provider": "gemini"
   }
   ```

5. **Subir tu CV base**:
   Coloca tu currículum actual como `cv_original.pdf` o `cv_original.txt` en la raíz del proyecto.

## 💻 Uso

Ejecuta el orquestador principal:

```bash
python main.py
```

El script te avisará por consola cuando termine y podrás encontrar tus documentos en:
`output/[Fecha]-[Empresa]-[Puesto]/`

## 📁 Estructura del Proyecto

```text
├── main.py              # Orquestador del flujo completo
├── data.json            # Configuración de la oferta y perfiles
├── requirements.txt     # Dependencias de Python
├── modules/             # Lógica modular
│   ├── scraper.py       # Playwright scraping
│   ├── github_analyzer.py # Análisis de repositorios
│   ├── llm_factory.py    # Interfaz multi-IA
│   ├── cv_optimizer.py   # Prompt engineering y lógica LLM
│   └── pdf_generator.py  # Renderizado HTML -> PDF
├── templates/           # Plantillas visuales (HTML/CSS)
└── output/              # Currículums generados
```

---
Creado con ❤️ por [Antigravity](https://github.com/google-gemini) para **Roman Myziuk**.