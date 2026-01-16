# AI Photography Quality Auditor

A technical multi-agent system built with **Gemini 2.5 Flash** and **Python** to analyze digital photography quality by cross-referencing raw EXIF metadata with visual pixel analysis.

## Features
- **Metadata Extraction:** Reads ISO, F-stop, Shutter Speed, and Exposure Bias.
- **Forensic Analysis:** Identifies "Software Bokeh" vs. Optical blur.
- **Automated Reporting:** Generates a technical health grade (A-F) based on hardware performance.

## Tech Stack
- **AI Model:** Gemini 2.5 Flash
- **Framework:** Google Generative AI SDK
- **Imaging:** Pillow (PIL)
- **Environment:** Python 3.10+, Dotenv, Git

## Installation
1. Clone the repo: `git clone <your-url>`
2. Install requirements: `pip install -r requirements.txt`
3. Add your `GOOGLE_API_KEY` to a `.env` file.
4. Run `python agent.py`.