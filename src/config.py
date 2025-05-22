import os
import yaml
from pathlib import Path

def load_config():
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load configuration
CONFIG = load_config()

# Environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

# LLM Configuration
LLM_CONFIG = {
    "config_list": [
        {
            "model": CONFIG["llm"]["model"],
            "api_key": ANTHROPIC_API_KEY,
            "base_url": CONFIG["llm"]["base_url"],
            "api_type": CONFIG["llm"]["api_type"]
        }
    ],
    "temperature": CONFIG["llm"]["temperature"],
}

# Export commonly used config values
BATCH_SIZE = CONFIG["scraping"]["batch_size"]

PERFECT_SCORE_THRESHOLD = CONFIG["scoring"]["perfect_score_threshold"]
GOOD_SCORE_THRESHOLD = CONFIG["scoring"]["good_score_threshold"]
FAIR_SCORE_THRESHOLD = CONFIG["scoring"]["fair_score_threshold"]
POOR_SCORE_THRESHOLD = CONFIG["scoring"]["poor_score_threshold"]

EARLY_TERMINATION_SCORE = CONFIG["agent"]["early_termination_score"]