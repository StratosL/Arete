# Troubleshooting Guide

Common issues and solutions when working with Arete.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Resume Parsing Issues](#resume-parsing-issues)
- [Job Analysis Issues](#job-analysis-issues)
- [Frontend Build Issues](#frontend-build-issues)
- [Database Connection Issues](#database-connection-issues)
- [Docker Issues](#docker-issues)
- [API Integration Issues](#api-integration-issues)
- [Performance Issues](#performance-issues)
- [Debug Commands](#debug-commands)

---

## Quick Diagnostics

Run these commands to quickly identify issues:

```bash
# Check Docker status
docker ps
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Validate environment
python scripts/setup/validate_env.py

# Check API health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000
```

---

## Resume Parsing Issues

### Issue: "Resume parsing fails" or returns empty data

**Symptoms:**
- Upload succeeds but parsing returns no data
- Error: "Failed to parse resume"
- Partial data extracted

**Possible Causes & Solutions:**

#### 1. File Format Issues
```bash
# Check file type
file your-resume.pdf

# Verify it's a valid PDF/DOCX/TXT
```

**Solutions:**
- Only PDF, DOCX, and TXT formats supported
- Verify file is not corrupted
- Try converting to different format (PDF → TXT)
- Avoid password-protected or encrypted PDFs

#### 2. File Size Limits
```bash
# Check file size (must be <10MB)
ls -lh your-resume.pdf
```

**Solution:**
- Compress large PDFs using online tools
- Remove unnecessary images/graphics
- Maximum size: 10MB

#### 3. Complex PDF Layouts
**Solution:**
- PDFs with complex layouts (tables, columns) may fail
- Try converting to plain text first
- Use single-column resume format

#### 4. Claude API Issues
```bash
# Check logs for API errors
docker-compose logs backend | grep "Claude"
```

**Solutions:**
- Verify Claude API key is valid: Check `.env`
- Ensure sufficient API credits
- Check Anthropic console for usage limits
- Test API key: `python scripts/setup/validate_env.py`

#### 5. Timeout Issues
**Symptoms:**
- Parsing takes >2 minutes
- Request times out

**Solutions:**
- Simplify resume (remove graphics)
- Check internet connection
- Restart backend: `docker-compose restart backend`

### Issue: "Parsing is slow" (>30 seconds)

**Causes:**
- Large file size
- Complex document structure
- Slow API response

**Solutions:**
- Optimize file size
- Use simpler formatting
- Check network latency to Claude API

---

## Job Analysis Issues

### Issue: "Job analysis not working" or returns empty results

**Symptoms:**
- Analysis returns no data
- Error: "Failed to analyze job"
- Missing required fields

**Possible Causes & Solutions:**

#### 1. Job Description Too Short
**Validation Error:** "Job description must be at least 50 characters"

**Solution:**
- Ensure job description has substantive content
- Minimum: 50 characters for text input
- Include key sections: responsibilities, requirements, skills

#### 2. URL Scraping Fails
**Error:** "Failed to scrape job URL"

**Causes:**
- URL is not publicly accessible
- Website blocks web scraping
- Invalid URL format

**Solutions:**
- Verify URL is accessible in browser
- Try copying job text manually instead of URL
- Use "Text Input" mode as fallback
- Supported sites: LinkedIn, Indeed, most company career pages

#### 3. Form Validation Errors
**Symptoms:**
- Form shows validation errors
- Cannot submit job description

**Solutions:**
- Clear browser cache
- Refresh page (Ctrl+F5 / Cmd+Shift+R)
- Check browser console for JavaScript errors (F12)
- Verify form fields are not empty

#### 4. API Issues
```bash
# Check backend logs
docker-compose logs backend | grep "jobs"
```

**Solutions:**
- Restart backend if schema changed
- Verify Claude API key is valid
- Check API rate limits

---

## Frontend Build Issues

### Issue: "Frontend build fails" or white screen

**Symptoms:**
- `npm run build` fails
- Blank page at localhost:3000
- Console errors in browser

**Diagnostic Steps:**

```bash
# Check Node.js version (requires 18+)
node --version

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check for build errors
npm run build

# View browser console
# Press F12, check Console tab
```

**Common Solutions:**

#### 1. Node Version Mismatch
```bash
# Install Node 18+ via nvm
nvm install 18
nvm use 18
```

#### 2. Dependency Conflicts
```bash
# Clear npm cache
npm cache clean --force

# Delete lock file and reinstall
rm package-lock.json
npm install
```

#### 3. Environment Variables Missing
```bash
# Check .env file
cat .env | grep VITE_API_URL

# Should be: VITE_API_URL=http://localhost:8000
```

#### 4. Vite Configuration Issues
```bash
# Check vite.config.ts for errors
npm run dev -- --debug
```

#### 5. Port Already in Use
```bash
# Check if port 3000 is occupied
netstat -an | grep 3000  # Linux/Mac
netstat -ano | findstr 3000  # Windows

# Kill process or use different port
# In vite.config.ts: server: { port: 3001 }
```

### Issue: "Hot reload not working"

**Solutions:**
- Restart dev server: `docker-compose restart frontend`
- Clear browser cache (Ctrl+Shift+Del)
- Check file watchers aren't exhausted (Linux): `sudo sysctl fs.inotify.max_user_watches=524288`

---

## Database Connection Issues

### Issue: "Database connection errors" or Supabase failures

**Symptoms:**
- Error: "Failed to connect to Supabase"
- Resume data not persisting
- Authentication fails

**Diagnostic Steps:**

```bash
# Validate environment variables
python scripts/setup/validate_env.py

# Check Supabase status
curl https://status.supabase.com

# Test connection
python scripts/database/verify_schema.py
```

**Common Solutions:**

#### 1. Invalid Credentials
```bash
# Verify .env file
cat .env | grep SUPABASE

# Should have:
# SUPABASE_URL=https://...supabase.co
# SUPABASE_KEY=eyJ...
# SUPABASE_SERVICE_KEY=eyJ...
```

**Solutions:**
- Copy keys exactly from Supabase dashboard
- No extra spaces or line breaks
- Check for correct service_role key (not anon key for backend)

#### 2. Schema Not Created
```bash
# Run migrations
python scripts/setup/setup_supabase.py

# Or manually via Supabase dashboard
# Run scripts in supabase/migrations/ in order
```

#### 3. Network Connectivity
```bash
# Test connectivity
ping your-project-id.supabase.co

# Check DNS resolution
nslookup your-project-id.supabase.co
```

**Solutions:**
- Check firewall rules
- Verify internet connection
- Try different network (VPN may block Supabase)

#### 4. Storage Bucket Not Created
**Error:** "Storage bucket 'resumes' not found"

**Solution:**
```bash
# Run setup script
python scripts/setup/setup_supabase.py

# Or create manually in Supabase dashboard:
# Storage → New Bucket → Name: "resumes"
```

---

## Docker Issues

### Issue: "Docker containers won't start"

**Diagnostic Steps:**

```bash
# Check Docker status
docker ps -a

# View logs
docker-compose logs

# Check for port conflicts
netstat -an | grep 8000  # Backend
netstat -an | grep 3000  # Frontend
```

**Common Solutions:**

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

#### 2. Docker Daemon Not Running
```bash
# Start Docker Desktop (Windows/Mac)
# Or start Docker service (Linux)
sudo systemctl start docker
```

#### 3. Permission Issues (Linux)
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. Out of Disk Space
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Issue: "Docker build fails"

**Symptoms:**
- `docker-compose up --build` fails
- Dependency installation errors

**Solutions:**

```bash
# Clear build cache
docker-compose build --no-cache

# Remove old images
docker images | grep arete
docker rmi <image-id>

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

---

## API Integration Issues

### Issue: "Claude API errors" or rate limits

**Error Messages:**
- "Authentication failed"
- "Rate limit exceeded"
- "Invalid API key"

**Solutions:**

#### 1. Authentication Failed
```bash
# Verify API key format
echo $CLAUDE_API_KEY | head -c 20
# Should start with: sk-ant-api03-
```

**Fix:**
- Copy fresh key from Anthropic console
- Ensure no spaces in `.env` file
- Check key hasn't been deleted/expired

#### 2. Rate Limit Exceeded
**Error:** "429 Too Many Requests"

**Solutions:**
- Wait a few minutes before retrying
- Check usage in Anthropic console
- Upgrade API tier if needed
- Implement request queuing (future feature)

#### 3. Insufficient Credits
**Error:** "402 Payment Required"

**Solutions:**
- Add payment method to Anthropic account
- Check current balance
- Typical cost: $0.02-0.05 per resume

#### 4. API Timeout
**Error:** "Request timeout"

**Solutions:**
- Check internet connection
- Verify Claude API status: [status.anthropic.com](https://status.anthropic.com)
- Increase timeout in `backend/app/core/llm.py` (if needed)

---

## Performance Issues

### Issue: "Application is slow" or timeouts

**Symptoms:**
- Requests take >2 minutes
- UI freezes
- Timeouts occur

**Diagnostic Steps:**

```bash
# Check CPU/memory usage
docker stats

# Check logs for errors
docker-compose logs | grep -i error

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

**Solutions:**

#### 1. Insufficient Resources
```bash
# Increase Docker resources in Docker Desktop:
# Settings → Resources → Memory: 4GB+
# Settings → Resources → CPUs: 2+
```

#### 2. Large File Processing
- Optimize resume file size (<5MB ideal)
- Simplify document formatting
- Remove unnecessary graphics

#### 3. Network Latency
- Check internet speed
- Test Claude API latency
- Consider using local LLM (future feature)

#### 4. Database Performance
- Check Supabase dashboard for slow queries
- Ensure indexes are created (via migrations)
- Monitor database usage

---

## Debug Commands

### Backend Debugging

```bash
# Start backend with debug mode
DEBUG=true docker-compose up backend

# Run specific test
cd backend
pytest tests/test_resume_parser.py -v

# Check Python dependencies
docker-compose exec backend pip list

# Interactive Python shell
docker-compose exec backend python
>>> from app.core.config import settings
>>> print(settings.supabase_url)
```

### Frontend Debugging

```bash
# Start with verbose logging
cd frontend
npm run dev -- --debug

# Check build output
npm run build -- --debug

# Run specific test
npm test -- ResumeUpload.test.tsx

# Check dependencies
npm list
```

### Database Debugging

```bash
# Verify schema
python scripts/database/verify_schema.py

# Check migrations
python scripts/database/check_migrations.py

# Test Supabase connection
python -c "from app.core.database import supabase; print(supabase)"
```

### Log Analysis

```bash
# Follow logs in real-time
docker-compose logs -f

# Search for errors
docker-compose logs | grep -i "error\|fail\|exception"

# View last 100 lines
docker-compose logs --tail=100

# Filter by service
docker-compose logs backend | grep "resume"
```

---

## Getting More Help

### Before Seeking Help

1. **Check logs**: `docker-compose logs`
2. **Verify environment**: `python scripts/setup/validate_env.py`
3. **Search existing issues**: [GitHub Issues](https://github.com/StratosL/Arete/issues)
4. **Review documentation**: [docs/](.)

### Reporting Issues

When reporting bugs, include:

1. **Environment**:
   - OS and version
   - Docker version: `docker --version`
   - Node version: `node --version`
   - Python version: `python --version`

2. **Steps to reproduce**:
   - Exact commands run
   - Input files/data used
   - Expected vs. actual behavior

3. **Logs**:
   ```bash
   docker-compose logs > logs.txt
   ```
   Attach `logs.txt` to issue

4. **Configuration** (sanitized):
   - `.env` file (remove API keys!)
   - `docker-compose.yml` modifications

### Contact

- **GitHub Issues**: [Report Bug](https://github.com/StratosL/Arete/issues/new)
- **GitHub Discussions**: [Ask Question](https://github.com/StratosL/Arete/discussions)
- **Email**: [your-email@example.com]

---

## Additional Resources

- **Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **API Keys Setup**: [API_KEYS.md](API_KEYS.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **API Documentation**: http://localhost:8000/docs (when running)
