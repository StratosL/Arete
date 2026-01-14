# API Keys Setup Guide

Arete requires API keys from two services: **Supabase** (database & storage) and **Anthropic** (Claude AI).

## Overview

| Service | Purpose | Cost | Sign Up Link |
|---------|---------|------|--------------|
| Supabase | Database + File Storage + Auth | Free tier available | [supabase.com](https://supabase.com) |
| Anthropic | Claude AI API | Pay-as-you-go (~$0.01-0.05/resume) | [console.anthropic.com](https://console.anthropic.com) |

---

## Supabase Setup (Database & Storage)

Supabase provides the PostgreSQL database and file storage for Arete.

### Step 1: Create a Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"** (top right)
3. Sign up with GitHub, or use email/password
4. Verify your email if required

### Step 2: Create a New Project

1. Once logged in, you'll see the **Dashboard**
2. Click **"New Project"** button
3. Fill in the project details:
   - **Name**: `arete` (or any name you prefer)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose the closest to your location
   - **Pricing Plan**: Free tier is sufficient
4. Click **"Create new project"**
5. Wait ~2 minutes for the project to provision

### Step 3: Get Your API Keys

Once your project is ready:

1. In the left sidebar, click **⚙️ Project Settings** (gear icon at bottom)
2. Click **API** in the settings menu
3. You'll see the **API Settings** page with your keys:

| Key Name | Location | Environment Variable | Usage |
|----------|----------|---------------------|-------|
| **Project URL** | Under "Project URL" | `SUPABASE_URL` | Database connection |
| **anon public** | Under "Project API keys" | `SUPABASE_KEY` | Client-side access |
| **service_role** | Under "Project API keys" (click "Reveal") | `SUPABASE_SERVICE_KEY` | Backend operations |

⚠️ **Important**:
- The `service_role` key is hidden by default - click **"Reveal"** to see it
- Never expose `service_role` key in frontend code or public repositories
- The `anon` key is safe for client-side use

**Example values** (yours will be different):
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNj...
```

---

## Anthropic Claude API Setup

Anthropic provides the Claude AI that powers resume parsing, job analysis, and optimization.

### Step 1: Create an Anthropic Account

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Click **"Sign Up"**
3. Sign up with Google, or use email/password
4. Complete email verification if required
5. You may need to provide payment information (pay-as-you-go pricing)

### Step 2: Generate an API Key

1. Once logged in, you'll see the **Anthropic Console**
2. Click **"API Keys"** in the left sidebar (or go to [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys))
3. Click **"Create Key"** button
4. Give your key a name: `arete-dev` (or any name)
5. Click **"Create Key"**
6. **Copy the key immediately** - it won't be shown again!

| Key Name | Environment Variable | Format |
|----------|---------------------|--------|
| API Key | `CLAUDE_API_KEY` | `sk-ant-api03-...` |

**Example value** (yours will be different):
```env
CLAUDE_API_KEY=sk-ant-api03-abcdefghijklmnopqrstuvwxyz123456789...
```

⚠️ **Important**:
- Copy the key immediately after creation - you can't view it again
- If you lose it, you'll need to create a new key
- Keep your API key secret - don't commit it to git

### Step 3: API Pricing

- Claude API uses pay-as-you-go pricing
- Typical usage for Arete: **~$0.01-0.05 per resume optimization**
- Current pricing: [anthropic.com/pricing](https://www.anthropic.com/pricing)
- Model used: Claude 3.5 Sonnet

**Estimated Costs:**
- Resume parsing: ~$0.005-0.01
- Job analysis: ~$0.002-0.005
- AI optimization: ~$0.01-0.03
- Cover letter generation: ~$0.003-0.008

**Total per application: $0.02-0.05**

---

## Configure Environment Variables

### Step 1: Copy Environment Template

From the Arete project root:

```bash
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in your text editor and add your keys:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Anthropic Claude API
CLAUDE_API_KEY=sk-ant-api03-your-api-key
```

### Step 3: Verify Configuration

Run the validation script:

```bash
python scripts/setup/validate_env.py
```

You should see:
```
✅ All environment variables configured correctly
```

---

## Security Best Practices

### Protecting Your Keys

1. **Never commit .env to git**
   - The `.gitignore` file already excludes `.env`
   - Double-check before committing

2. **Use different keys for development vs. production**
   - Create separate Supabase projects
   - Use separate Anthropic API keys

3. **Rotate keys periodically**
   - Generate new keys every 3-6 months
   - Immediately rotate if compromised

4. **Limit key permissions**
   - Use `anon` key for frontend (read-only operations)
   - Use `service_role` only in backend (full access)

### What to Do If Keys Are Exposed

**Supabase:**
1. Go to Project Settings → API
2. Click "Rotate JWT Secret" (invalidates all keys)
3. Update your `.env` with new keys

**Anthropic:**
1. Go to API Keys in console
2. Delete the exposed key
3. Create a new key
4. Update your `.env`

---

## Troubleshooting

### Supabase connection fails

**Error**: "Invalid Supabase URL or Key"

**Solutions**:
- Verify URL format: `https://[project-ref].supabase.co`
- Check for extra spaces in `.env` file
- Ensure project is fully provisioned (wait 2-3 minutes after creation)
- Test connection: `python scripts/setup/validate_env.py`

### Claude API key invalid

**Error**: "Authentication failed"

**Solutions**:
- Verify key starts with `sk-ant-api03-`
- Check for extra spaces or line breaks
- Ensure you copied the complete key
- Verify billing is set up in Anthropic console
- Check API key hasn't been deleted or expired

### Environment variables not loading

**Error**: Variables are `None` or empty

**Solutions**:
- Verify `.env` file exists in project root
- Check file is named exactly `.env` (not `.env.txt`)
- Restart Docker containers: `docker-compose down && docker-compose up`
- Ensure `.env` uses `KEY=value` format (no spaces around `=`)

---

## Cost Management

### Monitoring Usage

**Anthropic Console:**
- View usage: [console.anthropic.com/settings/usage](https://console.anthropic.com/settings/usage)
- Set up billing alerts
- Review monthly costs

**Supabase Dashboard:**
- Monitor database usage
- Check storage consumption
- Free tier limits: 500MB database, 1GB storage

### Optimizing Costs

1. **Use caching** - Store parsed resume data to avoid re-parsing
2. **Batch operations** - Process multiple optimizations together
3. **Limit retries** - Don't retry failed API calls infinitely
4. **Monitor quotas** - Set up alerts before hitting limits

---

## Next Steps

After configuring your API keys:

1. **Run Setup Script**: `./scripts/setup/setup.sh` or `setup.bat`
2. **Start Application**: `docker-compose up --build`
3. **Test Connection**: Upload a sample resume at http://localhost:3000

For additional help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
