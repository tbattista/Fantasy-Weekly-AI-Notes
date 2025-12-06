# ESPN Link Integration and Past Week Article Filtering

## Overview

The system has been updated to use ESPN game data links instead of manual date/week entry, and now filters article sources to only include content from the past week.

## Changes Made

### 1. Configuration Changes

**app/config.py:**
- Replaced `year`, `week_number`, and `date` fields with single `espn_game_data_link` field
- Default ESPN link: `https://www.espn.com/nfl/schedule/_/week/13/year/2025/seasontype/2`

**templates/admin.html:**
- Removed separate Year, Week Number, and Date input fields
- Added single ESPN Game Data Link input field with URL validation
- Added helper text explaining the ESPN link format

### 2. Backend Changes

**app/main.py:**
- Updated `/admin/run` endpoint to accept `espn_game_data_link` instead of separate date/week fields
- Updated `/api/config` endpoint to return ESPN link instead of individual date/week fields
- Modified form processing to extract week/year from ESPN link automatically

**app/ai_client.py:**
- Updated `render_prompt()` to extract week and year from ESPN link using regex
- Modified `save_picks()` to use week from ESPN link for historical filenames
- Added ESPN link variable to prompt template

### 3. Prompt Updates

**app/prompts/weekly_picks.txt:**
- Added `ESPN_GAME_DATA_LINK` variable to template
- Updated instructions to use provided ESPN link for validation
- **CRITICAL**: Added instruction to only use articles from past 7 days for source aggregation
- Enhanced source requirements to emphasize timeliness

## How It Works

### ESPN Link Processing
1. User provides ESPN NFL schedule URL (e.g., `https://www.espn.com/nfl/schedule/_/week/13/year/2025/seasontype/2`)
2. System extracts week number and year using regex patterns
3. Extracted values are used in prompt generation and file naming

### Historical File Naming
- Format: `week_{week_number}_{YYYY-MM-DD}.json`
- Example: `week_13_2025-12-03.json`
- Week number extracted from ESPN link, date uses current generation date

### Article Filtering
- AI is explicitly instructed to only use sources from the past 7 days
- Ensures relevance and timeliness of fantasy analysis
- Prevents outdated information from influencing picks

## Usage

### Admin Configuration
1. Navigate to `/admin`
2. Enter ESPN NFL schedule URL for the desired week
3. Configure other settings (slate description, focus games, etc.)
4. Generate picks

### File Selection
1. Navigate to dashboard (`/`)
2. Use the file selector dropdown in the header
3. Choose between "Current Week (Latest)" or historical files
4. Historical files display as "Week X - YYYY-MM-DD"

## Benefits

1. **Simplified Configuration**: Single ESPN link replaces multiple date/week fields
2. **Automatic Validation**: System uses ESPN schedule as authoritative source
3. **Timely Sources**: Only past week's articles influence decisions
4. **Consistent Naming**: Historical files follow predictable naming pattern
5. **Easy Access**: Dropdown selector for switching between current and past picks

## File Structure

Generated files are saved to `app/data/`:
- `current_picks.json` - Always contains the most recent generation
- `week_{week}_{date}.json` - Historical archive (e.g., `week_13_2025-12-03.json`)

## API Endpoints

- `GET /api/picks/list` - Lists all available JSON files
- `GET /api/picks/{filename}` - Loads specific historical file
- `GET /api/config` - Returns current configuration including ESPN link

## Testing

The system has been tested with:
- ESPN link parsing and week/year extraction
- Historical file generation with correct naming
- File selector dropdown functionality
- Article filtering instructions in prompt

All functionality is working as expected with the new ESPN link integration and past week article filtering.