# AI Photography Quality Auditor

A technical audit and critical mentorship tool for photographers. This uses Gemini 2.5 Flash to perform simultaneous hardware-level diagnostics and professional critiques through an agentic multimodal pipeline

## Features
- Multimodal Analysis: Combines raw pixel data with extracted EXIF metadata to cross-reference hardware settings against visual results
- Provides advanced technical advice for professional photography in key fields like color theory and lighting
- Automatically cleans EXIF logs by stripping unreadable binary fields
- Zero-bloat local host UI for user convenience

## Tech Stack
- **Model:** Gemini 2.5 Flash
- **UI:** Streamlit
- **Imaging:** Pillow (PIL)
- **Environment:** Python 3.10+, Dotenv

## Installation
1. Clone the repo: `git clone <your-url>`
2. Install requirements: `pip install -r requirements.txt`
3. Add your `GOOGLE_API_KEY` to a `.env` file.
4. Run `streamlit run app.py`.