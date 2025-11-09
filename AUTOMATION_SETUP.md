# 🤖 Automated Weekly Data Updates

This guide explains how to set up automatic weekly data generation and deployment every Saturday at 7 AM EST.

---

## 🎯 Architecture Overview

```
GitHub Actions (Cron Job)
    ↓
OpenAI API (Generate Data)
    ↓
Commit to GitHub
    ↓
Railway Auto-Deploy
    ↓
Live Dashboard Updated
```

---

## 📋 What You Need

### 1. OpenAI API Access
- **API Key**: From https://platform.openai.com/api-keys
- **Model**: GPT-4 or GPT-4-turbo (recommended for data accuracy)
- **Cost**: ~$0.10-0.50 per week (depending on data complexity)

### 2. GitHub Secrets
- Store your OpenAI API key securely in GitHub
- No code changes needed - all in GitHub settings

### 3. No Railway Changes Needed
- ✅ Railway already auto-deploys from GitHub
- ✅ No database required (static JSON files)
- ✅ No additional Railway services needed

---

## 🔧 Setup Instructions

### Step 1: Get OpenAI API Key

1. **Go to OpenAI**: https://platform.openai.com/api-keys
2. **Create new key**: Click "Create new secret key"
3. **Name it**: "Fantasy-Weekly-Automation"
4. **Copy the key**: Save it securely (you'll only see it once)
5. **Add billing**: Ensure you have credits/payment method set up

**Expected Cost**: $0.10-0.50 per week for data generation

### Step 2: Add GitHub Secret

1. **Go to your repository**: https://github.com/tbattista/weekly-fantay
2. **Click**: Settings → Secrets and variables → Actions
3. **Click**: "New repository secret"
4. **Add secret**:
   - Name: `OPENAI_API_KEY`
   - Value: [paste your OpenAI API key]
5. **Click**: "Add secret"

### Step 3: Create GitHub Actions Workflow

I'll create the automation file that runs every Saturday at 7 AM EST.

---

## 📁 Required Files

### File 1: `.github/workflows/weekly-update.yml`
GitHub Actions workflow that runs on schedule

### File 2: `scripts/generate-weekly-data.js`
Node.js script that calls OpenAI API to generate data

### File 3: `scripts/package.json`
Dependencies for the automation script

---

## ⚙️ How It Works

### Every Saturday at 7 AM EST:

1. **GitHub Actions triggers** the workflow
2. **Script calculates** current NFL week and date
3. **OpenAI API called** with your data generation prompt
4. **JSON validated** for correctness
5. **File saved** to `data/week{X}-data.json`
6. **Git commit** created automatically
7. **Pushed to GitHub** (triggers Railway deployment)
8. **Railway deploys** new version (2-5 minutes)
9. **Dashboard updated** with fresh data

### Manual Override Available:
- You can still manually update data anytime
- Workflow can be triggered manually from GitHub Actions tab
- Automation can be paused by disabling the workflow

---

## 🔐 Security

### API Key Protection
- ✅ Stored as GitHub Secret (encrypted)
- ✅ Never exposed in code or logs
- ✅ Only accessible to GitHub Actions
- ✅ Can be rotated anytime

### Access Control
- ✅ Only your GitHub account can modify workflow
- ✅ OpenAI API key scoped to your account
- ✅ Railway deployment requires GitHub authentication

---

## 💰 Cost Breakdown

### OpenAI API Costs
- **Model**: GPT-4-turbo
- **Input tokens**: ~2,000 tokens (prompt)
- **Output tokens**: ~8,000 tokens (JSON data)
- **Cost per run**: ~$0.10-0.50
- **Weekly cost**: ~$0.10-0.50
- **Monthly cost**: ~$0.40-2.00

### Railway Costs
- **Current**: Free tier ($5/month credit)
- **Your usage**: ~$0.50-2/month
- **Total**: Within free tier ✅

### Total Monthly Cost
- **OpenAI**: $0.40-2.00
- **Railway**: $0 (free tier)
- **Total**: $0.40-2.00/month

---

## 🎛️ Configuration Options

### Customize Schedule

Edit `.github/workflows/weekly-update.yml`:

```yaml
schedule:
  - cron: '0 12 * * 6'  # Saturday 7 AM EST (12 PM UTC)
```

Change to different times:
- `'0 11 * * 6'` = Saturday 6 AM EST
- `'0 13 * * 6'` = Saturday 8 AM EST
- `'0 12 * * 5'` = Friday 7 AM EST

### Customize Data Generation

Edit `scripts/generate-weekly-data.js` to:
- Change OpenAI model (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
- Adjust temperature for creativity
- Modify prompt for different data focus
- Add validation rules

---

## 🧪 Testing

### Test Locally (Before Automation)

```bash
# Install dependencies
cd scripts
npm install

# Set environment variable
export OPENAI_API_KEY="your-key-here"

# Run script manually
node generate-weekly-data.js

# Check output
cat ../data/week11-data.json
```

### Test GitHub Action

1. Go to: https://github.com/tbattista/weekly-fantay/actions
2. Click: "Weekly Data Update" workflow
3. Click: "Run workflow" button
4. Select: main branch
5. Click: "Run workflow"
6. Monitor: Workflow execution in real-time

---

## 📊 Monitoring

### Check Workflow Status

1. **GitHub Actions Tab**: https://github.com/tbattista/weekly-fantay/actions
2. **View runs**: See all automated updates
3. **Check logs**: Debug any issues
4. **Email notifications**: GitHub sends alerts on failures

### Verify Data Quality

After each automated run:
1. Check GitHub commit history
2. Review generated JSON file
3. Visit dashboard to verify display
4. Check Railway deployment logs

---

## 🚨 Troubleshooting

### Workflow Fails

**Check**:
1. OpenAI API key is valid
2. API has sufficient credits
3. GitHub Actions logs for error messages
4. JSON validation passed

**Fix**:
- Rotate API key if expired
- Add credits to OpenAI account
- Review and fix script errors
- Manually generate data as backup

### Data Quality Issues

**Check**:
1. OpenAI response completeness
2. JSON structure matches schema
3. All required fields populated
4. Sources cited properly

**Fix**:
- Adjust prompt for better results
- Increase temperature for creativity
- Add validation rules to script
- Manually review and edit JSON

### Railway Deployment Issues

**Check**:
1. Git commit was successful
2. Railway detected the change
3. Build logs for errors
4. Dashboard displays new data

**Fix**:
- Verify git push succeeded
- Check Railway webhook is active
- Review build logs
- Hard refresh browser (Ctrl+Shift+R)

---

## 🔄 Maintenance

### Weekly
- ✅ Automated - no action needed
- Monitor GitHub Actions for success
- Spot-check data quality

### Monthly
- Review OpenAI API usage and costs
- Check Railway deployment metrics
- Update prompt if data quality declines

### Seasonally
- Update NFL schedule for new season
- Adjust week number calculations
- Review and improve automation

---

## 🎯 Next Steps

1. **Get OpenAI API Key** (5 minutes)
2. **Add GitHub Secret** (2 minutes)
3. **I'll create the automation files** (next step)
4. **Test the workflow** (5 minutes)
5. **Enable automation** (1 minute)

**Total setup time**: ~15 minutes

---

## ✅ Benefits of Automation

- ✅ **Hands-free updates**: No manual work each week
- ✅ **Consistent timing**: Always ready Saturday morning
- ✅ **Fresh data**: Latest lines, weather, injuries
- ✅ **Reliable**: Runs even if you're busy/away
- ✅ **Auditable**: Full history in GitHub
- ✅ **Flexible**: Can override manually anytime

---

## 📞 Support

### OpenAI Issues
- **Documentation**: https://platform.openai.com/docs
- **API Status**: https://status.openai.com
- **Support**: https://help.openai.com

### GitHub Actions Issues
- **Documentation**: https://docs.github.com/actions
- **Community**: https://github.community

### Railway Issues
- **Documentation**: https://docs.railway.app
- **Discord**: https://discord.gg/railway

---

**Ready to automate? Let's create the automation files!**

Once you provide your OpenAI API key and add it to GitHub Secrets, I'll create the automation scripts that will handle everything automatically every Saturday at 7 AM EST.