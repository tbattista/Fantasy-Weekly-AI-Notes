# 📅 Weekly Dashboard Update Guide

This guide explains how to update your Fantasy Weekly NFL Dashboard with fresh data each week using the AI data generation prompt.

---

## 🎯 Quick Update Process

### Step 1: Generate New Data (5-10 minutes)

Use this prompt with ChatGPT, Claude, or your preferred AI:

```
Week: {WEEK_NUMBER}
Season: {SEASON_YEAR}
as_of_date_et: {CURRENT_DATE_ISO_ET}

Pull Vegas lines, weather, injuries, props, and role notes using the most recent publicly available data as of now. Use timestamps in America/New_York time.

ROLE
You are a rigorous NFL data compiler. Produce a single JSON file capturing all Sunday games for Week {WEEK_NUMBER} of the {SEASON_YEAR} NFL season.

SCOPE
- Sunday games only (no SNF if requested, otherwise include it).
- Use the official NFL schedule to confirm the exact matchups and date.
- Offense only: QB / RB / WR / TE
- No DST, no kickers.

SOURCING REQUIREMENTS
- Minimum 15–20 reputable sources
- Prioritize: ESPN, CBS Sports, SportsLine
- Also acceptable: Rotowire, Rotogrinders, FantasyPros, Action Network, NumberFire, PFF, FTN, The Athletic, team sites, Vegas books
- For news/DFS takes/injuries, use last 5 days relative to today
- All non-obvious claims must include a cite tag like [ESPN-1]

WHAT TO RETURN
Return ONLY JSON, matching this exact structure:

{
  "as_of_date_et": "{CURRENT_DATE_ISO_ET}",
  "week": {WEEK_NUMBER},
  "games": [
    {
      "game_id": "BUF@MIA_YYYY-MM-DD",
      "kickoff_et": "YYYY-MM-DDTHH:MM:SS-05:00",
      "venue": "",
      "surface": "",
      "is_dome": false,
      "city": "",
      "timezone": "America/New_York",
      "broadcast": "",

      "vegas": {
        "spread": "",
        "total": "",
        "implied_totals": { "away": null, "home": null },
        "book": "",
        "line_timestamp_et": "",
        "over_under_trends": {
          "away": [
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" }
          ],
          "home": [
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" },
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" }
          ],
          "team_summary": {
            "away": { "overs": 0, "unders": 0, "pushes": 0, "avg_total_points": null, "outlier_flags": [] },
            "home": { "overs": 0, "unders": 0, "pushes": 0, "avg_total_points": null, "outlier_flags": [] }
          }
        }
      },

      "weather": {
        "forecast_source": "",
        "observed_at_et": "",
        "temp_f": null,
        "wind_mph_sustained": null,
        "wind_mph_gust": null,
        "precip_chance_pct": null,
        "conditions": "",
        "weather_impact_note": "",
        "cite": ""
      },

      "dfs": {
        "qb": [],
        "rb": [],
        "wr": [],
        "te": []
      },

      "player_props": [],
      "injuries": [],
      "narrative_notes": []
    }
  ],

  "dfs_player_pool": {
    "qb": [],
    "rb": [],
    "wr": [],
    "te": []
  },

  "outlier_summary": {
    "teams_consistently_over": [],
    "teams_consistently_under": [],
    "notes": []
  },

  "weather_watch": [],

  "sources": [
    {
      "tag": "[ESPN-1]",
      "title": "",
      "outlet": "ESPN",
      "date": "",
      "url": "",
      "note": ""
    }
  ],

  "generation_notes": {
    "method": "Compiled using public sources from last 5 days",
    "assumptions": [],
    "data_quality_flags": []
  }
}
```

### Step 2: Save the Generated JSON

1. Copy the JSON output from the AI
2. Replace the content in `data/week{X}-data.json`
3. Validate the JSON is properly formatted

### Step 3: Deploy to Railway

```bash
# Navigate to your project directory
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Add the updated data file
git add data/week{X}-data.json

# Commit with descriptive message
git commit -m "Update Week {X} data - {DATE}"

# Push to GitHub (triggers automatic Railway deployment)
git push
```

### Step 4: Verify Deployment (2-5 minutes)

1. Wait for Railway to redeploy (automatic)
2. Visit: https://fantasyweekly-production.up.railway.app
3. Verify new data is displaying correctly

---

## 📋 Weekly Checklist

Use this checklist each week:

### Tuesday/Wednesday (Data Preparation)
- [ ] Check NFL schedule for Week {X} games
- [ ] Note any schedule changes (flexed games, postponements)
- [ ] Gather current date/time in ET format

### Thursday (Data Generation)
- [ ] Run AI prompt with correct week number and date
- [ ] Review generated JSON for completeness
- [ ] Validate JSON syntax (use jsonlint.com if needed)
- [ ] Check that all games are included
- [ ] Verify DFS player pool is populated

### Friday (Deployment)
- [ ] Save JSON to `data/week{X}-data.json`
- [ ] Update any references to week number in code (if needed)
- [ ] Commit and push to GitHub
- [ ] Monitor Railway deployment
- [ ] Test dashboard functionality
- [ ] Verify all pages load correctly

### Saturday (Final Check)
- [ ] Review for any last-minute injury updates
- [ ] Check weather forecasts are current
- [ ] Verify Vegas lines are up-to-date
- [ ] Share dashboard link with your league

---

## 🔧 Required Inputs Each Week

Replace these placeholders in the prompt:

| Placeholder | Example | How to Get |
|-------------|---------|------------|
| `{WEEK_NUMBER}` | `11` | Current NFL week |
| `{SEASON_YEAR}` | `2025` | Current NFL season |
| `{CURRENT_DATE_ISO_ET}` | `2025-11-15T00:00:00-05:00` | Today's date in ISO format (ET timezone) |

### Quick Date Format Generator

For the current date in ET timezone:
```javascript
// Run in browser console or Node.js
new Date().toLocaleString('en-US', { 
  timeZone: 'America/New_York',
  year: 'numeric',
  month: '2-digit', 
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
  hour12: false
}).replace(/(\d+)\/(\d+)\/(\d+),\s(\d+):(\d+):(\d+)/, '$3-$1-$2T$4:$5:$6-05:00')
```

Or use this format: `YYYY-MM-DDTHH:MM:SS-05:00`

---

## 📁 File Naming Convention

Keep your data files organized:

```
data/
├── week10-data.json  ✅ Current format
├── week11-data.json  ✅ Next week
├── week12-data.json  ✅ Future weeks
└── archive/          📦 Optional: Store old weeks
    ├── week9-data.json
    └── week8-data.json
```

---

## 🔄 Automation Options

### Option 1: Manual Weekly Update (Current)
- Run AI prompt manually
- Copy/paste JSON
- Git commit and push
- **Time**: 10-15 minutes per week

### Option 2: Semi-Automated (Recommended)
1. Create a script to validate JSON
2. Use git hooks to auto-commit on file change
3. Still manually generate data with AI

### Option 3: Fully Automated (Advanced)
- Set up API integration with data providers
- Schedule weekly cron job
- Auto-generate and deploy
- **Requires**: API keys, server setup, monitoring

---

## 🛠️ Validation Script

Create `scripts/validate-data.js` to check your JSON:

```javascript
const fs = require('fs');

function validateWeekData(weekNumber) {
  const filePath = `./data/week${weekNumber}-data.json`;
  
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    
    // Check required fields
    const checks = {
      'as_of_date_et': !!data.as_of_date_et,
      'week': data.week === weekNumber,
      'games': Array.isArray(data.games) && data.games.length > 0,
      'dfs_player_pool': !!data.dfs_player_pool,
      'sources': Array.isArray(data.sources) && data.sources.length >= 15
    };
    
    console.log('Validation Results:');
    Object.entries(checks).forEach(([key, passed]) => {
      console.log(`  ${passed ? '✅' : '❌'} ${key}`);
    });
    
    return Object.values(checks).every(v => v);
  } catch (error) {
    console.error('❌ JSON Parse Error:', error.message);
    return false;
  }
}

// Usage: node scripts/validate-data.js 11
const week = process.argv[2] || 10;
const isValid = validateWeekData(week);
process.exit(isValid ? 0 : 1);
```

Run before deploying:
```bash
node scripts/validate-data.js 11
```

---

## 📊 Data Quality Checklist

Before deploying, verify:

### Games Data
- [ ] All Sunday games included
- [ ] Correct kickoff times (ET timezone)
- [ ] Venue information complete
- [ ] Weather data for outdoor games
- [ ] Vegas lines from reputable book

### DFS Player Pool
- [ ] QB: 8-12 players with salaries
- [ ] RB: 15-20 players with salaries
- [ ] WR: 20-30 players with salaries
- [ ] TE: 8-12 players with salaries
- [ ] All players have projections

### Sources
- [ ] Minimum 15 sources cited
- [ ] Mix of ESPN, CBS, FantasyPros, etc.
- [ ] All sources dated within last 5 days
- [ ] URLs included where applicable

### Injuries
- [ ] Key injuries noted for each game
- [ ] Status (Out/Doubtful/Questionable) included
- [ ] Impact assessment provided
- [ ] Sources cited

---

## 🚨 Troubleshooting

### JSON Validation Errors

**Problem**: "Unexpected token" or "Invalid JSON"

**Solution**:
1. Copy JSON to jsonlint.com
2. Fix syntax errors (missing commas, brackets)
3. Ensure all strings use double quotes
4. Remove any trailing commas

### Missing Data

**Problem**: Some games or players missing

**Solution**:
1. Re-run AI prompt with emphasis on completeness
2. Manually add missing data
3. Cross-reference with NFL.com schedule

### Deployment Doesn't Update

**Problem**: Dashboard shows old data after push

**Solution**:
1. Check Railway deployment logs
2. Verify file was committed: `git log --oneline`
3. Hard refresh browser: Ctrl+Shift+R
4. Check Railway build completed successfully

### Data Not Displaying

**Problem**: Dashboard loads but shows no games

**Solution**:
1. Open browser console (F12)
2. Check for JavaScript errors
3. Verify JSON file path is correct
4. Ensure week number matches in code

---

## 📈 Enhancement Ideas

### Future Improvements
1. **Multi-Week View**: Show data for multiple weeks
2. **Historical Comparison**: Compare current week to past weeks
3. **Player Trends**: Track player performance over season
4. **Live Updates**: Pull live scores during games
5. **Mobile App**: Create PWA for mobile access
6. **Email Alerts**: Send weekly summary to league
7. **API Integration**: Auto-pull from DraftKings/FanDuel

---

## 🎯 Best Practices

### Timing
- **Generate data**: Thursday afternoon (after practice reports)
- **Deploy**: Friday morning (before lineup locks)
- **Final update**: Saturday evening (last-minute changes)

### Data Sources Priority
1. **Vegas Lines**: Use closing lines from major books
2. **Weather**: Check 24-48 hours before game
3. **Injuries**: Monitor up to kickoff
4. **DFS Salaries**: Lock in Thursday/Friday

### Communication
- Share dashboard link with league on Friday
- Post updates in league chat for major changes
- Note any data quality issues in dashboard

---

## 📞 Support

### Issues with Data Generation
- Review AI prompt for completeness
- Try different AI model if output is inconsistent
- Manually verify critical data points

### Issues with Deployment
- Check [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for Railway help
- Review git commit history
- Monitor Railway dashboard for errors

### Issues with Dashboard
- Check browser console for JavaScript errors
- Verify JSON structure matches expected format
- Test on different browsers/devices

---

## ✅ Success Metrics

Your weekly update is successful when:

- ✅ JSON validates without errors
- ✅ All games for the week are included
- ✅ DFS player pool is comprehensive
- ✅ Sources are cited and recent
- ✅ Railway deployment completes
- ✅ Dashboard displays all data correctly
- ✅ Mobile view works properly
- ✅ League members can access and use it

---

## 📅 Season-Long Workflow

### Pre-Season (August)
- Set up dashboard infrastructure
- Test with preseason data
- Share with league for feedback

### Regular Season (September-December)
- Weekly updates every Thursday/Friday
- Monitor for bye weeks
- Track player trends

### Playoffs (January)
- Focus on playoff teams
- Increase update frequency
- Add playoff-specific insights

### Off-Season (February-July)
- Archive season data
- Plan improvements
- Prepare for next season

---

**🏈 Keep your dashboard fresh with weekly updates!**

This process takes 10-15 minutes per week and keeps your league engaged with the latest NFL insights.