# 🚀 ATS-Master CV Generator Pro

A "Senior" level resume generator designed to beat **ATS (Applicant Tracking Systems)** with a match score higher than 95%. Automate the entire process: from job scraping to generating a premium PDF.

## 🌟 Features

- **Multi-Offer Support**: Process a list of URLs in a single command. Generate as many resumes as job offers provided.
- **Dynamic Scraping**: Extracts job descriptions from LinkedIn, InfoJobs, and other platforms using Playwright.
- **GitHub Analysis**: Reads your repository READMEs to integrate real technical evidence into your CV.
- **Multi-LLM Native**: Built-in support for **Google Gemini**, **OpenAI**, and **Anthropic**.
- **Premium PDF**: Professional PDF generation from HTML/CSS templates with selectable text.
- **Automatic Organization**: Every application gets its own folder in `output/` with its custom CV and Cover Letter.

## 🛠️ Technical Requirements

- Python 3.10+
- [Playwright](https://playwright.dev/python/) for scraping and rendering.
- API Key for Gemini, OpenAI, or Anthropic.

## 🚀 Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ro0oman/pythonCVGenerator.git
   cd pythonCVGenerator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. **Configure environment variables**:
   Create a `.env` file based on `.env.example`:
   ```env
   GEMINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   GITHUB_TOKEN=optional_but_recommended
   ```

4. **Configure your data**:
    Edit `data.json` with the list of job URLs and your profiles:
    ```json
    {
      "job_urls": [
        "JOB_URL_1",
        "JOB_URL_2"
      ],
      "portfolio_url": "YOUR_PORTFOLIO",
      "github_url": "YOUR_GITHUB",
      "generate_cover_letter": true,
      "llm_provider": "gemini"
    }
    ```

5. **Upload your base CV**:
   Place your current resume as `cv_original.pdf` or `cv_original.txt` in the project root.

## 💻 Usage

Run the main orchestrator:

```bash
python main.py
```

The script will notify you in the console when finished. You can find your documents at:
`output/[Date]-[Company]-[Job]/`

## 🖌️ Retouch Mode (Human-in-the-Loop)

ATS-Master Pro (V7+) allows you to manually refine the content before generating the final PDF. This workflow is ideal for adjusting details that the AI might have over-optimized.

1.  **Full Execution**: Run the script normally. A `resume_to_retouch.json` file will be generated in the output folder of each offer.
2.  **Manual Editing**: Open that JSON and modify the fields you want (such as `summary` or experience `achievements`).

    ```json
    {
      "optimized_data": {
        "summary": "Fullstack Developer with 5 years of experience...",
        "experience": [
          {
            "role": "Senior Engineer",
            "achievements": ["Team leadership", "Migration to AWS"]
          }
        ]
      }
    }
    ```

3.  **Final Rendering**: Launch the generator again in `render` mode pointing to your edited JSON:

    ```bash
    python main.py --mode render --data output/JOB_FOLDER/resume_to_retouch.json
    ```

## 📁 Project Structure

```text
├── main.py              # Main orchestrator
├── data.json            # Offer and profile configuration
├── requirements.txt     # Python dependencies
├── modules/             # Modular logic
│   ├── scraper.py       # Playwright scraping
│   ├── github_analyzer.py # Repository analysis
│   ├── llm_factory.py    # Multi-AI interface
│   ├── cv_optimizer.py   # Prompt engineering and LLM logic
│   └── pdf_generator.py  # HTML -> PDF rendering
├── templates/           # Visual templates (HTML/CSS)
└── output/              # Generated resumes
```

---
Made with ❤️ by [Antigravity](https://github.com/google-gemini) for **Roman Myziuk**.
