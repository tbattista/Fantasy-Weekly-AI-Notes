# DFS/Props Picks App - Architecture Plan

## 🎯 Project Overview

A production-ready web application that generates weekly NFL DFS and prop betting recommendations using AI (OpenAI GPT), with a clean admin interface for configuration and a beautiful dashboard for viewing picks.

### Key Features
- **AI-Powered Data Generation**: Single master prompt generates structured JSON data
- **Admin Interface**: Configure variables, preview prompts, trigger manual refreshes
- **Dashboard**: Display picks with the existing beautiful card-based UI
- **Production Ready**: Deployable to Railway with scheduled jobs support

---

## 📁 Project Structure

```
dfs-picks-app/
├── README.md                          # Setup and deployment guide
├── requirements.txt                   # Python dependencies
├── Procfile                          # Railway/Heroku deployment config
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore patterns
├── railway.json                      # Railway-specific configuration
│
├── app/
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # FastAPI application entrypoint
│   ├── config.py                     # Settings from environment variables
│   ├── models.py                     # Pydantic models for JSON schema
│   ├── ai_client.py                  # OpenAI integration & prompt rendering
│   ├── scheduler.py                  # Data refresh logic
│   │
│   ├── prompts/
│   │   └── weekly_picks_prompt.txt   # Master prompt template
│   │
│   └── data/
│       └── current_picks.json        # Generated AI output (gitignored)
│
├── templates/
│   ├── base.html                     # Sneat layout wrapper with nav/sidebar
│   ├── dashboard.html                # Main picks display (extends base)
│   └── admin.html                    # Admin controls (extends base)
│
└── static/
    ├── css/
    │   ├── core.css                  # Sneat core styles
    │   └── custom.css                # Custom card styling from current UI
    ├── js/
    │   ├── main.js                   # Sneat main JS
    │   └── dashboard.js              # Dashboard-specific JS
    └── vendor/
        ├── libs/
        │   ├── jquery/
        │   ├── popper/
        │   └── perfect-scrollbar/
        └── fonts/
```

---

## 🏗️ Architecture Components

### 1. Backend (FastAPI + Python)

#### **main.py** - Application Entry Point
```python
FastAPI app with routes:
- GET  /                    → Dashboard (renders dashboard.html)
- GET  /api/picks           → Returns current_picks.json as JSON
- GET  /admin               → Admin page (renders admin.html)
- POST /admin/run           → Triggers refresh_weekly_picks()
- GET  /api/config          → Returns current config values
- POST /api/config          → Updates config values (optional)
```

#### **config.py** - Configuration Management
```python
Uses pydantic-settings to load from environment:
- OPENAI_API_KEY           (required)
- YEAR                     (default: current year)
- WEEK_NUMBER              (default: current week)
- DATE                     (default: today)
- SLATE_DESCRIPTION        (default: "Sunday main slate")
- NOTE                     (default: auto-generated)
- FOCUS_GAMES              (default: "all")
- MIN_ARTICLES_FOR_SENTIMENT (default: 3)
- INCLUDE_LONG_SHOTS       (default: true)
```

#### **models.py** - Pydantic Data Models
```python
Exact schema matching your JSON structure:
- MetaModel
- SourceModel
- SuggestionModel
- PlayerModel
- LongShotPredictionModel
- LongShotPlayerModel
- LongShotsModel
- CategoriesModel
- WeeklyPicksModel (root)
```

#### **ai_client.py** - OpenAI Integration
```python
Functions:
- render_prompt(config) → str
  Reads weekly_picks_prompt.txt and replaces {{VARIABLES}}
  
- call_openai(prompt) → dict
  Sends to OpenAI API, parses JSON response
  Validates against Pydantic models
  
- generate_picks(config) → WeeklyPicksModel
  Combines render + call + validate
```

#### **scheduler.py** - Data Refresh
```python
Functions:
- refresh_weekly_picks() → bool
  Calls ai_client.generate_picks()
  Writes to app/data/current_picks.json
  Returns success/failure
  
- scheduled_refresh() → None
  Wrapper for Railway cron jobs
```

---

### 2. Frontend (Jinja2 Templates + Sneat)

#### **base.html** - Layout Wrapper
- Sneat sidebar navigation
- Top navbar with user menu
- Content wrapper area
- Footer
- All CSS/JS includes

#### **dashboard.html** - Main Picks Display
**Preserves your current UI design:**
```html
Features:
- Week/Date badges at top
- Position filter dropdown
- Grid layout of player cards with:
  * Position badge (colored: QB/RB/WR/TE)
  * Player name + team
  * Injury status badge
  * Verified badge
  * Game matchup
  * Matchup note
  * Target stats
  * Why explanation
  * Suggestion badges (over/under/yes)
  * Source tags with sentiment
- Separate long shots section
```

**Card Styling (from your current index.html):**
- Compact cards with hover effects
- Color-coded position badges
- Inline suggestion badges
- Source sentiment indicators
- Responsive grid layout

#### **admin.html** - Configuration Interface
```html
Features:
- Form with all configurable variables
- Live prompt preview (shows rendered prompt)
- "Generate Picks" button → POST /admin/run
- Status messages (success/error)
- Display last generated JSON (collapsible)
- Link to view dashboard
```

---

### 3. Static Assets

#### **CSS Structure**
```
static/css/
├── core.css              # Sneat core (copied from template)
└── custom.css            # Your player card styles
```

#### **JavaScript Structure**
```
static/js/
├── main.js               # Sneat functionality
└── dashboard.js          # Position filtering, card rendering
```

#### **Vendor Libraries**
```
static/vendor/
├── libs/
│   ├── jquery/
│   ├── popper/
│   ├── bootstrap/
│   └── perfect-scrollbar/
└── fonts/
```

---

## 🔄 Data Flow

### Initial Page Load (Dashboard)
```
User → GET / 
  → FastAPI reads app/data/current_picks.json
  → Renders dashboard.html with data
  → Browser displays player cards
```

### Manual Refresh (Admin)
```
User → GET /admin
  → Displays form with current config
  
User → Fills form → POST /admin/run
  → FastAPI calls scheduler.refresh_weekly_picks()
    → ai_client.render_prompt(config)
    → ai_client.call_openai(prompt)
    → Validates with Pydantic models
    → Writes to current_picks.json
  → Returns success/error
  → Redirects to dashboard
```

### API Access
```
External → GET /api/picks
  → Returns current_picks.json as JSON
  → Can be used by other apps/scripts
```

---

## 🔐 Security & Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=sk-proj-...

# Optional (with defaults)
YEAR=2025
WEEK_NUMBER=13
DATE=2025-11-30
SLATE_DESCRIPTION="Sunday main slate"
NOTE="Generated picks for Week 13"
FOCUS_GAMES="all"
MIN_ARTICLES_FOR_SENTIMENT=3
INCLUDE_LONG_SHOTS=true
```

### .gitignore
```
.env
app/data/current_picks.json
__pycache__/
*.pyc
.venv/
venv/
```

---

## 🚀 Deployment (Railway)

### Procfile
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### railway.json (Optional Cron)
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Deployment Steps
1. Push to GitHub
2. Connect Railway to repo
3. Set environment variables in Railway dashboard
4. Deploy automatically
5. (Optional) Add Railway cron job for weekly refresh

---

## 📦 Dependencies (requirements.txt)

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
jinja2==3.1.3
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
openai>=1.0.0
aiofiles==23.2.1
```

---

## 🎨 UI Design Preservation

### Current Card Design Elements to Keep
1. **Compact Layout**: Minimal padding, efficient space usage
2. **Color Coding**: Position-specific badge colors
3. **Inline Badges**: Suggestions displayed as colored pills
4. **Hover Effects**: Subtle shadow on card hover
5. **Responsive Grid**: Auto-fill columns based on screen size
6. **Typography**: Clean hierarchy with varied font sizes
7. **Status Indicators**: Injury status, verified badges
8. **Source Tags**: Small pills with sentiment colors

### Sneat Integration Points
- Use Sneat's sidebar navigation
- Use Sneat's top navbar
- Use Sneat's card component base
- Use Sneat's color variables
- Use Sneat's responsive utilities
- Keep your custom card styling on top

---

## 🧪 Testing Strategy

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up .env file
cp .env.example .env
# Edit .env with your OpenAI API key

# 3. Run locally
uvicorn app.main:app --reload

# 4. Test endpoints
- http://localhost:8000/          (Dashboard)
- http://localhost:8000/admin     (Admin)
- http://localhost:8000/api/picks (API)
```

### Manual Testing Checklist
- [ ] Dashboard loads and displays existing JSON
- [ ] Position filter works correctly
- [ ] Admin page displays all config fields
- [ ] Prompt preview renders correctly
- [ ] Generate button triggers AI call
- [ ] Success/error messages display
- [ ] Generated JSON is valid
- [ ] Dashboard updates with new data
- [ ] API endpoint returns valid JSON
- [ ] Responsive design works on mobile

---

## 📝 Implementation Order

### Phase 1: Project Setup (Steps 1-3)
1. Create directory structure
2. Generate configuration files
3. Set up .gitignore and .env.example

### Phase 2: Backend Core (Steps 4-6)
4. Create Pydantic models
5. Implement config.py
6. Create master prompt template

### Phase 3: AI Integration (Steps 7-8)
7. Build ai_client.py
8. Implement scheduler.py

### Phase 4: FastAPI App (Step 9)
9. Create main.py with all routes

### Phase 5: Frontend (Steps 10-12)
10. Build base.html template
11. Create dashboard.html with card styling
12. Build admin.html

### Phase 6: Static Assets (Step 13)
13. Copy Sneat files and create custom.css

### Phase 7: Testing & Deployment (Steps 14-16)
14. Test locally
15. Prepare Railway config
16. Write documentation

---

## 🎯 Success Criteria

✅ **Functional Requirements**
- AI generates valid JSON matching schema
- Dashboard displays picks beautifully
- Admin can configure and trigger refreshes
- API endpoint provides JSON access
- Deploys successfully to Railway

✅ **Non-Functional Requirements**
- UI matches current design aesthetic
- Response time < 2s for dashboard
- AI generation completes in < 60s
- Mobile responsive
- Error handling for API failures

✅ **Documentation**
- Clear README with setup steps
- Environment variable documentation
- Deployment guide for Railway
- API endpoint documentation

---

## 🔮 Future Enhancements (Post-MVP)

1. **Authentication**: Add login for admin page
2. **History**: Store multiple weeks of picks
3. **Comparison**: Compare AI picks vs actual results
4. **Scheduling**: Automatic weekly refresh via Railway cron
5. **Notifications**: Email/Slack when new picks generated
6. **Analytics**: Track pick accuracy over time
7. **Export**: Download picks as CSV/PDF
8. **Multi-Model**: Support different LLM providers

---

## 📚 Key Technical Decisions

### Why FastAPI?
- Modern, fast, async support
- Automatic API documentation
- Great for Railway deployment
- Excellent Pydantic integration

### Why Jinja2?
- Server-side rendering for SEO
- Simple template syntax
- Good FastAPI integration
- Easy to maintain

### Why Pydantic?
- Strong type validation
- JSON schema generation
- Excellent error messages
- FastAPI native support

### Why Single Prompt?
- Simpler to maintain
- Consistent output format
- Easier to version control
- Reduces API costs

---

## 🎨 Visual Design Notes

### Color Palette (from current UI)
- **QB**: Blue (#1976d2, #e3f2fd)
- **RB**: Green (#388e3c, #e8f5e9)
- **WR**: Purple (#7b1fa2, #f3e5f5)
- **TE**: Orange (#f57c00, #fff3e0)
- **Over**: Green (#2e7d32, #e8f5e9)
- **Under**: Red (#c62828, #ffebee)
- **Yes**: Blue (#1565c0, #e3f2fd)

### Typography
- **Headers**: 1.1rem, 600 weight
- **Player Names**: 0.95rem, 600 weight
- **Body Text**: 0.75-0.8rem
- **Badges**: 0.65-0.7rem

### Spacing
- **Card Padding**: 8-10px
- **Card Margin**: 8px bottom
- **Grid Gap**: 10px
- **Badge Gap**: 4px

---

This architecture provides a solid foundation for a production-ready app that preserves your beautiful UI while adding powerful AI-driven data generation capabilities.