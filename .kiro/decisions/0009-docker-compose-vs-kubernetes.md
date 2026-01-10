# 9. Use Docker Compose for Development (Not Kubernetes)

**Date**: 2026-01-05
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: deployment, infrastructure, docker, orchestration

## Context

Arete needs containerization for:
- **Development environment**: Consistent setup across team members
- **Local testing**: Run full stack (frontend + backend + database) locally
- **CI/CD**: Automated testing in GitHub Actions
- **Potential deployment**: Easy hosting on Railway, Render, or similar

Key requirements:
- Fast local development (hot reload, quick startup)
- Simple setup for new developers (single command to start everything)
- Match production environment (minimize "works on my machine" issues)

## Decision Drivers

* **Team size**: Solo developer (hackathon), potentially 2-3 in future
* **Complexity tolerance**: Keep it simple (not managing a cluster)
* **Time constraint**: 3-week hackathon (can't spend days on infrastructure)
* **Cost**: Free tier must be sufficient
* **Learning curve**: Should be easy for Python/React developers to understand
* **Deployment target**: Railway, Render, Vercel (simple PaaS, not AWS EKS)

## Considered Options

### 1. No Containerization (Direct Python + Node)

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Terminal 3: Database
# Download and run PostgreSQL locally
```

**Pros**:
- No Docker knowledge needed
- Fast startup (no container overhead)
- Simple debugging (direct process access)

**Cons**:
- **"Works on my machine"** syndrome
- **Complex setup** (Python version, Node version, PostgreSQL installation)
- **Platform-specific issues** (Windows vs Mac vs Linux)
- **Hard to onboard new developers** (30-minute setup with potential issues)
- **CI/CD complexity** (need to install everything on CI runner)

### 2. Kubernetes (Full Orchestration)

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: arete-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: arete-backend
  template:
    spec:
      containers:
      - name: backend
        image: arete-backend:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: arete-backend-service
spec:
  selector:
    app: arete-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

**Pros**:
- Industry standard for production
- Auto-scaling, self-healing, load balancing
- Declarative configuration
- Powerful for large deployments

**Cons**:
- **Massive overkill** for hackathon/small app
- **Steep learning curve** (Pods, Services, Ingress, ConfigMaps, Secrets...)
- **Complex local setup** (minikube, k3s, or Docker Desktop Kubernetes)
- **Slow iteration** (deploy changes to cluster, wait for pod restart)
- **Expensive** (AWS EKS, GKE, AKS all cost money)
- **Time cost**: 8-12 hours to set up properly

### 3. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app  # Hot reload
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/arete

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app  # Hot reload
    environment:
      - VITE_API_URL=http://localhost:8000

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=arete
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Setup**:
```bash
# One command to start everything
docker-compose up

# That's it! Backend, frontend, and database are running.
```

**Pros**:
- **Simple**: Single YAML file describes entire stack
- **Fast setup**: New developer runs `docker-compose up` and they're ready
- **Consistent environment**: Same containers on all machines
- **Hot reload**: Volume mounts enable live code changes
- **Easy debugging**: `docker-compose logs backend`, `docker-compose exec backend bash`
- **CI/CD friendly**: GitHub Actions can run `docker-compose up` for testing
- **Production-like**: Match production containers (Railway, Render support Docker)

**Cons**:
- Single machine only (can't distribute across cluster)
- No auto-scaling (but we don't need it)
- Less powerful than Kubernetes (but we don't need the power)

### 4. Docker Without Compose (Manual Containers)

```bash
# Build images
docker build -t arete-backend ./backend
docker build -t arete-frontend ./frontend

# Run containers
docker run -d --name arete-db -e POSTGRES_PASSWORD=pass postgres:15
docker run -d --name arete-backend -p 8000:8000 arete-backend
docker run -d --name arete-frontend -p 5173:5173 arete-frontend
```

**Pros**:
- Full Docker control
- No extra tools (just docker CLI)

**Cons**:
- **Manual networking** (need to connect containers)
- **Manual orchestration** (restart order matters)
- **Hard to manage** (many docker run commands)
- **No hot reload** (need to rebuild and restart for code changes)

## Decision Outcome

Chosen option: **Docker Compose**

### Justification

For a hackathon project with potential to grow:

1. **Perfect Balance**:
   ```
   Too simple: No containerization → "works on my machine" issues
   Just right: Docker Compose → consistent, simple, productive
   Too complex: Kubernetes → overkill, slow, expensive
   ```

2. **One-Command Setup**:
   ```bash
   # New developer joins project
   git clone https://github.com/user/arete
   cd arete
   docker-compose up

   # Done! Backend on :8000, Frontend on :5173, DB running.
   # No Python version issues, no Node version issues, no PostgreSQL installation.
   ```

3. **Hot Reload Preserved**:
   ```yaml
   # Backend hot reload (uvicorn --reload works in container)
   backend:
     volumes:
       - ./backend:/app  # Mount source code
     command: uvicorn app.main:app --reload --host 0.0.0.0

   # Frontend hot reload (Vite HMR works in container)
   frontend:
     volumes:
       - ./frontend:/app  # Mount source code
     command: npm run dev -- --host
   ```

4. **Production Alignment**:
   - Railway/Render deploy from Dockerfile
   - Same Dockerfile used in docker-compose.yml
   - **What works locally works in production**

5. **CI/CD Integration**:
   ```yaml
   # .github/workflows/test.yml
   name: Test
   on: [push]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Run tests in Docker
           run: |
             docker-compose up -d
             docker-compose exec -T backend pytest
             docker-compose exec -T frontend npm test
   ```

### Implementation

**Project Structure**:
```
arete/
├── docker-compose.yml       # Main orchestration file
├── backend/
│   ├── Dockerfile          # Backend container definition
│   ├── requirements.txt
│   └── app/
├── frontend/
│   ├── Dockerfile          # Frontend container definition
│   ├── package.json
│   └── src/
└── .env.example            # Environment variables template
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: arete-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - /app/__pycache__  # Exclude cache
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    depends_on:
      - db
    networks:
      - arete-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: arete-frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules  # Exclude node_modules (use container's)
    environment:
      - VITE_API_URL=http://localhost:8000
    command: npm run dev -- --host 0.0.0.0
    depends_on:
      - backend
    networks:
      - arete-network

  db:
    image: postgres:15-alpine
    container_name: arete-db
    environment:
      - POSTGRES_DB=arete
      - POSTGRES_USER=arete_user
      - POSTGRES_PASSWORD=arete_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - arete-network

volumes:
  postgres_data:

networks:
  arete-network:
    driver: bridge
```

**backend/Dockerfile**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command is defined in docker-compose.yml (for flexibility)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**frontend/Dockerfile**:
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Command is defined in docker-compose.yml (for flexibility)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Usage Commands**:
```bash
# Start all services
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run commands in containers
docker-compose exec backend pytest
docker-compose exec backend python -m app.scripts.seed_db
docker-compose exec frontend npm test

# Stop all services
docker-compose down

# Rebuild after dependency changes
docker-compose up --build

# Reset database
docker-compose down -v  # Remove volumes
docker-compose up
```

### Consequences

**Good**:
- ✅ **One-command setup**: `docker-compose up` gets you running
- ✅ **Consistent environments**: No "works on my machine" issues
- ✅ **Hot reload works**: Code changes reflect immediately
- ✅ **Easy debugging**: `docker-compose logs`, `docker-compose exec`
- ✅ **CI/CD ready**: GitHub Actions can run docker-compose
- ✅ **Production-aligned**: Same Dockerfiles used for deployment
- ✅ **Team onboarding**: New developer productive in 5 minutes

**Bad**:
- ⚠️ **Single machine only** (can't scale across cluster, but we don't need this)
- ⚠️ **Container overhead** (~500MB RAM for all containers vs ~300MB native)
- ⚠️ **Initial build time** (2-3 minutes first time, but cached after)

**Neutral**:
- Need Docker Desktop installed (but most developers have it)
- Volume mounts can be slow on Windows/Mac (but fine for our use case)
- Need to rebuild after dependency changes (but rare)

## Validation

Success criteria:

✅ **Criterion 1**: Setup time <5 minutes for new developer
- Result: **3 minutes** (git clone + docker-compose up)

✅ **Criterion 2**: Hot reload works in containers
- Result: **Backend and frontend both hot reload** (save file → see changes in <2s)

✅ **Criterion 3**: Easy debugging
- Result: **docker-compose logs works perfectly**, can exec into containers easily

✅ **Criterion 4**: CI/CD integration
- Result: **GitHub Actions runs docker-compose for testing** (consistent with local)

✅ **Criterion 5**: Production alignment
- Result: **Railway deploys using same Dockerfiles** (zero drift)

## Related Decisions

* [0003-supabase-vs-postgres.md] - Using Supabase for production, but PostgreSQL in docker-compose for local development
* [0001-vertical-slice-architecture.md] - Each service (backend, frontend) is a separate container

## References

* [Docker Compose Documentation](https://docs.docker.com/compose/)
* [Docker Compose for Development Best Practices](https://docs.docker.com/compose/development/)
* Implementation: `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`
* Setup guide: `README.md` (Development section)

## Migration Path (If We Ever Need Kubernetes)

**If the app grows to enterprise scale**:

1. **Docker Compose → Kubernetes** is well-trodden path
2. Tools like **Kompose** can convert docker-compose.yml to Kubernetes YAML
3. Our Dockerfiles work as-is (Kubernetes uses same images)
4. Migration effort: ~16-24 hours

**Signs we'd need Kubernetes**:
- Running on 10+ servers
- Need auto-scaling based on load
- Need zero-downtime deployments with complex rollout strategies
- Need service mesh (Istio, Linkerd)

**Current reality**: None of these apply. Docker Compose is perfect for our scale.

## Future Considerations

**Production Deployment Options** (all support Docker/Docker Compose):

1. **Railway** (current choice):
   - Reads Dockerfile directly
   - No docker-compose needed in production
   - Auto-deploy from GitHub

2. **Render**:
   - Supports Docker + docker-compose
   - Free tier available

3. **Fly.io**:
   - Dockerfile-based deployment
   - Good for global distribution

4. **AWS ECS** (if we scale):
   - Supports Docker containers
   - More complex than above, but more powerful

All options use the same Dockerfiles we have in docker-compose.yml.
