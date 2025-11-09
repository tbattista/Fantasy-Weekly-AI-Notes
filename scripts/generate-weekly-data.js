#!/usr/bin/env node

/**
 * Automated NFL Weekly Data Generator
 * Uses OpenAI API to generate comprehensive NFL game data
 * Runs automatically every Saturday at 7 AM EST via GitHub Actions
 */

const fs = require('fs');
const path = require('path');
const OpenAI = require('openai');

// Configuration
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const CURRENT_WEEK = require('./get-current-week.js');
const SEASON_YEAR = 2025;

// Initialize OpenAI client
if (!OPENAI_API_KEY) {
  console.error('❌ Error: OPENAI_API_KEY environment variable not set');
  process.exit(1);
}

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY
});

/**
 * Get current date in ET timezone ISO format
 */
function getCurrentDateET() {
  const now = new Date();
  const etDate = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
  
  const year = etDate.getFullYear();
  const month = String(etDate.getMonth() + 1).padStart(2, '0');
  const day = String(etDate.getDate()).padStart(2, '0');
  const hours = String(etDate.getHours()).padStart(2, '0');
  const minutes = String(etDate.getMinutes()).padStart(2, '0');
  const seconds = String(etDate.getSeconds()).padStart(2, '0');
  
  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}-05:00`;
}

/**
 * Generate the data generation prompt
 */
function generatePrompt(week, season, asOfDate) {
  return `Week: ${week}
Season: ${season}
as_of_date_et: ${asOfDate}

Pull Vegas lines, weather, injuries, props, and role notes using the most recent publicly available data as of now. Use timestamps in America/New_York time.

ROLE
You are a rigorous NFL data compiler. Produce a single JSON file capturing all Sunday games for Week ${week} of the ${season} NFL season.

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
Return ONLY valid JSON (no markdown, no code blocks, no explanations), matching this exact structure:

{
  "as_of_date_et": "${asOfDate}",
  "week": ${week},
  "games": [
    {
      "game_id": "AWAY@HOME_YYYY-MM-DD",
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
            { "date": "", "opp": "", "total_closing": null, "game_points": null, "result": "", "book": "", "cite": "" }
          ],
          "home": [
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

CRITICAL: Return ONLY the JSON object. No markdown formatting, no code blocks, no explanations before or after.`;
}

/**
 * Validate generated JSON data
 */
function validateData(data, week) {
  const errors = [];
  
  // Check required top-level fields
  if (!data.as_of_date_et) errors.push('Missing as_of_date_et');
  if (data.week !== week) errors.push(`Week mismatch: expected ${week}, got ${data.week}`);
  if (!Array.isArray(data.games)) errors.push('games must be an array');
  if (!data.dfs_player_pool) errors.push('Missing dfs_player_pool');
  if (!Array.isArray(data.sources)) errors.push('sources must be an array');
  
  // Check games array
  if (data.games && data.games.length === 0) {
    errors.push('No games found in data');
  }
  
  // Check sources
  if (data.sources && data.sources.length < 10) {
    errors.push(`Insufficient sources: ${data.sources.length} (minimum 10 recommended)`);
  }
  
  // Check DFS player pool
  const positions = ['qb', 'rb', 'wr', 'te'];
  positions.forEach(pos => {
    if (!data.dfs_player_pool[pos] || !Array.isArray(data.dfs_player_pool[pos])) {
      errors.push(`Missing or invalid dfs_player_pool.${pos}`);
    }
  });
  
  return errors;
}

/**
 * Clean OpenAI response to extract JSON
 */
function cleanJsonResponse(text) {
  // Remove markdown code blocks if present
  let cleaned = text.replace(/```json\n?/g, '').replace(/```\n?/g, '');
  
  // Remove any leading/trailing whitespace
  cleaned = cleaned.trim();
  
  // Find the first { and last }
  const firstBrace = cleaned.indexOf('{');
  const lastBrace = cleaned.lastIndexOf('}');
  
  if (firstBrace !== -1 && lastBrace !== -1) {
    cleaned = cleaned.substring(firstBrace, lastBrace + 1);
  }
  
  return cleaned;
}

/**
 * Main function to generate weekly data
 */
async function generateWeeklyData() {
  console.log('🏈 Fantasy Weekly Data Generator');
  console.log('================================');
  console.log(`Week: ${CURRENT_WEEK}`);
  console.log(`Season: ${SEASON_YEAR}`);
  console.log(`Date: ${getCurrentDateET()}`);
  console.log('');
  
  try {
    // Generate prompt
    const prompt = generatePrompt(CURRENT_WEEK, SEASON_YEAR, getCurrentDateET());
    
    console.log('📡 Calling OpenAI API...');
    console.log(`Model: gpt-4-turbo`);
    console.log('');
    
    // Call OpenAI API
    const completion = await openai.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content: 'You are a precise NFL data compiler. Return ONLY valid JSON with no markdown formatting or explanations.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.3, // Lower temperature for more consistent output
      max_tokens: 16000 // Enough for comprehensive data
    });
    
    const responseText = completion.choices[0].message.content;
    console.log('✅ Received response from OpenAI');
    console.log(`Tokens used: ${completion.usage.total_tokens}`);
    console.log('');
    
    // Clean and parse JSON
    console.log('🔍 Parsing JSON...');
    const cleanedJson = cleanJsonResponse(responseText);
    const data = JSON.parse(cleanedJson);
    
    console.log('✅ JSON parsed successfully');
    console.log('');
    
    // Validate data
    console.log('🔍 Validating data...');
    const errors = validateData(data, CURRENT_WEEK);
    
    if (errors.length > 0) {
      console.log('⚠️  Validation warnings:');
      errors.forEach(err => console.log(`   - ${err}`));
      console.log('');
    } else {
      console.log('✅ Data validation passed');
      console.log('');
    }
    
    // Save to file
    const outputPath = path.join(__dirname, '..', 'data', `week${CURRENT_WEEK}-data.json`);
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf8');
    
    console.log('💾 Data saved successfully');
    console.log(`File: ${outputPath}`);
    console.log('');
    
    // Summary
    console.log('📊 Summary:');
    console.log(`   Games: ${data.games ? data.games.length : 0}`);
    console.log(`   DFS QBs: ${data.dfs_player_pool?.qb?.length || 0}`);
    console.log(`   DFS RBs: ${data.dfs_player_pool?.rb?.length || 0}`);
    console.log(`   DFS WRs: ${data.dfs_player_pool?.wr?.length || 0}`);
    console.log(`   DFS TEs: ${data.dfs_player_pool?.te?.length || 0}`);
    console.log(`   Sources: ${data.sources ? data.sources.length : 0}`);
    console.log('');
    
    console.log('🎉 Weekly data generation complete!');
    
    return data;
    
  } catch (error) {
    console.error('❌ Error generating weekly data:');
    console.error(error.message);
    
    if (error.response) {
      console.error('API Response:', error.response.data);
    }
    
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  generateWeeklyData()
    .then(() => process.exit(0))
    .catch(error => {
      console.error(error);
      process.exit(1);
    });
}

module.exports = generateWeeklyData;