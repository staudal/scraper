# AI Web Content Extractor

A tool that uses AI agents to scrape websites and answer questions based on the content.

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set your Anthropic API key as an environment variable:
   - Windows: `set ANTHROPIC_API_KEY=your_api_key_here`
   - Mac/Linux: `export ANTHROPIC_API_KEY=your_api_key_here`
6. (Optional) Modify `config.yaml` to customize settings like batch size, model, temperature, etc.

## Usage

Run the web scraping agent with a URL and a question:

```bash
python -m src.agent --url "https://example.com" --question "What services does this company offer?"
```

The agent will:
1. Scrape the website in batches
2. Score each batch for relevance to your question
3. Extract and return the answer from the most relevant content

## Features

- Handles large websites by processing content in batches
- Scores content relevance to find the most useful information
- Returns concise answers extracted from the best content

## Flow

Website (10,000 words) → Split into 100 batches of 100 words each

↓

Score batch 1: 45/100

Score batch 2: 78/100

Score batch 3: 23/100

...

Score batch 67: 92/100 ← Best match

↓

Extract answer from only batch 67

## Configuration

The system uses `config.yaml` for all configuration settings:

- **LLM settings**: Model, temperature, API endpoints
- **Scraping settings**: Batch size
- **Scoring thresholds**: Score ranges for relevance assessment
- **Agent limits**: Early termination rules