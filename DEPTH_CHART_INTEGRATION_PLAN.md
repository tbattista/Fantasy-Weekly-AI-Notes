# Depth Chart Integration Plan

## Problem Statement
The AI is returning players with incorrect team assignments (e.g., Derrick Henry as "Tennessee Titans" when he's now on Baltimore Ravens, Saquon Barkley as "New York Giants" when he's on Philadelphia Eagles). We need to integrate the FantasyPros depth chart data to ensure accurate team assignments and only recommend players currently on active rosters.

## Current Issues Identified
1. **Derrick Henry**: Listed as Tennessee Titans → Should be Baltimore Ravens
2. **Stefon Diggs**: Listed as Buffalo Bills → No longer there (traded to Houston Texans)
3. **Saquon Barkley**: Listed as New York Giants → Should be Philadelphia Eagles
4. **Christian McCaffrey**: Game context doesn't match team assignment

## Solution Architecture

### 1. Depth Chart Parser Module (`app/depth_chart_parser.py`)

**Purpose**: Parse the CSV file and create a structured lookup system

**Key Functions**:
```python
def parse_depth_chart(csv_path: str) -> Dict[str, Dict[str, List[str]]]
    """
    Parse FantasyPros depth chart CSV into structured data.
    
    Returns:
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

def get_player_team(player_name: str, depth_chart: Dict) -> Optional[str]
    """
    Look up a player's current team from depth chart.
    Returns team name or None if not found.
    """

def get_team_players(team_name: str, position: str, depth_chart: Dict) -> List[str]
    """
    Get all players for a specific team and position.
    """

def validate_player_team(player_name: str, claimed_team: str, depth_chart: Dict) -> bool
    """
    Verify if a player is actually on the claimed team.
    """

def format_depth_chart_for_prompt(depth_chart: Dict, games: List[str]) -> str
    """
    Format depth chart data for specific games into a prompt-friendly string.
    Only includes teams playing in the specified games.
    """
```

**Data Structure**:
```python
{
    "team_name": {
        "QB": ["Player1", "Player2"],
        "RB": ["Player1", "Player2", "Player3"],
        "WR": ["Player1", "Player2", "Player3", "Player4"],
        "TE": ["Player1", "Player2"]
    }
}
```

### 2. Integration Points

#### A. Prompt Enhancement (`app/ai_client.py`)

**Modify `render_prompt()` function**:
```python
def render_prompt() -> str:
    # ... existing code ...
    
    # Parse depth chart
    from .depth_chart_parser import parse_depth_chart, format_depth_chart_for_prompt
    
    depth_chart_path = Path(__file__).parent.parent / "data" / "FantasyPros_Fantasy_Football_2025_Depth_Charts.csv"
    depth_chart = parse_depth_chart(str(depth_chart_path))
    
    # Format depth chart for games in focus
    depth_chart_context = format_depth_chart_for_prompt(depth_chart, games)
    
    # Add to prompt
    prompt = prompt.replace("{{DEPTH_CHART_DATA}}", depth_chart_context)
    
    return prompt
```

#### B. Prompt Template Update (`app/prompts/weekly_picks.txt`)

**Add new section after Live Game Data**:
```
# Current NFL Depth Charts (2025 Season)
{{DEPTH_CHART_DATA}}

# CRITICAL PLAYER VALIDATION RULES
1. **ONLY recommend players listed in the depth charts above**
2. **Verify each player's team matches the depth chart data**
3. **Cross-reference player names exactly as shown in depth charts**
4. **If a player is not in the depth charts, DO NOT include them**
5. **Focus on players mentioned in articles who are also on current rosters**

When suggesting players:
- Check the depth chart first to confirm their current team
- Prioritize players who appear in both the articles AND the depth charts
- If uncertain about a player's team, exclude them rather than guess
```

#### C. Post-Processing Validation (`app/ai_client.py`)

**Add validation function**:
```python
def validate_and_correct_picks(picks: WeeklyPicksModel, depth_chart: Dict) -> WeeklyPicksModel:
    """
    Validate player-team assignments and flag/correct errors.
    
    Args:
        picks: Generated picks from AI
        depth_chart: Parsed depth chart data
        
    Returns:
        Validated picks with corrections and warnings
    """
    from .depth_chart_parser import validate_player_team, get_player_team
    
    warnings = []
    
    # Validate each category
    for category_name in ['qbs', 'rbs', 'wrs', 'tes']:
        category = getattr(picks.categories, category_name)
        for player in category:
            # Check if player-team combo is valid
            if not validate_player_team(player.name, player.team, depth_chart):
                correct_team = get_player_team(player.name, depth_chart)
                if correct_team:
                    warnings.append(f"⚠️ {player.name}: Corrected team from '{player.team}' to '{correct_team}'")
                    player.team = correct_team
                    player.verified = False  # Mark as unverified due to correction
                else:
                    warnings.append(f"❌ {player.name}: Not found in depth charts - may be outdated")
                    player.verified = False
    
    # Log warnings
    if warnings:
        print("\n=== DEPTH CHART VALIDATION WARNINGS ===")
        for warning in warnings:
            print(warning)
        print("=" * 40 + "\n")
    
    return picks
```

**Update `generate_picks()` function**:
```python
def generate_picks() -> WeeklyPicksModel:
    # ... existing code to get picks from AI ...
    
    # Validate against depth chart
    depth_chart_path = Path(__file__).parent.parent / "data" / "FantasyPros_Fantasy_Football_2025_Depth_Charts.csv"
    depth_chart = parse_depth_chart(str(depth_chart_path))
    
    validated_picks = validate_and_correct_picks(message.parsed, depth_chart)
    
    return validated_picks
```

### 3. Implementation Strategy

#### Phase 1: Core Parser (Priority: HIGH)
- Create `depth_chart_parser.py` with CSV parsing logic
- Implement player-to-team lookup functions
- Add unit tests for parser functions

#### Phase 2: Prompt Integration (Priority: HIGH)
- Update prompt template with depth chart section
- Modify `render_prompt()` to include depth chart data
- Format depth chart data to be concise and relevant to games

#### Phase 3: Validation Layer (Priority: MEDIUM)
- Implement post-processing validation
- Add correction logic for common mistakes
- Create warning/logging system

#### Phase 4: Testing & Refinement (Priority: MEDIUM)
- Test with Week 14 data
- Compare before/after results
- Adjust prompt instructions based on results

### 4. Depth Chart Data Format for Prompt

**Compact Format** (to minimize token usage):
```
ARIZONA CARDINALS vs OPPONENT
QB: Jacoby Brissett, Jeff Driskel
RB: Zonovan Knight, Michael Carter, Emari Demercado, Trey Benson
WR: Marvin Harrison Jr., Michael Wilson, Zay Jones, Xavier Weaver
TE: Trey McBride, Elijah Higgins

BALTIMORE RAVENS vs OPPONENT
QB: Lamar Jackson, Tyler Huntley
RB: Derrick Henry, Justice Hill, Keaton Mitchell
WR: Zay Flowers, Rashod Bateman, DeAndre Hopkins
TE: Mark Andrews, Isaiah Likely
```

### 5. Benefits

1. **Accuracy**: Ensures all player-team assignments are current
2. **Validation**: Catches outdated information from articles
3. **Focus**: Limits recommendations to active roster players
4. **Transparency**: Warnings show when corrections are made
5. **Maintainability**: Easy to update with new depth chart CSV

### 6. Edge Cases to Handle

1. **Player name variations**: "Trent Sherfield Sr." vs "Trent Sherfield"
2. **Injured/suspended players**: Still in depth chart but may be "out"
3. **Practice squad players**: May not be in depth chart
4. **Recent trades**: Depth chart may lag behind real-time moves
5. **Duplicate names**: Handle players with same name on different teams

### 7. Future Enhancements

1. **Injury status integration**: Cross-reference with injury reports
2. **Depth position tracking**: Use ECR rankings from depth chart
3. **Automatic updates**: Fetch latest depth chart from FantasyPros API
4. **Historical tracking**: Compare depth chart changes week-over-week
5. **Confidence scoring**: Higher confidence for higher-ranked depth chart players

## Implementation Files

### New Files
- `app/depth_chart_parser.py` - Core parsing and lookup logic
- `tests/test_depth_chart_parser.py` - Unit tests

### Modified Files
- `app/ai_client.py` - Add depth chart integration and validation
- `app/prompts/weekly_picks.txt` - Add depth chart context and rules
- `requirements.txt` - Add `csv` module (built-in, no changes needed)

## Success Metrics

1. **Zero incorrect team assignments** in generated picks
2. **All players verified** against current depth charts
3. **Clear warnings** when corrections are made
4. **Improved AI accuracy** by providing authoritative roster data
5. **Faster generation** by focusing AI on relevant players only

## Timeline Estimate

- **Phase 1**: 2-3 hours (parser development)
- **Phase 2**: 1-2 hours (prompt integration)
- **Phase 3**: 2-3 hours (validation layer)
- **Phase 4**: 1-2 hours (testing)

**Total**: 6-10 hours for complete implementation

## Next Steps

1. Review and approve this plan
2. Switch to Code mode to implement Phase 1 (parser)
3. Test parser with sample data
4. Implement Phase 2 (prompt integration)
5. Test end-to-end with actual AI generation
6. Refine based on results