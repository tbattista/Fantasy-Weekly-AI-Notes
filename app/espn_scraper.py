"""ESPN web scraper for fetching live NFL game data."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import re


class GameData:
    """Data structure for NFL game information with time slot categorization."""
    def __init__(self, away_team: str, home_team: str, time: str, status: str = "Scheduled", day_of_week: str = ""):
        self.away_team = away_team
        self.home_team = home_team
        self.time = time
        self.status = status
        self.matchup = f"{away_team} @ {home_team}"
        self.day_of_week = day_of_week
        self.time_slot = self._categorize_time_slot()
        self.game_id = self._generate_game_id()
    
    def _categorize_time_slot(self) -> str:
        """
        Categorize game into time slot based on time string and day.
        
        Returns:
            One of: 'early', 'afternoon', 'night', 'monday', 'thursday'
        """
        time_lower = self.time.lower()
        day_lower = self.day_of_week.lower()
        
        # Check for specific days first
        if 'monday' in day_lower or 'mon' in day_lower:
            return 'monday'
        elif 'thursday' in day_lower or 'thu' in day_lower:
            return 'thursday'
        
        # Parse time for Sunday games
        # Extract hour from time string (e.g., "1:00 PM", "4:05 PM", "8:20 PM")
        time_match = re.search(r'(\d+):(\d+)', self.time)
        if time_match:
            hour = int(time_match.group(1))
            
            # Determine if PM (most NFL games are PM)
            is_pm = 'pm' in time_lower or 'p.m.' in time_lower
            
            # Convert to 24-hour for easier comparison
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            
            # Categorize by time
            if 13 <= hour < 16:  # 1:00 PM - 3:59 PM
                return 'early'
            elif 16 <= hour < 20:  # 4:00 PM - 7:59 PM
                return 'afternoon'
            elif hour >= 20:  # 8:00 PM and later
                return 'night'
        
        # Default to early if can't determine
        return 'early'
    
    def _generate_game_id(self) -> str:
        """
        Generate unique game ID.
        
        Returns:
            Format: {away_team}_{home_team}_{time_slot}
        """
        # Clean team names (remove spaces, special chars)
        away_clean = re.sub(r'[^A-Za-z0-9]', '', self.away_team)
        home_clean = re.sub(r'[^A-Za-z0-9]', '', self.home_team)
        return f"{away_clean}_{home_clean}_{self.time_slot}"
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for JSON serialization."""
        return {
            "away_team": self.away_team,
            "home_team": self.home_team,
            "time": self.time,
            "status": self.status,
            "matchup": self.matchup,
            "day_of_week": self.day_of_week,
            "time_slot": self.time_slot,
            "game_id": self.game_id
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
        week_match = re.search(r'/week/(\d+)', espn_url)
        year_match = re.search(r'/year/(\d+)', espn_url)
        week = int(week_match.group(1)) if week_match else None
        year = int(year_match.group(1)) if year_match else None
        
        # Try to extract day of week from section headers
        current_day = ""
        
        # Parse using table rows - ESPN's current structure
        table_rows = soup.find_all('tr', class_='Table__TR')
        
        for row in table_rows:
            try:
                # Check if this row is a date header
                header = row.find('th', class_='Table__TH')
                if header:
                    # Extract day of week from header (e.g., "Thursday, December 5")
                    header_text = header.get_text(strip=True)
                    if header_text:
                        # Extract day name (first word before comma)
                        day_match = re.match(r'(\w+)', header_text)
                        if day_match:
                            current_day = day_match.group(1)
                    continue
                
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
                        game = GameData(away_team, home_team, game_time, "Scheduled", current_day)
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
    current_day = ""
    
    # Try finding by table rows (same as primary now, but kept for compatibility)
    rows = soup.find_all('tr', class_='Table__TR')
    
    for row in rows:
        try:
            # Check for date header
            header = row.find('th', class_='Table__TH')
            if header:
                header_text = header.get_text(strip=True)
                if header_text:
                    day_match = re.match(r'(\w+)', header_text)
                    if day_match:
                        current_day = day_match.group(1)
                continue
            
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
                    game = GameData(away_team, home_team, game_time, "Scheduled", current_day)
                    games.append(game)
        except:
            continue
    
    return games


def group_games_by_time_slot(games: List[GameData]) -> Dict[str, List[GameData]]:
    """
    Group games by their time slot category.
    
    Args:
        games: List of GameData objects
    
    Returns:
        Dictionary with time slots as keys and lists of games as values
    """
    grouped = {
        'early': [],
        'afternoon': [],
        'night': [],
        'monday': [],
        'thursday': []
    }
    
    for game in games:
        time_slot = game.time_slot
        if time_slot in grouped:
            grouped[time_slot].append(game)
    
    return grouped


def format_games_for_prompt(games: List[GameData], focus_games: str = "all", selected_game_ids: Optional[List[str]] = None) -> str:
    """
    Format game data for inclusion in AI prompt.
    
    Args:
        games: List of GameData objects
        focus_games: Filter for specific games ("all", "afternoon_only", or specific matchups) - legacy parameter
        selected_game_ids: List of game IDs to include (None = use focus_games parameter)
    
    Returns:
        Formatted string with game information
    """
    if not games:
        return "No game data available. Please check the ESPN URL."
    
    # New system: Filter by selected game IDs
    if selected_game_ids is not None:
        filtered_games = [g for g in games if g.game_id in selected_game_ids]
    # Legacy system: Filter by focus_games string
    elif focus_games != "all":
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
    else:
        filtered_games = games
    
    if not filtered_games:
        return "No games match the selected criteria."
    
    # Group by time slot for better organization
    grouped = group_games_by_time_slot(filtered_games)
    
    # Format output with time slot headers
    lines = ["# NFL Games for Analysis\n"]
    game_count = 0
    
    time_slot_labels = {
        'early': '🕐 EARLY GAMES (1:00 PM ET)',
        'afternoon': '🕓 AFTERNOON GAMES (4:00 PM ET)',
        'night': '🌙 NIGHT GAMES (8:00+ PM ET)',
        'monday': '🏈 MONDAY NIGHT FOOTBALL',
        'thursday': '🏈 THURSDAY NIGHT FOOTBALL'
    }
    
    for slot in ['early', 'afternoon', 'night', 'thursday', 'monday']:
        if grouped[slot]:
            lines.append(f"\n## {time_slot_labels[slot]}")
            for game in grouped[slot]:
                game_count += 1
                lines.append(f"{game_count}. **{game.matchup}** - {game.time}")
    
    lines.append(f"\n**Total games to analyze: {game_count}**")
    
    return "\n".join(lines)