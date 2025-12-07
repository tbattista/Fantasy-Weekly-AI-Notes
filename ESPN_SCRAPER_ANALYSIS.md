# ESPN Scraper Analysis and Fix Plan

## Problem Identified

The ESPN scraper is only capturing home teams (showing "@ Green Bay - TBD") instead of complete matchups. Based on the log output:

```
[10:46:20 PM] ✅ Found 16 games
[10:46:20 PM] 1. @ Green Bay - TBD
[10:46:20 PM] 2. @ Kansas City - TBD
...
```

## Root Cause Analysis

### Current Scraper Logic Issues

1. **Outdated CSS Selectors**: The scraper is looking for:
   - `div.ScoreCell__TeamName` for team names
   - `div.ScheduleTables` for game containers
   - `section.Card` as alternative containers

2. **HTML Structure Changes**: ESPN likely updated their HTML structure, and these selectors no longer match the actual page elements.

3. **Incomplete Parsing**: The scraper is finding some elements but not extracting both away and home teams properly.

## ESPN URL Being Used
```
https://www.espn.com/nfl/schedule/_/week/15/year/2025/seasontype/2
```

## Proposed Solution Strategy

### Phase 1: Diagnostic Analysis
1. **Create debug script** to examine actual ESPN HTML structure
2. **Identify current CSS classes** used by ESPN for:
   - Game containers
   - Team names (away/home)
   - Game times
   - Game status

### Phase 2: Update Scraping Logic
1. **Primary Parser Updates**:
   - Update container selectors to match current ESPN structure
   - Fix team name extraction to get both away and home teams
   - Ensure time and status extraction works correctly

2. **Alternative Parser Enhancements**:
   - Improve table row parsing logic
   - Add more robust fallback methods
   - Handle different page layouts (desktop vs mobile)

3. **Error Handling Improvements**:
   - Add detailed logging for debugging
   - Show what HTML elements are actually found
   - Provide better error messages

### Phase 3: Testing and Validation
1. **Test against Week 15 URL**
2. **Verify complete game data extraction**
3. **Ensure all 16 games show proper matchups**

## Expected HTML Structure (Current ESPN Pattern)

Based on typical ESPN schedule pages, the structure is likely:

```html
<table class="Table">
  <tbody>
    <tr class="Table__TR">
      <td class="date__col">1:00 PM</td>
      <td class="team__col">
        <a href="/nfl/team/_/name/nyj/new-york-jets" class="AnchorLink">New York Jets</a>
      </td>
      <td class="team__col">
        <a href="/nfl/team/_/name/mia/miami-dolphins" class="AnchorLink">Miami Dolphins</a>
      </td>
      <td class="status__col">Scheduled</td>
    </tr>
  </tbody>
</table>
```

## Implementation Plan

### Updated scrape_espn_schedule Function
```python
def scrape_espn_schedule(espn_url: str) -> tuple[List[GameData], Dict[str, any]]:
    # 1. Add debug logging
    # 2. Try multiple selector strategies
    # 3. Extract complete game information
    # 4. Handle edge cases gracefully
```

### New Selector Strategies
1. **Table-based parsing** (most reliable)
2. **Div-based container parsing**
3. **Link-based team extraction**
4. **Text pattern matching as fallback**

### Enhanced Error Handling
- Log what selectors found
- Show sample HTML for debugging
- Provide specific error messages
- Continue with partial data if possible

## Next Steps

1. **Switch to Code mode** to implement the diagnostic script
2. **Run diagnostic analysis** against the ESPN URL
3. **Update scraper logic** based on findings
4. **Test thoroughly** with the Week 15 data
5. **Verify complete game matchups** are captured

## Success Criteria

- ✅ All 16 games show complete matchups (Away @ Home)
- ✅ Game times are correctly extracted
- ✅ Game status is properly captured
- ✅ Scraper handles ESPN HTML structure changes gracefully
- ✅ Error messages are informative for debugging