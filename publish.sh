#!/bin/bash
# Complete script to publish insta-bot-gemini to PyPI

echo "📦 Instagram Gemini Bot - PyPI Publishing Script"
echo "=================================================="

# Step 1: Check if build tools are installed
echo ""
echo "Step 1: Installing build tools..."
pip install --upgrade build twine

# Step 2: Clean old builds
echo ""
echo "Step 2: Cleaning old distributions..."
rm -rf build/ dist/ *.egg-info

# Step 3: Build distribution
echo ""
echo "Step 3: Building distribution..."
python -m build

# Step 4: Check distribution
echo ""
echo "Step 4: Checking distribution..."
twine check dist/*

# Step 5: Ask for PyPI token
echo ""
echo "Step 5: Upload to PyPI"
echo "You'll need your PyPI API token. Get it from:"
echo "  1. Go to https://pypi.org/account/"
echo "  2. Login"
echo "  3. Go to Account settings → API tokens"
echo "  4. Generate a new token"
echo ""
echo "When uploading:"
echo "  Username: __token__"
echo "  Password: paste your PyPI API token"
echo ""
read -p "Ready to upload? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Uploading to PyPI..."
    twine upload dist/*
    echo ""
    echo "✅ Published successfully!"
    echo ""
    echo "Users can now install with:"
    echo "  pip install insta-bot-gemini"
else
    echo "Upload cancelled."
fi
