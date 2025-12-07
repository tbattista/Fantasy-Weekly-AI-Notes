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
        
        # Parse using table rows - ESPN's current structure
        table_rows = soup.find_all('tr', class_='Table__TR')
        
        for row in table_rows:
            try:
                # Get all table cells
                cells = row.find_all('td')
                
                if len(cells) >= 3:
                    # Cell 0: Away team
                    # Cell 1: @Home team
                    # Cell 2: Game time
                    
                    # Extract away team from first cell
                    away_links = cells[0].find_all('a', class_='AnchorLink')
                    away_team = away_links[-1].get_text(strip=True) if away_links else None
                    
                    # Extract home team from second cell (format: "@TeamName")
                    home_text = cells[1].get_text(strip=True)
                    home_team = home_text.replace('@', '').strip() if '@' in home_text else None
                    
                    # Extract game time from third cell
                    game_time = cells[2].get_text(strip=True) if len(cells) > 2 else "TBD"
                    
                    # Only create game if we have both teams
                    if away_team and home_team:
                        game = GameData(away_team, home_team, game_time, "Scheduled")
                        games.append(game)
            except Exception as e:
                # Skip rows that don't match expected format
                continue
        
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
    
    # Try finding by table rows (same as primary now, but kept for compatibility)
    rows = soup.find_all('tr', class_='Table__TR')
    
    for row in rows:
        try:
            # Get all table cells
            cells = row.find_all('td')
            
            if len(cells) >= 3:
                # Cell 0: Away team
                # Cell 1: @Home team
                # Cell 2: Game time
                
                # Extract away team from first cell
                away_links = cells[0].find_all('a', class_='AnchorLink')
                away_team = away_links[-1].get_text(strip=True) if away_links else None
                
                # Extract home team from second cell (format: "@TeamName")
                home_text = cells[1].get_text(strip=True)
                home_team = home_text.replace('@', '').strip() if '@' in home_text else None
                
                # Extract game time from third cell
                game_time = cells[2].get_text(strip=True) if len(cells) > 2 else "TBD"
                
                # Only create game if we have both teams
                if away_team and home_team:
                    game = GameData(away_team, home_team, game_time, "Scheduled")
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