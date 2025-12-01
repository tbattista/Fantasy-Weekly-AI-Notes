# 🔧 Fix Git History - Remove Secret from Commit

GitHub detected a secret in commit `713b0325b8e7b3fff13152fe96caccb82b835d10`.

We need to rewrite the commit history to remove it.

## Option 1: Reset and Recommit (Easiest)

Since you're ahead by only 2 commits, we can reset and recommit:

```bash
# Go to project root
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Reset to before the problematic commits (keeps your changes)
git reset --soft HEAD~2

# Now recommit with the fixed files
git add dfs-picks-app/
git commit -m "Add DFS/Props Picks Generator app (secure)"

# Force push (this rewrites history)
git push --force origin main
```

## Option 2: Interactive Rebase (More Control)

```bash
# Go to project root
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Start interactive rebase for last 2 commits
git rebase -i HEAD~2

# In the editor that opens:
# - Change 'pick' to 'edit' for the commit with the secret
# - Save and close

# Now edit the file
# (The file is already fixed in your working directory)

# Stage the fixed file
git add dfs-picks-app/GIT_DEPLOY.md

# Amend the commit
git commit --amend --no-edit

# Continue the rebase
git rebase --continue

# Force push
git push --force origin main
```

## Option 3: Use GitHub's Allow Secret (Quick but Not Recommended)

GitHub provided a link to allow the secret:
https://github.com/tbattista/Fantasy-Weekly-AI-Notes/security/secret-scanning/unblock-secret/36Dc9swMfTBbLTQJJQTlXjZWZjD

**⚠️ NOT RECOMMENDED** - This would allow the secret to be pushed, which is a security risk.

## Recommended: Option 1 (Reset and Recommit)

This is the cleanest approach:

1. Resets the last 2 commits (keeps your files)
2. Recommits with the fixed GIT_DEPLOY.md
3. Force pushes the clean history

After this, your API key will not be in the Git history.

## After Fixing

Once pushed successfully:

1. **Rotate your API key** (recommended since it was in a commit)
   - Go to https://platform.openai.com/api-keys
   - Delete the old key
   - Create a new one
   - Update your local `.env` file
   - Update Railway environment variables

2. **Test locally** with the new key:
   ```bash
   cd dfs-picks-app
   run.bat
   ```

3. **Deploy to Railway** with the new key in environment variables