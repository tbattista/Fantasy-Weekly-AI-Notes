#!/bin/bash
# Railway Environment Variables Setup Script
# Run this after installing Railway CLI: npm install -g @railway/cli

echo "========================================"
echo "Railway Environment Variables Setup"
echo "========================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "ERROR: Railway CLI not found!"
    echo ""
    echo "Please install it first:"
    echo "npm install -g @railway/cli"
    echo ""
    exit 1
fi

echo "Railway CLI found!"
echo ""

# Navigate to project directory
cd "c:/Users/user/iCloudDrive/PARA/1 - Projects/_Websites/Fantasy Weekly AI Notes"

echo "Current directory: $(pwd)"
echo ""

# Login to Railway (if not already logged in)
echo "Step 1: Logging in to Railway..."
railway login
if [ $? -ne 0 ]; then
    echo "ERROR: Railway login failed!"
    exit 1
fi
echo ""

# Link to project (if not already linked)
echo "Step 2: Linking to Railway project..."
railway link
if [ $? -ne 0 ]; then
    echo "ERROR: Railway link failed!"
    exit 1
fi
echo ""

# Prompt for OpenAI API Key
echo "Step 3: Setting environment variables..."
echo ""
read -p "Enter your OpenAI API Key (from https://platform.openai.com/api-keys): " OPENAI_KEY

if [ -z "$OPENAI_KEY" ]; then
    echo "ERROR: OpenAI API Key is required!"
    exit 1
fi

echo ""
echo "Setting OPENAI_API_KEY..."
railway variables set OPENAI_API_KEY="$OPENAI_KEY"

echo "Setting YEAR..."
railway variables set YEAR=2025

echo "Setting WEEK_NUMBER..."
railway variables set WEEK_NUMBER=13

echo "Setting DATE..."
railway variables set DATE=2025-11-30

echo "Setting SLATE_DESCRIPTION..."
railway variables set SLATE_DESCRIPTION="Sunday main slate"

echo "Setting FOCUS_GAMES..."
railway variables set FOCUS_GAMES=all

echo "Setting MIN_ARTICLES_FOR_SENTIMENT..."
railway variables set MIN_ARTICLES_FOR_SENTIMENT=3

echo "Setting INCLUDE_LONG_SHOTS..."
railway variables set INCLUDE_LONG_SHOTS=true

echo ""
echo "========================================"
echo "Environment variables set successfully!"
echo "========================================"
echo ""
echo "Railway will automatically redeploy your app."
echo "Wait 1-2 minutes, then check your deployment."
echo ""
echo "To view logs: railway logs"
echo "To open app: railway open"
echo ""