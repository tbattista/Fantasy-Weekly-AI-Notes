"""Quick test of the updated ESPN scraper."""

from app.espn_scraper import scrape_espn_schedule, format_games_for_prompt

def test_scraper():
    url = "https://www.espn.com/nfl/schedule/_/week/15/year/2025/seasontype/2"
    
    print("🚀 Testing ESPN Scraper...")
    print(f"URL: {url}\n")
    
    try:
        games, metadata = scrape_espn_schedule(url)
        
        print(f"✅ Found {len(games)} games\n")
        print("=" * 80)
        
        for i, game in enumerate(games, 1):
            print(f"{i}. {game.matchup} - {game.time}")
        
        print("\n" + "=" * 80)
        print("\nFormatted for AI prompt:\n")
        print(format_games_for_prompt(games, "all"))
        
        print("\n" + "=" * 80)
        print("\nMetadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scraper()