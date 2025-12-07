"""Test script for depth chart integration."""

from pathlib import Path
from app.depth_chart_parser import (
    parse_depth_chart,
    get_player_team,
    validate_player_team,
    format_all_depth_charts_compact
)


def test_depth_chart_parser():
    """Test the depth chart parser with known players."""
    
    print("=" * 60)
    print("DEPTH CHART INTEGRATION TEST")
    print("=" * 60)
    
    # Load depth chart
    depth_chart_path = Path("data/FantasyPros_Fantasy_Football_2025_Depth_Charts.csv")
    
    if not depth_chart_path.exists():
        print(f"❌ Error: Depth chart file not found at {depth_chart_path}")
        return
    
    print(f"\n✅ Loading depth chart from: {depth_chart_path}")
    depth_chart = parse_depth_chart(str(depth_chart_path))
    
    print(f"✅ Loaded {len(depth_chart)} teams\n")
    
    # Test cases - players with known team changes
    test_cases = [
        ("Derrick Henry", "Baltimore Ravens", "Should be Ravens, not Titans"),
        ("Saquon Barkley", "Philadelphia Eagles", "Should be Eagles, not Giants"),
        ("Lamar Jackson", "Baltimore Ravens", "Should be Ravens"),
        ("Josh Allen", "Buffalo Bills", "Should be Bills"),
        ("Patrick Mahomes", "Kansas City Chiefs", "Should be Chiefs"),
        ("Stefon Diggs", None, "Traded from Bills - check current team"),
        ("Christian McCaffrey", "San Francisco 49ers", "Should be 49ers"),
    ]
    
    print("Testing player lookups:")
    print("-" * 60)
    
    for player_name, expected_team, note in test_cases:
        actual_team = get_player_team(player_name, depth_chart)
        
        if actual_team:
            if expected_team and actual_team == expected_team:
                print(f"✅ {player_name}: {actual_team} (CORRECT)")
            elif expected_team and actual_team != expected_team:
                print(f"⚠️  {player_name}: {actual_team} (Expected: {expected_team})")
            else:
                print(f"ℹ️  {player_name}: {actual_team} ({note})")
        else:
            print(f"❌ {player_name}: NOT FOUND in depth charts")
    
    print("\n" + "-" * 60)
    print("\nTesting team validation:")
    print("-" * 60)
    
    # Test validation with incorrect teams
    validation_tests = [
        ("Derrick Henry", "Tennessee Titans", False, "Old team - should fail"),
        ("Derrick Henry", "Baltimore Ravens", True, "Current team - should pass"),
        ("Saquon Barkley", "New York Giants", False, "Old team - should fail"),
        ("Saquon Barkley", "Philadelphia Eagles", True, "Current team - should pass"),
    ]
    
    for player_name, claimed_team, should_pass, note in validation_tests:
        is_valid = validate_player_team(player_name, claimed_team, depth_chart)
        
        if is_valid == should_pass:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        print(f"{status}: {player_name} on {claimed_team} -> {is_valid} ({note})")
    
    print("\n" + "=" * 60)
    print("Sample depth chart output (first 3 teams):")
    print("=" * 60)
    
    # Show sample of formatted output
    sample_teams = list(depth_chart.keys())[:3]
    for team in sample_teams:
        print(f"\n{team.upper()}")
        for pos in ['QB', 'RB', 'WR', 'TE']:
            players = depth_chart[team][pos][:3]  # First 3 players
            if players:
                print(f"  {pos}: {', '.join(players)}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_depth_chart_parser()