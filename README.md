# 🚀 ATS-Master CV Generator Pro

Un generador de currículums de nivel "Senior" diseñado para superar los filtros **ATS (Applicant Tracking Systems)** con una puntuación de coincidencia superior al 95%. Automatiza todo el proceso: desde el scraping de la oferta hasta la generación de un PDF premium.

## 🌟 Características

- **Multi-Oferta**: Procesa una lista de URLs en un solo comando. Genera tantos CVs como ofertas de empleo proporciones.
- **Scraping Dinámico**: Extrae descripciones de empleo de LinkedIn, InfoJobs y otros portales usando Playwright.
- **Análisis de GitHub**: Lee los READMEs de tus repositorios para integrar evidencias técnicas reales.
- **Multi-LLM Native**: Soporte para **Google Gemini**, **OpenAI** y **Anthropic**.
- **PDF Premium**: Generación de PDFs profesionales desde plantillas HTML/CSS.
- **Organización Automática**: Cada aplicación tiene su propia carpeta en `output/`.

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
    Edita `data.json` con la lista de URLs de las ofertas y tus perfiles:
    ```json
    {
      "job_urls": [
        "URL_OFERTA_1",
        "URL_OFERTA_2"
      ],
      "portfolio_url": "TU_PORTFOLIO",
      "github_url": "TU_GITHUB",
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

## 🖌️ Modo Retoque (Human-in-the-Loop)

ATS-Master Pro (V7+) permite refinar manualmente el contenido antes de generar el PDF final. Este flujo es ideal para ajustar matices que la IA haya podido sobre-optimizar.

1.  **Ejecución Completa**: Corre el script normalmente. Se generará un archivo `resume_to_retouch.json` en la carpeta de salida de cada oferta.
2.  **Edición Manual**: Abre dicho JSON y modifica los campos que desees (como `summary` o los `achievements` de la experiencia).

    ```json
    {
      "optimized_data": {
        "summary": "Fullstack Developer con 5 años de experiencia...",
        "experience": [
          {
            "role": "Senior Engineer",
            "achievements": ["Liderazgo de equipo", "Migración a AWS"]
          }
        ]
      }
    }
    ```

3.  **Renderizado Final**: Lanza de nuevo el generador en modo `render` apuntando a tu JSON editado:

    ```bash
    python main.py --mode render --data output/CARPETA_OFERTA/resume_to_retouch.json
    ```

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