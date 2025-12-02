#!/bin/bash
# Railway Status Check Script

echo "========================================"
echo "Railway Configuration Check"
echo "========================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo ""
    echo "Install it with:"
    echo "npm install -g @railway/cli"
    echo ""
    exit 1
fi

echo "✅ Railway CLI is installed"
echo ""

# Check if logged in
echo "Checking Railway login status..."
railway whoami
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Not logged in to Railway"
    echo ""
    echo "Run: railway login"
    echo ""
    exit 1
fi

echo ""
echo "✅ Logged in to Railway"
echo ""

# Check if project is linked
echo "Checking if project is linked..."
railway status
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ No project linked"
    echo ""
    echo "Run: railway link"
    echo ""
    exit 1
fi

echo ""
echo "✅ Project is linked"
echo ""

# Show current variables
echo "Current environment variables:"
echo "========================================"
railway variables
echo "========================================"
echo ""

# Check if OPENAI_API_KEY is set
if railway variables | grep -q "OPENAI_API_KEY"; then
    echo "✅ OPENAI_API_KEY is set"
else
    echo "❌ OPENAI_API_KEY is NOT set"
    echo ""
    echo "Set it with:"
    echo "railway variables set OPENAI_API_KEY=your-key-here"
fi

echo ""
echo "========================================"
echo "Check complete!"
echo "========================================"