# 🔧 Git History Cleanup Commands

## ⚠️ CRITICAL: Run These Commands Now

The file `dfs-picks-app/GIT_DEPLOY.md` has been sanitized to remove the secret pattern.

Now you need to clean the Git history and push the fixed version.

---

## 📋 Step-by-Step Commands

### Step 1: Verify You're in the Right Directory

```bash
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"
pwd
# Should show: c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes
```

### Step 2: Check Current Git Status

```bash
git status
# You should see modified: dfs-picks-app/GIT_DEPLOY.md
```

### Step 3: Reset Last 2 Commits (Keeps Your Files)

```bash
git reset --soft HEAD~2
```

**What this does:**
- Removes the last 2 commits from history
- Keeps all your files exactly as they are
- Stages all changes for a new commit

### Step 4: Stage All Files

```bash
git add .
```

### Step 5: Create New Clean Commit

```bash
git commit -m "Add DFS/Props Picks Generator (secure)"
```

### Step 6: Force Push to Rewrite History

```bash
git push --force origin main
```

**⚠️ Important:** This rewrites Git history. The old commits with the secret pattern will be gone.

---

## ✅ Verification

After pushing, verify success:

```bash
# Check that push succeeded
git log --oneline -3

# You should see your new commit at the top
# The old commits with the secret should be gone
```

---

## 🔐 Security Recommendation

Since the API key pattern was in a commit (even briefly), it's recommended to rotate your OpenAI API key:

1. **Go to:** https://platform.openai.com/api-keys
2. **Delete** the old key (if it was a real key)
3. **Create** a new secret key
4. **Update** your local `.env` file with the new key
5. **Update** Railway environment variables with the new key

---

## 🚨 If Push Still Fails

If GitHub still blocks the push, it might be caching. Try:

```bash
# Clear any cached credentials
git credential-cache exit

# Try push again
git push --force origin main
```

Or use GitHub's "Allow Secret" link (NOT RECOMMENDED):
https://github.com/tbattista/Fantasy-Weekly-AI-Notes/security/secret-scanning/unblock-secret/36Dc9swMfTBbLTQJJQTlXjZWZjD

**Note:** Only use the "Allow Secret" option if you're absolutely sure the key in the commit was fake/example text.

---

## 📞 Next Steps After Successful Push

Once the push succeeds, we'll proceed with:
1. Moving files from `dfs-picks-app/` to root
2. Updating application code
3. Creating new documentation
4. Testing the restructured app

---

## 🚂 Optional: Railway CLI Setup

If you want to deploy to Railway using the CLI, here are the commands:

### Install Railway CLI

```bash
# Install Railway CLI globally
npm install -g @railway/cli
```

### Login to Railway

```bash
railway login
```

This will open your browser to authenticate.

### Link to Your Project

```bash
# Navigate to your project directory
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Link to existing Railway project (or create new one)
railway link
```

### Set Environment Variables via CLI

```bash
# Set your OpenAI API key
railway variables set OPENAI_API_KEY=your-actual-key-here

# Set other configuration variables
railway variables set YEAR=2025
railway variables set WEEK_NUMBER=13
railway variables set DATE=2025-11-30
railway variables set SLATE_DESCRIPTION="Sunday main slate"
railway variables set FOCUS_GAMES=all
railway variables set MIN_ARTICLES_FOR_SENTIMENT=3
railway variables set INCLUDE_LONG_SHOTS=true
```

### Deploy to Railway

```bash
# Deploy your app
railway up
```

### View Logs

```bash
# Watch live logs
railway logs
```

### Open Your App

```bash
# Open deployed app in browser
railway open
```

---

**Run these commands now and let me know the result!**