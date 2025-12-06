"""ESPN web scraper for fetching live NFL game data."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime


class GameData:
    """Data structure for NFL game information."""
    def __init__(self, away_team: str, home_team: str, time: str, status: str = "Scheduled"):
        self.away_team = away_team
        self.home_team = home_team
        self.time = time
        self.status = status
        self.matchup = f"{away_team} @ {home_team}"
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "away_team": self.away_team,
            "home_team": self.home_team,
            "time": self.time,
            "status": self.status,
            "matchup": self.matchup
        }


def scrape_espn_schedule(espn_url: str) -> tuple[List[GameData], Dict[str, any]]:
    """
    Scrape ESPN NFL schedule page for game data.
    
    Args:
        espn_url: ESPN NFL schedule URL (e.g., https://www.espn.com/nfl/schedule/_/week/13/year/2025/seasontype/2)
    
    Returns:
        Tuple of (list of GameData objects, metadata dict with week/year info)
    """
    try:
        # Fetch the page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(espn_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        games = []
        
        # Extract week and year from URL
        import re
        week_match = re.search(r'/week/(\d+)', espn_url)
        year_match = re.search(r'/year/(\d+)', espn_url)
        week = int(week_match.group(1)) if week_match else None
        year = int(year_match.group(1)) if year_match else None
        
        # ESPN schedule structure: Look for game containers
        # This may need adjustment based on ESPN's current HTML structure
        game_containers = soup.find_all('div', class_='ScheduleTables')
        
        if not game_containers:
            # Try alternative selectors
            game_containers = soup.find_all('section', class_='Card')
        
        for container in game_containers:
            # Find team names
            teams = container.find_all('div', class_='ScoreCell__TeamName')
            if len(teams) >= 2:
                away_team = teams[0].get_text(strip=True)
                home_team = teams[1].get_text(strip=True)
                
                # Find game time
                time_element = container.find('div', class_='ScoreCell__Time')
                game_time = time_element.get_text(strip=True) if time_element else "TBD"
                
                # Find game status
                status_element = container.find('div', class_='ScoreCell__Status')
                status = status_element.get_text(strip=True) if status_element else "Scheduled"
                
                game = GameData(away_team, home_team, game_time, status)
                games.append(game)
        
        # If no games found with primary method, try alternative parsing
        if not games:
            games = _parse_alternative_format(soup)
        
        metadata = {
            "week": week,
            "year": year,
            "games_found": len(games),
            "scraped_at": datetime.now().isoformat()
        }
        
        return games, metadata
        
    except Exception as e:
        raise Exception(f"Error scraping ESPN: {str(e)}")


def _parse_alternative_format(soup: BeautifulSoup) -> List[GameData]:
    """Alternative parser for different ESPN HTML structures."""
    games = []
    
    # Try finding by table rows
    rows = soup.find_all('tr', class_='Table__TR')
    
    for row in rows:
        try:
            # Look for team links
            team_links = row.find_all('a', class_='AnchorLink')
            if len(team_links) >= 2:
                away_team = team_links[0].get_text(strip=True)
                home_team = team_links[1].get_text(strip=True)
                
                # Get time from row
                time_cell = row.find('td', class_='date__col')
                game_time = time_cell.get_text(strip=True) if time_cell else "TBD"
                
                game = GameData(away_team, home_team, game_time)
                games.append(game)
        except:
            continue
    
    return games


def format_games_for_prompt(games: List[GameData], focus_games: str = "all") -> str:
    """
    Format game data for inclusion in AI prompt.
    
    Args:
        games: List of GameData objects
        focus_games: Filter for specific games ("all", "afternoon_only", or specific matchups)
    
    Returns:
        Formatted string with game information
    """
    if not games:
        return "No game data available. Please check the ESPN URL."
    
    # Filter games based on focus_games parameter
    filtered_games = games
    
    if focus_games != "all":
        if "afternoon" in focus_games.lower():
            # Filter for afternoon games (typically 4:05 PM ET and later)
            filtered_games = [g for g in games if "4:" in g.time or "8:" in g.time]
        elif "early" in focus_games.lower():
            # Filter for early games (typically 1:00 PM ET)
            filtered_games = [g for g in games if "1:" in g.time]
        elif "primetime" in focus_games.lower():
            # Filter for primetime games (typically 8:00+ PM ET)
            filtered_games = [g for g in games if "8:" in g.time or "9:" in g.time]
        else:
            # Assume it's a comma-separated list of specific matchups
            focus_list = [m.strip() for m in focus_games.split(",")]
            filtered_games = [g for g in games if any(team in g.matchup for team in focus_list)]
    
    # Format output
    lines = ["# NFL Games for Analysis\n"]
    for i, game in enumerate(filtered_games, 1):
        lines.append(f"{i}. **{game.matchup}** - {game.time} ({game.status})")
    
    lines.append(f"\nTotal games to analyze: {len(filtered_games)}")
    
    return "\n".join(lines)