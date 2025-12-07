"""Parser for FantasyPros depth chart CSV data."""

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def parse_depth_chart(csv_path: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Parse FantasyPros depth chart CSV into structured data.
    
    Args:
        csv_path: Path to the depth chart CSV file
        
    Returns:
        Dictionary mapping team names to positions to player lists:
        {
            "Arizona Cardinals": {
                "QB": ["Jacoby Brissett", "Jeff Driskel"],
                "RB": ["Zonovan Knight", "Michael Carter", ...],
                "WR": ["Michael Wilson", "Xavier Weaver", ...],
                "TE": ["Trey McBride", "Elijah Higgins", ...]
            },
            ...
        }
    """
    depth_chart = {}
    current_team = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            # Skip empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue
            
            # Check if this is a team name row (single non-empty cell)
            if len(row) == 1 or (len(row) > 1 and all(cell.strip() == '' for cell in row[1:])):
                team_name = row[0].strip().strip('"')
                if team_name and not team_name.startswith('ECR'):
                    current_team = team_name
                    depth_chart[current_team] = {
                        'QB': [],
                        'RB': [],
                        'WR': [],
                        'TE': []
                    }
                continue
            
            # Skip header rows
            if 'Quarterbacks' in str(row) or 'ECR' in str(row[0]):
                continue
            
            # Parse player data rows
            if current_team and len(row) >= 8:
                # QB (columns 1)
                qb_name = row[1].strip().strip('"')
                if qb_name and qb_name != '-' and not qb_name.startswith('ECR'):
                    depth_chart[current_team]['QB'].append(qb_name)
                
                # RB (column 3)
                rb_name = row[3].strip().strip('"')
                if rb_name and rb_name != '-' and not rb_name.startswith('ECR'):
                    depth_chart[current_team]['RB'].append(rb_name)
                
                # WR (column 5)
                wr_name = row[5].strip().strip('"')
                if wr_name and wr_name != '-' and not wr_name.startswith('ECR'):
                    depth_chart[current_team]['WR'].append(wr_name)
                
                # TE (column 7)
                te_name = row[7].strip().strip('"')
                if te_name and te_name != '-' and not te_name.startswith('ECR'):
                    depth_chart[current_team]['TE'].append(te_name)
    
    return depth_chart


def normalize_player_name(name: str) -> str:
    """
    Normalize player name for comparison (remove suffixes, lowercase, etc.).
    
    Args:
        name: Player name to normalize
        
    Returns:
        Normalized player name
    """
    # Remove common suffixes
    name = name.replace(' Jr.', '').replace(' Sr.', '').replace(' III', '').replace(' II', '')
    # Remove extra whitespace and convert to lowercase
    return ' '.join(name.split()).lower()


def get_player_team(player_name: str, depth_chart: Dict[str, Dict[str, List[str]]]) -> Optional[str]:
    """
    Look up a player's current team from depth chart.
    
    Args:
        player_name: Name of the player to look up
        depth_chart: Parsed depth chart data
        
    Returns:
        Team name if found, None otherwise
    """
    normalized_search = normalize_player_name(player_name)
    
    for team, positions in depth_chart.items():
        for position, players in positions.items():
            for player in players:
                if normalize_player_name(player) == normalized_search:
                    return team
    
    return None


def get_team_players(team_name: str, position: str, depth_chart: Dict[str, Dict[str, List[str]]]) -> List[str]:
    """
    Get all players for a specific team and position.
    
    Args:
        team_name: Name of the team
        position: Position code (QB, RB, WR, TE)
        depth_chart: Parsed depth chart data
        
    Returns:
        List of player names for that team/position
    """
    if team_name in depth_chart and position in depth_chart[team_name]:
        return depth_chart[team_name][position]
    return []


def validate_player_team(player_name: str, claimed_team: str, depth_chart: Dict[str, Dict[str, List[str]]]) -> bool:
    """
    Verify if a player is actually on the claimed team.
    
    Args:
        player_name: Name of the player
        claimed_team: Team the player is claimed to be on
        depth_chart: Parsed depth chart data
        
    Returns:
        True if player is on the claimed team, False otherwise
    """
    actual_team = get_player_team(player_name, depth_chart)
    if actual_team is None:
        return False
    
    # Normalize team names for comparison
    return normalize_player_name(actual_team) == normalize_player_name(claimed_team)


def extract_team_from_game(game_str: str) -> Tuple[str, str]:
    """
    Extract team names from game string (e.g., "Cincinnati @ Buffalo").
    
    Args:
        game_str: Game string in format "Away @ Home"
        
    Returns:
        Tuple of (away_team, home_team)
    """
    if '@' in game_str:
        parts = game_str.split('@')
        away = parts[0].strip()
        home = parts[1].strip()
        return (away, home)
    return ('', '')


def find_team_in_depth_chart(team_partial: str, depth_chart: Dict[str, Dict[str, List[str]]]) -> Optional[str]:
    """
    Find full team name from partial match (e.g., "Buffalo" -> "Buffalo Bills").
    
    Args:
        team_partial: Partial team name
        depth_chart: Parsed depth chart data
        
    Returns:
        Full team name if found, None otherwise
    """
    team_partial_lower = team_partial.lower()
    
    for team_name in depth_chart.keys():
        if team_partial_lower in team_name.lower():
            return team_name
    
    return None


def format_depth_chart_for_prompt(depth_chart: Dict[str, Dict[str, List[str]]], games: List[Dict]) -> str:
    """
    Format depth chart data for specific games into a prompt-friendly string.
    
    Args:
        depth_chart: Parsed depth chart data
        games: List of game dictionaries with 'away_team' and 'home_team' keys
        
    Returns:
        Formatted string with depth chart data for relevant teams
    """
    output_lines = []
    teams_included = set()
    
    # Collect all teams from games
    for game in games:
        away_team = find_team_in_depth_chart(game.get('away_team', ''), depth_chart)
        home_team = find_team_in_depth_chart(game.get('home_team', ''), depth_chart)
        
        if away_team:
            teams_included.add(away_team)
        if home_team:
            teams_included.add(home_team)
    
    # Format depth chart for included teams
    for team in sorted(teams_included):
        if team in depth_chart:
            output_lines.append(f"\n{team.upper()}")
            
            positions = depth_chart[team]
            
            # Format each position
            if positions['QB']:
                output_lines.append(f"  QB: {', '.join(positions['QB'][:3])}")  # Top 3 QBs
            
            if positions['RB']:
                output_lines.append(f"  RB: {', '.join(positions['RB'][:5])}")  # Top 5 RBs
            
            if positions['WR']:
                output_lines.append(f"  WR: {', '.join(positions['WR'][:6])}")  # Top 6 WRs
            
            if positions['TE']:
                output_lines.append(f"  TE: {', '.join(positions['TE'][:3])}")  # Top 3 TEs
    
    return '\n'.join(output_lines)


def format_all_depth_charts_compact(depth_chart: Dict[str, Dict[str, List[str]]]) -> str:
    """
    Format all depth chart data in a compact format for the prompt.
    
    Args:
        depth_chart: Parsed depth chart data
        
    Returns:
        Formatted string with all depth chart data
    """
    output_lines = []
    
    for team in sorted(depth_chart.keys()):
        positions = depth_chart[team]
        
        output_lines.append(f"\n{team.upper()}")
        
        # Format each position with top players only
        if positions['QB']:
            output_lines.append(f"  QB: {', '.join(positions['QB'][:2])}")
        
        if positions['RB']:
            output_lines.append(f"  RB: {', '.join(positions['RB'][:4])}")
        
        if positions['WR']:
            output_lines.append(f"  WR: {', '.join(positions['WR'][:5])}")
        
        if positions['TE']:
            output_lines.append(f"  TE: {', '.join(positions['TE'][:2])}")
    
    return '\n'.join(output_lines)