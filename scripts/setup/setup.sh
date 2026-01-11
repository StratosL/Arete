#!/bin/bash
# Quick setup script for Arete development environment

set -e

echo "🚀 Setting up Arete development environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Check required environment variables
source .env
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_KEY" ] || [ -z "$CLAUDE_API_KEY" ]; then
    echo "❌ Error: Missing required environment variables"
    echo "   Please ensure SUPABASE_URL, SUPABASE_SERVICE_KEY, and CLAUDE_API_KEY are set in .env"
    exit 1
fi

echo "✅ Environment variables configured"

# Install Python dependencies for setup script
echo "📦 Installing Python dependencies..."
cd backend
python3 -m pip install --break-system-packages supabase python-dotenv
cd ..

# Run Supabase setup
echo "🗄️  Setting up Supabase..."
python3 scripts/setup/setup_supabase.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 You can now start the application:"
echo "   docker-compose up --build"
echo ""
echo "📝 Or run individual services:"
echo "   Backend:  cd backend && python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "   Frontend: cd frontend && npm run dev"
