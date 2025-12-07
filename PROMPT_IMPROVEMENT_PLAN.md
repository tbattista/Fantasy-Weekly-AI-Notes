# Prompt Improvement Plan

## Current Issues Identified

1. **No minimum player requirements** - Categories can have any number of players
2. **No value tier guidance** - No clear indication of salary/value considerations
3. **No data availability flags** - Doesn't note when player data is insufficient
4. **Redundant game listings** - Games listed twice in current prompt
5. **Vague analysis requirements** - Lacks specific output structure guidance

## Proposed Improvements

### 1. Minimum Player Requirements
Each category MUST include:
- **QBs**: Minimum 5 players
- **RBs**: Minimum 5 players  
- **WRs**: Minimum 5 players
- **TEs**: Minimum 5 players

### 2. Value Tier System
Each player should be tagged with a value tier:
- **Elite** ($8,000+) - Premium plays with high floors
- **Mid-Tier** ($6,000-$7,999) - Balanced value options
- **Value** ($4,000-$5,999) - Budget-friendly plays
- **Punt** (<$4,000) - Minimum salary options

### 3. Data Availability Flags
For each player, note data quality:
- **verified: true** - 3+ quality sources with consensus
- **verified: false** - Limited data, proceed with caution
- Add note in `matchup_note` if data is sparse

### 4. Enhanced Structure
- Remove duplicate game listings
- Add explicit minimum requirements to instructions
- Include value tier guidance in analysis requirements
- Add data quality expectations

## Updated Prompt Template

```
You are an expert NFL fantasy and DFS analyst. Generate detailed weekly picks for the specified slate.

# Context
- **NFL Season:** {year}
- **Week:** {week_number}
- **Date:** {date}
- **Slate Description:** {slate_description}
- **ESPN Game Data:** {espn_url}

# Game Focus
Focus on: {focus_games}

# Analysis Requirements
- Minimum {min_articles} articles for sentiment analysis
- Include long shots: {include_long_shots}

# CRITICAL: Minimum Player Requirements
You MUST provide AT LEAST the following number of players per category:
- **QBs**: Minimum 5 players
- **RBs**: Minimum 5 players
- **WRs**: Minimum 5 players
- **TEs**: Minimum 5 players

If fewer quality options exist, include lower-confidence plays but mark them with verified: false.

# Value Tier Guidelines
Categorize each player's value tier in the matchup_note:
- **Elite** ($8,000+) - Premium plays with high floors
- **Mid-Tier** ($6,000-$7,999) - Balanced value options
- **Value** ($4,000-$5,999) - Budget-friendly plays
- **Punt** (<$4,000) - Minimum salary options

# Data Quality Standards
- Set verified: true only when 3+ quality sources agree
- Set verified: false when data is limited or conflicting
- In matchup_note, mention if data is sparse (e.g., "Limited data available")
- Always provide reasoning even with limited data

# Live Game Data
{game_data}

# Task
Provide comprehensive DFS and prop betting recommendations based on the games above:

1. **Top DFS Core Plays by Position**
   - QB, RB, WR, TE picks (minimum 5 each)
   - Include value tier in matchup_note
   - Salary considerations and stacking opportunities
   - Matchup analysis based on actual opponents

2. **Prop Betting Recommendations**
   - Player props (TDs, yards, receptions)
   - Game-specific props based on matchups
   - Confidence levels tied to data quality

3. **Sleepers and Value Plays**
   - Under-the-radar options from the games above
   - Stack recommendations for specific games
   - Highlight value tier plays

4. **Data Quality Notes**
   - Flag players with limited data (verified: false)
   - Note when consensus is weak
   - Provide reasoning even with uncertainty

IMPORTANT: 
- Base recommendations on specific games and matchups listed above
- Reference actual team names and matchups from game data
- MUST meet minimum player counts per category
- Include value tier guidance for each player
- Flag data quality issues appropriately

Return your analysis in valid JSON format matching the WeeklyPicksModel schema.
```

## Implementation Steps

1. ✅ Review current prompt and models
2. ⏳ Update prompt template with new requirements
3. ⏳ Test with sample generation
4. ⏳ Validate output meets minimum requirements

## Benefits

- **Consistency**: Always get minimum 5 players per position
- **Value Awareness**: Clear salary tier guidance for DFS lineup building
- **Transparency**: Know when data is limited or uncertain
- **Better UX**: Users can trust the minimum coverage and understand value plays