# 🚀 Git & Railway Deployment Guide

Since your repo is already initialized and connected, here's how to deploy the new app:

## Step 1: Commit the New App

```bash
# Make sure you're in the project root
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Add all the new dfs-picks-app files
git add dfs-picks-app/

# Commit
git commit -m "Add DFS/Props Picks Generator app with OpenAI structured outputs"

# Push to GitHub
git push origin main
```

## Step 2: Deploy to Railway

### Option A: New Railway Project for This App

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Set **Root Directory** to: `dfs-picks-app`
6. Railway will auto-detect the configuration

### Option B: Add to Existing Railway Project

If you already have a Railway project:

1. Go to your Railway dashboard
2. Click your project
3. Click "New Service" → "GitHub Repo"
4. Select your repository
5. Set **Root Directory** to: `dfs-picks-app`

## Step 3: Configure Environment Variables in Railway

⚠️ **IMPORTANT**: Never commit your API key to Git! The `.env` file is gitignored.

### Detailed Steps to Add Variables:

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Log in to your account

2. **Select Your Project**
   - Click on the project where you deployed the app
   - You'll see your service listed

3. **Open Service Settings**
   - Click on your service (it will show the app name)
   - You'll see tabs at the top: Deployments, Metrics, Settings, etc.

4. **Go to Variables Tab**
   - Click the "Variables" tab (or "Settings" → "Variables")
   - You'll see a section to add environment variables

5. **Add Each Variable**
   - Click "+ New Variable" button
   - For each variable below, enter:
     - **Variable Name** (left field): `OPENAI_API_KEY`
     - **Value** (right field): Your actual API key
   - Click "Add" or press Enter

6. **Required Variables to Add:**
   ```
   OPENAI_API_KEY = [Get from https://platform.openai.com/api-keys]
   YEAR = 2025
   WEEK_NUMBER = 13
   DATE = 2025-11-30
   SLATE_DESCRIPTION = Sunday main slate
   FOCUS_GAMES = all
   MIN_ARTICLES_FOR_SENTIMENT = 3
   INCLUDE_LONG_SHOTS = true
   ```

7. **Save and Redeploy**
   - Railway will automatically redeploy with the new variables
   - Wait for deployment to complete (usually 1-2 minutes)

### Where to Get Your OpenAI API Key:

1. Go to https://platform.openai.com/api-keys
2. Log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-` followed by your unique key)
5. Paste it into Railway's `OPENAI_API_KEY` variable

### Alternative: Use Railway CLI

If you prefer command line:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Add variables (get your API key from OpenAI first!)
railway variables set OPENAI_API_KEY=[paste-your-key-here]
railway variables set YEAR=2025
railway variables set WEEK_NUMBER=13
railway variables set DATE=2025-11-30
railway variables set SLATE_DESCRIPTION="Sunday main slate"
railway variables set FOCUS_GAMES=all
railway variables set MIN_ARTICLES_FOR_SENTIMENT=3
railway variables set INCLUDE_LONG_SHOTS=true
```

## Step 4: Deploy!

Railway will automatically:
- Detect Python
- Install dependencies from `requirements.txt`
- Use the `Procfile` to start the app
- Assign a public URL

Your app will be live at: `https://your-app-name.railway.app`

## 🔄 Future Updates

To update the app after making changes:

```bash
# Make your changes
# Then commit and push
git add dfs-picks-app/
git commit -m "Update: description of changes"
git push origin main
```

Railway will automatically redeploy!

## 📝 Important Notes

- The `.env` file is gitignored (won't be pushed to GitHub)
- Your API key is safe - only set it in Railway's environment variables
- Railway uses the `Procfile` to know how to start the app
- The `railway.json` provides additional configuration

## 🐛 Troubleshooting

### Build fails on Railway
- Check that Root Directory is set to `dfs-picks-app`
- Verify all environment variables are set
- Check Railway logs for specific errors

### App starts but crashes
- Verify OPENAI_API_KEY is set correctly
- Check Railway logs: `railway logs`

### Can't access the app
- Make sure Railway assigned a public domain
- Check if the service is running in Railway dashboard

---

**Ready to deploy?** Just commit and push, then set up Railway!