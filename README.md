# 🏈 DFS/Props Picks Generator

AI-powered weekly NFL DFS and prop betting recommendations using OpenAI's structured outputs.

## ✨ Features

- **AI-Powered Generation**: Uses OpenAI GPT-4 with structured outputs for guaranteed JSON schema compliance
- **Beautiful Dashboard**: Clean, responsive UI with your existing card design
- **Admin Interface**: Easy configuration and manual pick generation
- **Production Ready**: Deployable to Railway with one click
- **API Access**: RESTful API endpoint for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git (for deployment)

### Local Development

1. **Clone or navigate to the project directory**

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-proj-your-key-here
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open your browser**
   - Dashboard: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api/picks

## 📁 Project Structure

```
Fantasy Weekly AI Notes/ (root)
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI application
│   ├── config.py             # Settings management
│   ├── models.py             # Pydantic models
│   ├── ai_client.py          # OpenAI integration
│   ├── prompts/
│   │   └── weekly_picks.txt  # Master prompt template
│   └── data/
│       └── current_picks.json # Generated picks (gitignored)
├── templates/
│   ├── base.html             # Base layout
│   ├── dashboard.html        # Main picks display
│   └── admin.html            # Admin interface
├── static/
│   └── css/
│       └── custom.css        # Custom styling
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🎯 Usage

### Generating Picks

1. Go to http://localhost:8000/admin
2. Configure the weekly settings:
   - Year and Week Number
   - Date and Slate Description
   - Focus Games (all, afternoon_only, or specific games)
   - Min Articles for Sentiment
   - Include Long Shots checkbox
3. Click "Generate Picks"
4. Wait for OpenAI to generate (30-60 seconds)
5. View results on the Dashboard

### API Access

Get current picks as JSON:
```bash
curl http://localhost:8000/api/picks
```

Get current configuration:
```bash
curl http://localhost:8000/api/config
```

## 🔧 Configuration

All settings can be configured via environment variables or the admin interface:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *required* | Your OpenAI API key |
| `YEAR` | 2025 | NFL season year |
| `WEEK_NUMBER` | 13 | Week number (1-18) |
| `DATE` | 2025-11-30 | Date in YYYY-MM-DD format |
| `SLATE_DESCRIPTION` | Sunday main slate | Description of the slate |
| `NOTE` | Auto-generated | Note about data sources |
| `FOCUS_GAMES` | all | Game filter (see below) |
| `MIN_ARTICLES_FOR_SENTIMENT` | 3 | Min sources to aggregate |
| `INCLUDE_LONG_SHOTS` | true | Include long shot predictions |

### Focus Games Options

- `all` - All games in the slate
- `afternoon_only` - Only afternoon games
- `early_only` - Only early games
- `primetime_only` - Only primetime games
- `BUF @ PIT, NO @ MIA` - Comma-separated list of specific games

## 🚂 Railway Deployment

### One-Click Deploy

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/fantasy-weekly-ai-notes.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the configuration

3. **Set Environment Variables**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add `OPENAI_API_KEY` with your key
   - Add any other custom variables

4. **Deploy**
   - Railway will automatically deploy
   - Your app will be live at `https://your-app.railway.app`

### Manual Deployment

If you prefer manual deployment:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables
railway variables set OPENAI_API_KEY=your-key-here

# Deploy
railway up
```

## 🔄 Scheduled Updates (Optional)

To automatically generate picks weekly:

1. In Railway dashboard, go to your project
2. Click "Settings" → "Cron Jobs"
3. Add a new cron job:
   - Command: `python -c "from app.ai_client import generate_picks, save_picks; save_picks(generate_picks())"`
   - Schedule: `0 10 * * 3` (Every Wednesday at 10 AM)

## 📊 JSON Schema

The app generates JSON matching this exact schema:

```json
{
  "meta": {
    "week": 13,
    "date": "2025-11-30",
    "slate_description": "Sunday main slate",
    "note": "..."
  },
  "categories": {
    "qbs": [...],
    "rbs": [...],
    "wrs": [...],
    "tes": [...]
  },
  "long_shots": {
    "players": [...]
  }
}
```

Each player includes:
- Basic info (name, team, position, game)
- Matchup analysis
- Injury status
- Target stats
- Reasoning
- Sources with sentiment
- Prop suggestions (over/under or yes/no)

## 🎨 UI Customization

The UI uses Bootstrap 5 from CDN plus custom CSS in `static/css/custom.css`.

To customize:
1. Edit `custom.css` for styling changes
2. Edit templates for layout changes
3. Colors are defined in CSS variables

## 🐛 Troubleshooting

### "No picks generated yet"
- Go to `/admin` and generate picks
- Check that your OpenAI API key is set correctly

### OpenAI API errors
- Verify your API key is valid
- Check you have credits in your OpenAI account
- Ensure you're using a model that supports structured outputs (gpt-4o-2024-08-06)

### Import errors
- Make sure you're in the virtual environment
- Run `pip install -r requirements.txt` again

### Port already in use
- Change the port: `uvicorn app.main:app --port 8001`

## 📝 Development

### Adding New Features

1. **New API endpoint**: Add to `app/main.py`
2. **New page**: Create template in `templates/`
3. **New styling**: Add to `static/css/custom.css`
4. **New config**: Add to `app/config.py` and `.env.example`

### Testing

```bash
# Run the app
uvicorn app.main:app --reload

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/config
```

## 🔐 Security Notes

- Never commit `.env` file (it's in `.gitignore`)
- Keep your OpenAI API key secret
- Use Railway's environment variables for production
- The app has no authentication by default (add if needed)

## 📚 Tech Stack

- **Backend**: FastAPI + Python 3.8+
- **AI**: OpenAI GPT-4 with Structured Outputs
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Templating**: Jinja2
- **Deployment**: Railway
- **Data Validation**: Pydantic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and structured outputs
- Bootstrap team for the UI framework
- FastAPI team for the excellent framework
- Railway for easy deployment

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the code comments
- Open an issue on GitHub

---

**Built with ❤️ for fantasy football enthusiasts**