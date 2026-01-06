# Arete - Quick Setup Guide for Windows

## One-Click Setup (Recommended)

1. **Download the project** and extract to a folder
2. **Copy `.env.example` to `.env`** and add your API keys:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-key
   CLAUDE_API_KEY=sk-ant-your-key
   ```
3. **Right-click in the project folder** → "Open in Terminal" or "Open PowerShell here"
4. **Run the setup script:**
   ```cmd
   setup.bat
   ```
5. **Start the application:**
   ```cmd
   docker-compose up --build
   ```

## Getting Your API Keys

### Supabase Setup (Free)
1. Go to [supabase.com](https://supabase.com) → Sign up/Login
2. Click "New Project" → Wait 2 minutes for creation
3. Go to **Settings** → **API** in your project dashboard
4. Copy these values to your `.env` file:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`
   - **service_role** key → `SUPABASE_SERVICE_KEY` (click "Reveal")

### Claude API Setup
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up/Login → Go to **API Keys**
3. Create a new key → Copy to `CLAUDE_API_KEY` in `.env`

## What the Setup Script Does
- ✅ Validates your `.env` file and API keys
- ✅ Installs required Python packages
- ✅ Creates database tables and storage buckets
- ✅ Tests all connections
- ✅ Provides clear error messages if something fails

## Troubleshooting

**"Python not found"**
- Install Python from [python.org](https://python.org)
- ✅ **Important:** Check "Add Python to PATH" during installation

**"Setup failed"**
- Check your `.env` file has all 4 required keys
- Verify API keys are correct (no extra spaces)
- Ensure internet connection for API calls

**"Docker not found"**
- Install Docker Desktop from [docker.com](https://docker.com)
- Restart computer after installation

## Manual Setup (Alternative)
If the batch script doesn't work, run these commands one by one:

```cmd
# Install dependencies
pip install supabase python-dotenv litellm

# Validate environment
python scripts/validate_env.py

# Setup database
python scripts/setup_supabase.py

# Start application
docker-compose up --build
```

## Need Help?
- Check the main [README.md](README.md) for detailed documentation
- Ensure all API keys are valid and have sufficient credits
- Try the manual setup commands if the batch script fails
