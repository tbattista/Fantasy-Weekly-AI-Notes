# 🚂 Railway CLI Setup Guide

## Quick Setup via Batch Script

I've created [`railway-setup.bat`](railway-setup.bat:1) to automate the entire process!

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Run the Setup Script

```bash
# Just double-click the file or run:
railway-setup.bat
```

The script will:
1. ✅ Check if Railway CLI is installed
2. ✅ Login to Railway (opens browser)
3. ✅ Link to your project
4. ✅ Prompt for your OpenAI API key
5. ✅ Set all environment variables
6. ✅ Trigger automatic redeploy

---

## Manual CLI Commands (Alternative)

If you prefer to run commands manually:

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login to Railway

```bash
railway login
```

This opens your browser to authenticate.

### 3. Navigate to Project

```bash
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"
```

### 4. Link to Railway Project

```bash
railway link
```

Select your "Fantasy-Weekly-AI-Notes" project from the list.

### 5. Set Environment Variables

```bash
# REQUIRED - Replace with your actual key
railway variables set OPENAI_API_KEY=sk-your-actual-key-here

# OPTIONAL - Defaults provided
railway variables set YEAR=2025
railway variables set WEEK_NUMBER=13
railway variables set DATE=2025-11-30
railway variables set SLATE_DESCRIPTION="Sunday main slate"
railway variables set FOCUS_GAMES=all
railway variables set MIN_ARTICLES_FOR_SENTIMENT=3
railway variables set INCLUDE_LONG_SHOTS=true
```

### 6. Verify Variables

```bash
railway variables
```

This shows all set variables.

### 7. Watch Deployment

```bash
railway logs
```

Watch the logs to see your app starting up.

### 8. Open Your App

```bash
railway open
```

Opens your deployed app in the browser.

---

## Troubleshooting

### "Railway CLI not found"

Install it:
```bash
npm install -g @railway/cli
```

### "Not logged in"

Run:
```bash
railway login
```

### "No project linked"

Run:
```bash
railway link
```

Then select your project from the list.

### "Variables not taking effect"

Railway automatically redeploys when you set variables. Wait 1-2 minutes.

Check deployment status:
```bash
railway status
```

---

## After Variables Are Set

Once all variables are set, Railway will automatically redeploy your app.

**Expected result:**
- App starts successfully
- No more "Field required" errors
- FastAPI dashboard loads at your Railway URL

**Check it worked:**
```bash
# View logs
railway logs

# Open app
railway open
```

You should see the FastAPI app with:
- Dashboard at `/`
- Admin panel at `/admin`
- API at `/api/picks`

---

## Next Steps

Once the app is running successfully:
1. ✅ Test the dashboard
2. ✅ Go to `/admin` and generate picks
3. ✅ View the generated picks on the dashboard
4. 🎯 Consider restructuring to move files to root (optional)