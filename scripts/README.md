# 🤖 Automation Scripts

This directory contains scripts for automated weekly NFL data generation.

## Files

- **`generate-weekly-data.js`** - Main script that calls OpenAI API to generate weekly data
- **`get-current-week.js`** - Calculates current NFL week based on date
- **`package.json`** - Node.js dependencies

## Setup

### 1. Install Dependencies

```bash
cd scripts
npm install
```

### 2. Set Environment Variable

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Run Manually

```bash
node generate-weekly-data.js
```

## Automated Execution

The GitHub Actions workflow (`.github/workflows/weekly-update.yml`) runs this script automatically every Saturday at 7 AM EST.

## Configuration

### Change NFL Season Start Date

Edit `get-current-week.js`:

```javascript
const seasonStart = new Date('2025-09-04T00:00:00-05:00');
```

### Change OpenAI Model

Edit `generate-weekly-data.js`:

```javascript
model: 'gpt-4-turbo', // or 'gpt-4', 'gpt-3.5-turbo'
```

### Adjust Temperature

Edit `generate-weekly-data.js`:

```javascript
temperature: 0.3, // 0.0-1.0 (lower = more consistent)
```

## Testing

Test locally before automation:

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Run script
node generate-weekly-data.js

# Check output
cat ../data/week11-data.json
```

## Troubleshooting

### API Key Error

```
❌ Error: OPENAI_API_KEY environment variable not set
```

**Fix**: Set the environment variable or add to GitHub Secrets

### JSON Parse Error

```
❌ Error generating weekly data: Unexpected token
```

**Fix**: OpenAI response may include markdown. The script attempts to clean it automatically.

### Validation Warnings

```
⚠️  Validation warnings:
   - Insufficient sources: 8 (minimum 10 recommended)
```

**Fix**: These are warnings, not errors. Data will still be saved. Adjust prompt if needed.

## Cost Estimation

- **Model**: GPT-4-turbo
- **Tokens per run**: ~10,000 tokens
- **Cost per run**: ~$0.10-0.50
- **Weekly cost**: ~$0.10-0.50
- **Monthly cost**: ~$0.40-2.00

## Support

See [`AUTOMATION_SETUP.md`](../AUTOMATION_SETUP.md) for full documentation.