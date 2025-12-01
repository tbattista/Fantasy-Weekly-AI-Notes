# 🎯 Project Restructuring & Git Cleanup Plan

## 📋 Current Situation

**Root Directory (Static Viewer):**
- `index.html` - Beautiful player card viewer
- `data/` - JSON files with player data
- `sneat-bootstrap-template/` - UI framework

**`dfs-picks-app/` Subdirectory (Python AI Generator):**
- FastAPI backend with OpenAI integration
- Templates with similar viewer functionality
- Admin interface for generating picks
- Deployment configuration

**Git Issue:** GitHub blocking push due to `sk-proj-...` pattern in `dfs-picks-app/GIT_DEPLOY.md` line 92

---

## 🎯 Proposed New Structure

```
Fantasy-Weekly-AI-Notes/  (root)
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py
│   ├── models.py
│   ├── ai_client.py
│   ├── prompts/
│   │   └── weekly_picks.txt
│   └── data/
│       └── .gitkeep
│
├── templates/
│   ├── base.html
│   ├── dashboard.html       # Merged viewer (combines both)
│   └── admin.html
│
├── static/
│   └── css/
│       └── custom.css       # Player card styles
│
├── data/                    # Keep existing JSON files
│   ├── 11-30.json
│   └── 11-30-afternoon.json
│
├── sneat-bootstrap-template/ # Keep as-is
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Procfile
├── railway.json
├── README.md                # Updated comprehensive guide
└── DEPLOYMENT.md            # Sanitized deployment guide
```

---

## 🔧 Step-by-Step Execution Plan

### **Phase 1: Git History Cleanup** (CRITICAL - Do First)

**Problem:** GitHub detected `sk-proj-...` pattern in `dfs-picks-app/GIT_DEPLOY.md` line 92

**Commands to Execute:**

```bash
# 1. Navigate to project root
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

# 2. First, we'll sanitize the problematic file (done via tool)

# 3. Reset the last 2 commits (keeps files)
git reset --soft HEAD~2

# 4. Stage all files
git add .

# 5. Create new clean commit
git commit -m "Add DFS/Props Picks Generator (restructured and secure)"

# 6. Force push to rewrite history
git push --force origin main
```

**Files to Sanitize:**
- `dfs-picks-app/GIT_DEPLOY.md` - Change line 92 from `sk-proj-...` to `sk-YOUR_KEY_HERE`

---

### **Phase 2: Project Restructuring**

#### **2A: Move Core App Files**

```bash
# Move Python app to root
mv dfs-picks-app/app ./app
mv dfs-picks-app/templates ./templates
mv dfs-picks-app/static ./static

# Move config files to root
mv dfs-picks-app/.env.example ./.env.example
mv dfs-picks-app/requirements.txt ./requirements.txt
mv dfs-picks-app/Procfile ./Procfile
mv dfs-picks-app/railway.json ./railway.json

# Update .gitignore
mv dfs-picks-app/.gitignore ./.gitignore
```

#### **2B: Clean Up Old Files**

```bash
# Remove old documentation with secrets
rm dfs-picks-app/GIT_DEPLOY.md
rm dfs-picks-app/FIX_GIT_HISTORY.md

# Archive planning docs (optional)
mkdir -p archive
mv dfs-picks-app/ARCHITECTURE_PLAN.md archive/
mv dfs-picks-app/SIMPLIFIED_PLAN.md archive/

# Remove old README (will create new one)
rm dfs-picks-app/README.md

# Remove empty dfs-picks-app directory
rm -rf dfs-picks-app/
```

#### **2C: Update Root Files**

- Create new `README.md` - Comprehensive guide
- Create new `DEPLOYMENT.md` - Sanitized deployment instructions
- Update `templates/dashboard.html` - Add file selector for historical data
- Remove old `index.html` (replaced by dashboard)

---

### **Phase 3: Update Application Code**

#### **Update `app/main.py`**

Add route to serve static JSON files:

```python
@app.get("/api/data/{filename}")
async def get_data_file(filename: str):
    """Serve static JSON files from data/ folder"""
    from pathlib import Path
    import json
    
    file_path = Path("data") / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")
    return JSONResponse(content=json.loads(file_path.read_text()))

@app.get("/api/data")
async def list_data_files():
    """List available JSON files in data/ folder"""
    from pathlib import Path
    
    data_dir = Path("data")
    files = [f.name for f in data_dir.glob("*.json")]
    return JSONResponse(content={"files": files})
```

#### **Update `templates/dashboard.html`**

Add file selector to switch between AI picks and historical data:

```html
<select id="data-source" class="form-select">
    <option value="ai">AI Generated Picks (Current)</option>
    <option value="11-30.json">Historical: 11-30.json</option>
    <option value="11-30-afternoon.json">Historical: 11-30-afternoon.json</option>
</select>
```

---

## 🔐 Security Fixes

### **Sanitization Changes**

**In `dfs-picks-app/GIT_DEPLOY.md` line 92:**
- ❌ OLD: `4. Copy the key (starts with `sk-proj-...`)`
- ✅ NEW: `4. Copy the key (starts with `sk-` followed by your unique key)`

**In new `DEPLOYMENT.md`:**
- Use `[YOUR_API_KEY]` or `your-openai-api-key` as placeholders
- Never include actual key patterns like `sk-proj-`

### **API Key Rotation (Recommended)**

Since the key pattern was in a commit:
1. Go to https://platform.openai.com/api-keys
2. Delete the old key (if it was real)
3. Create a new key
4. Update local `.env` file
5. Update Railway environment variables

---

## 📊 Migration Checklist

### ✅ Files to Keep (Move to Root)
- [x] `app/` directory
- [x] `templates/` directory  
- [x] `static/` directory
- [x] `requirements.txt`
- [x] `Procfile`
- [x] `railway.json`
- [x] `.env.example`
- [x] `.gitignore`

### ✅ Files to Keep (Already in Root)
- [x] `data/` folder with JSON files
- [x] `sneat-bootstrap-template/`

### ❌ Files to Delete
- [ ] `dfs-picks-app/GIT_DEPLOY.md` (has secret pattern)
- [ ] `dfs-picks-app/FIX_GIT_HISTORY.md` (no longer needed)
- [ ] `dfs-picks-app/QUICKSTART.md` (will merge into new README)
- [ ] `dfs-picks-app/` directory (after moving contents)
- [ ] Root `index.html` (replaced by dashboard)

### 📝 Files to Create
- [ ] New `README.md` (comprehensive guide)
- [ ] New `DEPLOYMENT.md` (sanitized)
- [ ] Updated `templates/dashboard.html` (with file selector)

---

## 🎨 Dashboard Enhancement

The new dashboard will have:

**Data Source Selector:**
- AI Picks (Current Week) - from `/api/picks`
- Historical Data - from `/api/data/{filename}`
- Same beautiful card layout for both

**Benefits:**
- One unified interface
- View AI picks OR historical data
- Keep your beautiful card design
- Admin can generate new picks

---

## ⚡ Execution Order

1. **Sanitize Files** ✅ (First - fixes Git issue)
2. **Git Cleanup** (Reset commits, force push)
3. **Move Files** (Restructure to root)
4. **Update Code** (Add new routes)
5. **Create Docs** (New README, DEPLOYMENT)
6. **Test Locally** (Verify everything works)
7. **Commit & Push** (Clean history)
8. **Deploy** (Railway)

---

## 🤔 Questions Before Proceeding

1. **Archive planning docs?** Keep ARCHITECTURE_PLAN.md in `archive/` folder?
2. **Keep old index.html?** Or fully replace with FastAPI dashboard?
3. **Proceed now?** Should I start executing the plan?

---

## 📞 Next Steps

Once approved, I will:
1. Sanitize `GIT_DEPLOY.md` to remove secret pattern
2. Provide exact Git commands to clean history
3. Create migration scripts for file moves
4. Generate new documentation files
5. Update application code
6. Test and verify

**Ready to proceed when you give the go-ahead!**