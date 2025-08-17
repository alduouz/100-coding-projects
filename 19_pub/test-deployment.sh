#!/bin/bash

# Pre-deployment test script
echo "🚀 Pre-deployment checks..."

# Check required files exist
echo "📁 Checking required files..."
[ -f "requirements.txt" ] && echo "✅ requirements.txt exists" || echo "❌ requirements.txt missing"
[ -f "Procfile" ] && echo "✅ Procfile exists" || echo "❌ Procfile missing"
[ -f ".dockerignore" ] && echo "✅ .dockerignore exists" || echo "❌ .dockerignore missing"
[ -f ".env.example" ] && echo "✅ .env.example exists" || echo "❌ .env.example missing"

# Check Procfile format
echo "📋 Checking Procfile format..."
if grep -q "web: gunicorn" Procfile; then
    echo "✅ Procfile has correct format"
else
    echo "❌ Procfile format incorrect"
fi

# Check requirements.txt includes gunicorn
echo "📦 Checking dependencies..."
if grep -q "gunicorn" requirements.txt; then
    echo "✅ gunicorn in requirements.txt"
else
    echo "❌ gunicorn missing from requirements.txt"
fi

# Test local gunicorn start (if available)
echo "🧪 Testing gunicorn startup..."
if command -v gunicorn &> /dev/null; then
    timeout 5 gunicorn app:app --bind 0.0.0.0:8000 --check-config && echo "✅ Gunicorn config valid" || echo "❌ Gunicorn config invalid"
else
    echo "⚠️  Gunicorn not installed locally (install for testing: pip install gunicorn)"
fi

echo "✅ Pre-deployment checks complete!"