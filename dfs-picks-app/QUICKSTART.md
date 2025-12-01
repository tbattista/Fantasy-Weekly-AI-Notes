# 🚀 Quick Start Guide

Get your DFS/Props Picks app running in 5 minutes!

## Step 1: Easy Setup (Windows)

**Option A: Automated Setup (Recommended)**
```bash
cd dfs-picks-app
setup.bat
```
This will create the virtual environment, install dependencies, and start the app!

**Option B: Manual Setup**
```bash
cd dfs-picks-app
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**For Mac/Linux:**
```bash
cd dfs-picks-app
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 2: Verify Configuration

Your `.env` file is already set up with your OpenAI API key. You can edit it if needed:

```bash
# Edit .env to change any settings
notepad .env  # Windows
nano .env     # Mac/Linux
```

## Step 3: Run the App

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
venv\Scripts\activate
uvicorn app.main:app --reload
```

**Mac/Linux:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 4: Generate Your First Picks

1. Open http://localhost:8000/admin in your browser
2. Review the configuration (defaults are already set)
3. Click "Generate Picks" button
4. Wait 30-60 seconds for OpenAI to generate
5. View results at http://localhost:8000

## 🎯 What's Next?

### View Your Picks
- **Dashboard**: http://localhost:8000
- **API**: http://localhost:8000/api/picks
- **Admin**: http://localhost:8000/admin

### Customize Settings
Edit any of these in the Admin page:
- Week number and date
- Focus games (all, afternoon_only, or specific games)
- Include/exclude long shots
- Minimum articles for sentiment

### Deploy to Production
See [README.md](README.md#-railway-deployment) for Railway deployment instructions.

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the virtual environment
# You should see (venv) in your terminal prompt
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Use a different port
uvicorn app.main:app --port 8001
```

### OpenAI API errors
- Check your API key in `.env`
- Verify you have credits in your OpenAI account
- Visit https://platform.openai.com/account/billing

## 📚 Learn More

- Full documentation: [README.md](README.md)
- Architecture details: [ARCHITECTURE_PLAN.md](ARCHITECTURE_PLAN.md)
- Simplified approach: [SIMPLIFIED_PLAN.md](SIMPLIFIED_PLAN.md)

---

**Need help?** Check the README or open an issue on GitHub.