# 🚀 Project Restructuring Execution Plan

## 📋 Overview

This document outlines the exact steps to move `dfs-picks-app` contents to the root directory and remove all other files, while properly managing Git history.

## 🎯 Final Structure Goal

```
Fantasy Weekly AI Notes/ (root)
├── .env.example
├── .gitignore
├── .git/ (preserved)
├── Procfile
├── README.md
├── requirements.txt
├── railway.json
├── run.bat
├── setup.bat
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── ai_client.py
│   ├── data/
│   └── prompts/
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── admin.html
├── static/
│   └── css/
│       └── custom.css
└── (documentation files from dfs-picks-app)
```

## 📝 Step-by-Step Execution

### Phase 1: Git Cleanup (Critical First Step)

**⚠️ IMPORTANT: Must be done before file restructuring!**

```bash
# Navigate to project root
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# Check current status
git status

# Reset last 2 commits (keeps files, removes from history)
git reset --soft HEAD~2

# Stage all current files
git add .

# Create clean commit
git commit -m "Add DFS/Props Picks Generator (secure)"

# Force push to rewrite history
git push --force origin main
```

### Phase 2: File Restructuring

```bash
# Create backup of dfs-picks-app (safety)
cp -r dfs-picks-app dfs-picks-app-backup

# Remove all root files/folders except .git and dfs-picks-app
# On Windows:
del /Q *.md *.html *.js *.css *.json *.sh *.bat
rmdir /S /Q data New sneat-bootstrap-template .github

# Move contents from dfs-picks-app to root
# On Windows:
xcopy /E /I dfs-picks-app\* .
rmdir /S /Q dfs-picks-app

# Verify structure
dir
```

### Phase 3: Verification & Testing

```bash
# Check Python app structure
dir app\
dir templates\
dir static\

# Test app locally
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Test in browser: http://localhost:8000
```

### Phase 4: Git Commit of New Structure

```bash
# Stage restructured files
git add .

# Commit the restructuring
git commit -m "Restructure: Move dfs-picks-app to root directory"

# Push to GitHub
git push origin main
```

## 🔧 Detailed Windows Commands

### Remove Root Files (Windows CMD)
```cmd
# Remove markdown files
del *.md

# Remove HTML/JS/CSS files
del *.html *.js *.css

# Remove JSON files
del *.json

# Remove batch/shell scripts
del *.bat *.sh

# Remove directories
rmdir /S /Q data
rmdir /S /Q New
rmdir /S /Q sneat-bootstrap-template
rmdir /S /Q .github
```

### Move dfs-picks-app Contents (Windows CMD)
```cmd
# Copy all contents including subdirectories
xcopy /E /I /Y dfs-picks-app\* .

# Remove the now-empty dfs-picks-app folder
rmdir /S /Q dfs-picks-app
```

## ⚠️ Critical Considerations

### 1. Git History
- Must clean Git history BEFORE file restructuring
- Use `--force` push to rewrite history
- This removes any sensitive data from commit history

### 2. File Preservation
- Backup dfs-picks-app before restructuring
- Preserve .git directory
- Ensure all app files are moved correctly

### 3. Path References
- Check for any hardcoded paths in Python files
- Update any configuration that references old structure
- Verify import statements still work

### 4. Railway Deployment
- Update Railway root directory setting
- Verify environment variables are still correct
- Test deployment after restructuring

## 🧪 Verification Checklist

### File Structure Verification
- [ ] All dfs-picks-app contents are in root
- [ ] No dfs-picks-app folder remains
- [ ] .git directory preserved
- [ ] All old root files removed

### Functionality Verification
- [ ] Python imports work correctly
- [ ] Templates load properly
- [ ] Static files are accessible
- [ ] App runs locally without errors
- [ ] Dashboard displays correctly
- [ ] Admin interface works

### Git Verification
- [ ] Git history is clean
- [ ] New structure committed
- [ ] Pushed to GitHub successfully
- [ ] Railway can deploy from new structure

## 🔄 Rollback Plan

If anything goes wrong:

```bash
# Restore from backup
rmdir /S /Q *
xcopy /E /I dfs-picks-app-backup\* .
rmdir /S /Q dfs-picks-app-backup

# Or reset Git to before restructuring
git log --oneline
git reset --hard <commit-hash-before-restructuring>
```

## 📞 Next Steps After Restructuring

1. **Update Railway Configuration**
   - Set root directory to `/` (instead of `/dfs-picks-app`)
   - Verify environment variables
   - Test deployment

2. **Update Documentation**
   - Update README.md with new structure
   - Update any path references in docs
   - Simplify setup instructions

3. **Final Testing**
   - Deploy to Railway
   - Test all functionality
   - Verify API endpoints work

---

**Ready to execute?** Follow the steps in order and verify each phase before proceeding to the next.