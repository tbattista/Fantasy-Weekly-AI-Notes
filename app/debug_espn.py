"""Debug script to analyze ESPN HTML structure."""

import requests
from bs4 import BeautifulSoup

def debug_espn_html(url: str):
    """Fetch ESPN page and print HTML structure for debugging."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"🔍 Fetching: {url}\n")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Try different selectors
    print("=" * 80)
    print("SEARCHING FOR GAME CONTAINERS")
    print("=" * 80)
    
    # Method 1: ScheduleTables
    schedule_tables = soup.find_all('div', class_='ScheduleTables')
    print(f"\n1. ScheduleTables divs found: {len(schedule_tables)}")
    
    # Method 2: Card sections
    cards = soup.find_all('section', class_='Card')
    print(f"2. Card sections found: {len(cards)}")
    
    # Method 3: Table rows
    table_rows = soup.find_all('tr', class_='Table__TR')
    print(f"3. Table__TR rows found: {len(table_rows)}")
    
    # Method 4: Look for any div with team info
    team_divs = soup.find_all('div', class_=lambda x: x and 'Team' in x)
    print(f"4. Divs with 'Team' in class: {len(team_divs)}")
    
    # Method 5: Search for common ESPN patterns
    print("\n" + "=" * 80)
    print("EXAMINING TABLE STRUCTURE")
    print("=" * 80)
    
    # Find all table rows and examine first few
    all_rows = soup.find_all('tr')
    print(f"\nTotal <tr> elements: {len(all_rows)}")
    
    # Look at first 5 rows with content
    game_count = 0
    for i, row in enumerate(all_rows[:20]):  # Check first 20 rows
        # Look for team links
        team_links = row.find_all('a', class_='AnchorLink')
        
        if len(team_links) >= 2:
            game_count += 1
            print(f"\n--- Game {game_count} (Row {i}) ---")
            print(f"Away Team Link: {team_links[0].get_text(strip=True)}")
            print(f"Home Team Link: {team_links[1].get_text(strip=True) if len(team_links) > 1 else 'N/A'}")
            
            # Check for time info
            time_cells = row.find_all('td')
            print(f"Table cells in row: {len(time_cells)}")
            for j, cell in enumerate(time_cells[:5]):  # First 5 cells
                text = cell.get_text(strip=True)
                if text:
                    print(f"  Cell {j}: {text}")
    
    print("\n" + "=" * 80)
    print("LOOKING FOR TEAM NAMES IN DIVS")
    print("=" * 80)
    
    # Check for team name divs
    team_name_divs = soup.find_all('div', class_='ScoreCell__TeamName')
    print(f"\nScoreCell__TeamName divs: {len(team_name_divs)}")
    for i, div in enumerate(team_name_divs[:10]):
        print(f"{i+1}. {div.get_text(strip=True)}")
    
    # Alternative: Look for span with team abbreviations
    team_abbrevs = soup.find_all('span', class_=lambda x: x and 'abbrev' in str(x).lower())
    print(f"\nTeam abbreviation spans: {len(team_abbrevs)}")
    for i, span in enumerate(team_abbrevs[:10]):
        print(f"{i+1}. {span.get_text(strip=True)}")
    
    print("\n" + "=" * 80)
    print("SAMPLE HTML FROM FIRST TABLE ROW")
    print("=" * 80)
    
    # Print raw HTML of first game row found
    for row in all_rows[:20]:
        team_links = row.find_all('a', class_='AnchorLink')
        if len(team_links) >= 2:
            print("\nFirst game row HTML:")
            print(row.prettify()[:1000])  # First 1000 chars
            break

if __name__ == "__main__":
    url = "https://www.espn.com/nfl/schedule/_/week/15/year/2025/seasontype/2"
    debug_espn_html(url)