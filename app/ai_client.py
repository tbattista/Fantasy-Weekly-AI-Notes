"""OpenAI client with structured outputs for generating weekly picks."""

import os
from pathlib import Path
from openai import OpenAI
from .models import WeeklyPicksModel
from .config import settings


def render_prompt() -> str:
    """
    Read the prompt template and replace variables with current settings.
    
    Returns:
        Rendered prompt string with all variables replaced.
    """
    # Get the prompt template path
    prompt_path = Path(__file__).parent / "prompts" / "weekly_picks.txt"
    
    # Read the template
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Replace all variables
    prompt = template.replace("{{YEAR}}", str(settings.year))
    prompt = prompt.replace("{{WEEK_NUMBER}}", str(settings.week_number))
    prompt = prompt.replace("{{DATE}}", settings.date)
    prompt = prompt.replace("{{SLATE_DESCRIPTION}}", settings.slate_description)
    prompt = prompt.replace("{{NOTE}}", settings.note)
    prompt = prompt.replace("{{FOCUS_GAMES}}", settings.focus_games)
    prompt = prompt.replace("{{MIN_ARTICLES_FOR_SENTIMENT}}", str(settings.min_articles_for_sentiment))
    prompt = prompt.replace("{{INCLUDE_LONG_SHOTS}}", str(settings.include_long_shots).lower())
    
    return prompt


def generate_picks() -> WeeklyPicksModel:
    """
    Generate weekly picks using OpenAI's structured outputs.
    
    This uses the new client.chat.completions.parse() method which:
    - Automatically validates the response against the Pydantic model
    - Returns a typed Pydantic instance (not raw JSON)
    - Handles errors gracefully
    
    Returns:
        WeeklyPicksModel instance with validated data.
        
    Raises:
        Exception: If OpenAI API call fails or response doesn't match schema.
    """
    # Render the prompt with current settings
    prompt = render_prompt()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=settings.openai_api_key)
    
    # Call OpenAI with structured outputs
    # Note: Must use gpt-4o-2024-08-06 or later for structured outputs
    completion = client.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are an expert NFL fantasy and betting analyst. Return only valid JSON matching the exact schema provided."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=WeeklyPicksModel,  # Pydantic model for automatic validation
        temperature=0.7,  # Some creativity but mostly consistent
    )
    
    # Extract the parsed response
    message = completion.choices[0].message
    
    # Check if parsing was successful
    if message.parsed:
        return message.parsed  # Already a WeeklyPicksModel instance!
    elif message.refusal:
        raise Exception(f"Model refused to generate picks: {message.refusal}")
    else:
        raise Exception("Failed to parse response from OpenAI")


def save_picks(picks: WeeklyPicksModel, filepath: str = "app/data/current_picks.json") -> None:
    """
    Save picks to a JSON file.
    
    Args:
        picks: WeeklyPicksModel instance to save.
        filepath: Path to save the JSON file (relative to project root).
    """
    # Ensure the data directory exists
    data_dir = Path(filepath).parent
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(picks.model_dump_json(indent=2))


def load_picks(filepath: str = "app/data/current_picks.json") -> WeeklyPicksModel:
    """
    Load picks from a JSON file.
    
    Args:
        filepath: Path to the JSON file (relative to project root).
        
    Returns:
        WeeklyPicksModel instance.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        Exception: If the JSON doesn't match the schema.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    
    return WeeklyPicksModel.model_validate_json(data)