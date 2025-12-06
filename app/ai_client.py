"""OpenAI client with structured outputs for generating weekly picks."""

import os
from pathlib import Path
from openai import OpenAI
from .models import WeeklyPicksModel
from .config import settings
from .espn_scraper import scrape_espn_schedule, format_games_for_prompt


def render_prompt() -> str:
    """
    Read the prompt template and replace variables with current settings.
    Also fetches live game data from ESPN.
    
    Returns:
        Rendered prompt string with all variables replaced and live game data.
    """
    # Get the prompt template path
    prompt_path = Path(__file__).parent / "prompts" / "weekly_picks.txt"
    
    # Read the template
    with open(prompt_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Extract week and date from ESPN link
    import re
    from datetime import datetime
    espn_link = settings.espn_game_data_link
    week_match = re.search(r'/week/(\d+)', espn_link)
    year_match = re.search(r'/year/(\d+)', espn_link)
    
    if week_match and year_match:
        week_num = week_match.group(1)
        year_num = year_match.group(1)
        current_date = datetime.now().strftime("%Y-%m-%d")
    else:
        # Fallback to default values if parsing fails
        week_num = "13"
        year_num = "2025"
        current_date = "2025-12-03"
    
    # Fetch live game data from ESPN
    try:
        games, metadata = scrape_espn_schedule(settings.espn_game_data_link)
        game_data = format_games_for_prompt(games, settings.focus_games)
    except Exception as e:
        game_data = f"Unable to fetch live game data: {str(e)}\nPlease verify the ESPN URL is correct."
    
    # Replace all variables
    prompt = template.replace("{{SLATE_DESCRIPTION}}", settings.slate_description)
    prompt = prompt.replace("{{NOTE}}", settings.note)
    prompt = prompt.replace("{{FOCUS_GAMES}}", settings.focus_games)
    prompt = prompt.replace("{{MIN_ARTICLES_FOR_SENTIMENT}}", str(settings.min_articles_for_sentiment))
    prompt = prompt.replace("{{INCLUDE_LONG_SHOTS}}", str(settings.include_long_shots).lower())
    prompt = prompt.replace("{{ESPN_GAME_DATA_LINK}}", settings.espn_game_data_link)
    prompt = prompt.replace("{{YEAR}}", year_num)
    prompt = prompt.replace("{{WEEK_NUMBER}}", week_num)
    prompt = prompt.replace("{{DATE}}", current_date)
    
    # Add live game data section
    prompt = f"{prompt}\n\n{game_data}"
    
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
    Save picks to both current_picks.json and a dated historical file.
    
    Args:
        picks: WeeklyPicksModel instance to save.
        filepath: Path to save the current JSON file (relative to project root).
    """
    from datetime import datetime
    import re
    
    # Ensure the data directory exists
    data_dir = Path(filepath).parent
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as current_picks.json
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(picks.model_dump_json(indent=2))
    
    # Extract week and date from ESPN link for filename
    espn_link = settings.espn_game_data_link
    week_match = re.search(r'/week/(\d+)', espn_link)
    year_match = re.search(r'/year/(\d+)', espn_link)
    
    if week_match:
        week = week_match.group(1)
    else:
        week = str(picks.meta.week)  # Fallback to meta.week
    
    # Use current date for historical filename
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    historical_filename = f"week_{week}_{current_date}.json"
    historical_path = data_dir / historical_filename
    
    with open(historical_path, "w", encoding="utf-8") as f:
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