# 🚂 Railway Deployment Fix

## ✅ Problem 1: SOLVED - Root Directory

You've successfully set the Root Directory to `dfs-picks-app`. Railway is now deploying the Python app!

## ❌ Problem 2: CURRENT - Missing Environment Variables

**Error:** `Field required [type=missing, input_value={}, input_type=dict]`

**Cause:** The `OPENAI_API_KEY` environment variable is not set in Railway.

## Solution: Add Environment Variables in Railway

### Via Railway Dashboard (REQUIRED NOW)

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Click on your "Fantasy-Weekly-AI-Notes" project

2. **Click on Your Service**
   - Click on the service card

3. **Go to Variables Tab**
   - Click the **Variables** tab at the top

4. **Add Required Variables**
   
   Click **+ New Variable** for each of these:

   **REQUIRED (App won't start without this):**
   ```
   OPENAI_API_KEY = your-actual-openai-api-key-here
   ```
   Get your key from: https://platform.openai.com/api-keys

   **OPTIONAL (Have defaults but you can customize):**
   ```
   YEAR = 2025
   WEEK_NUMBER = 13
   DATE = 2025-11-30
   SLATE_DESCRIPTION = Sunday main slate
   FOCUS_GAMES = all
   MIN_ARTICLES_FOR_SENTIMENT = 3
   INCLUDE_LONG_SHOTS = true
   ```

5. **Save and Redeploy**
   - Railway will automatically redeploy after you add variables
   - Wait 1-2 minutes for the deployment to complete

### Option 2: Via Railway CLI

```bash
# Navigate to project
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Link to Railway project
railway link

# Set root directory
railway service --root dfs-picks-app

# Redeploy
railway up
```

---

## Why This Happened

Your repository structure:
```
Fantasy-Weekly-AI-Notes/
├── index.html              ← Railway deployed THIS (static site)
├── data/
├── sneat-bootstrap-template/
└── dfs-picks-app/          ← You want THIS (Python app)
    ├── app/
    ├── templates/
    ├── requirements.txt
    └── Procfile
```

Railway defaults to the root directory and found `index.html`, so it deployed that as a static site.

---

## Alternative: Move Everything to Root (Better Long-term)

This is why we planned the restructuring! Once we move the Python app to root:

```
Fantasy-Weekly-AI-Notes/
├── app/                    ← Python app at root
├── templates/
├── static/
├── requirements.txt
├── Procfile
└── data/
```

Then Railway will automatically detect and deploy the Python app correctly.

---

## Quick Fix Now

**Do this in Railway Dashboard:**
1. Settings → Root Directory → `dfs-picks-app`
2. Save
3. Wait for redeploy (1-2 minutes)
4. Refresh your browser

**Then you'll see the FastAPI app instead of the static site!**

---

## After This Works

Once Railway is deploying correctly from `dfs-picks-app/`, we can proceed with the full restructuring to move everything to root for a cleaner setup.