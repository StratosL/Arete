# 3. Use Supabase Instead of Direct PostgreSQL

**Date**: 2026-01-05
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: database, infrastructure, backend

## Context

Arete needs a database to store:
- Resume metadata (id, filename, upload_date)
- Parsed resume data (JSON)
- Job analysis results
- Optimization suggestions
- User data (for future multi-user support)

We also need:
- File storage (for uploaded PDF/DOCX files)
- Authentication (for user accounts)
- API access to data

## Decision Drivers

* **Time constraint**: 3-week hackathon timeline
* **Complexity**: Don't want to manage infrastructure
* **Features needed**: Database + Auth + File Storage
* **Cost**: Free tier must be sufficient for MVP
* **Flexibility**: Should be easy to migrate away if needed
* **Development speed**: Quick setup and deployment

## Considered Options

### 1. Direct PostgreSQL + Custom Auth + AWS S3

```
Setup:
- PostgreSQL on Railway/Render
- Custom JWT auth implementation
- AWS S3 for file storage
- Write REST API endpoints manually
```

**Pros**:
- Full control over everything
- No vendor lock-in (standard PostgreSQL)
- Can optimize exactly as needed
- Industry standard stack

**Cons**:
- **Setup time: 4-6 hours** (database, auth, storage, APIs)
- Need to write auth logic (JWT, refresh tokens, password hashing)
- Need to set up S3 buckets and IAM policies
- Need to write CRUD API endpoints manually
- More infrastructure to manage

### 2. Firebase (Google)

```
Setup:
- Firestore (NoSQL database)
- Firebase Auth
- Firebase Storage
- Auto-generated APIs
```

**Pros**:
- Fast setup (1-2 hours)
- All-in-one platform
- Generous free tier
- Real-time updates built-in

**Cons**:
- **NoSQL** (document-based, not relational)
- No SQL queries (would need to restructure data model)
- Google vendor lock-in
- Migration to SQL later is painful

### 3. Supabase

```
Setup:
- PostgreSQL database (fully managed)
- Built-in auth (email/password, OAuth)
- Built-in storage (file uploads)
- Auto-generated REST API
- Row Level Security (RLS)
```

**Pros**:
- **Setup time: <1 hour**
- All-in-one platform (database + auth + storage)
- Uses **standard PostgreSQL** (easy to migrate)
- Auto-generated REST API (no manual endpoints needed)
- Free tier: 500MB database, 1GB storage (sufficient)
- **Open source** (can self-host if needed)
- Real-time subscriptions available
- Row Level Security for data isolation

**Cons**:
- Vendor dependency (though mitigated by open-source)
- Slightly less control vs raw PostgreSQL
- Learning curve for Supabase-specific features (RLS, policies)

## Decision Outcome

Chosen option: **Supabase**

### Justification

For a hackathon with tight timeline:

1. **Time Savings**:
   - Supabase: <1 hour setup
   - PostgreSQL + Auth + S3: 4-6 hours setup
   - **Saved: 3-5 hours**

2. **All-in-One Platform**:
   ```
   One service provides:
   ✅ PostgreSQL database
   ✅ Authentication (with JWT tokens)
   ✅ File storage (for resume PDFs)
   ✅ Auto-generated REST API
   ✅ Real-time subscriptions (for future features)
   ```

3. **Standard PostgreSQL**:
   - Not locked into proprietary NoSQL (like Firebase)
   - Can export database and migrate to raw PostgreSQL anytime
   - SQL queries work exactly as expected

4. **Free Tier is Sufficient**:
   - 500MB database (enough for thousands of resumes)
   - 1GB storage (enough for 100+ resume files)
   - 50,000 monthly active users (way more than needed)

5. **Open Source**:
   - Can self-host Supabase if we need full control later
   - Not locked into a proprietary platform

### Implementation

```python
# backend/app/core/database.py
from supabase import create_client, Client

supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_key
)

# Insert data
supabase.table("resumes").insert({
    "filename": "resume.pdf",
    "parsed_data": {...}
}).execute()

# Query data
result = supabase.table("resumes").select("*").eq("id", resume_id).execute()
```

**File storage**:
```python
# Upload file
supabase.storage.from_("resumes").upload(
    path=f"{resume_id}/resume.pdf",
    file=file_content
)

# Download file
file_url = supabase.storage.from_("resumes").get_public_url(
    f"{resume_id}/resume.pdf"
)
```

### Consequences

**Good**:
- ✅ **Set up entire backend in <1 hour** (database, auth, storage, APIs)
- ✅ Auto-generated REST API (no manual CRUD endpoints)
- ✅ Built-in auth (email/password works out of the box)
- ✅ File storage for resume uploads (no S3 configuration)
- ✅ Standard PostgreSQL (easy to migrate if needed)
- ✅ Row Level Security for future multi-user support

**Bad**:
- ⚠️ Vendor dependency (though open-source mitigates this)
- ⚠️ Some Supabase-specific learning curve (RLS policies)
- ⚠️ Less control than raw PostgreSQL + custom setup

**Neutral**:
- Free tier limits (500MB DB, 1GB storage) are fine for MVP
- Need to handle Supabase client initialization
- Auto-generated API sometimes less flexible than custom endpoints

## Validation

Success criteria:

✅ **Criterion 1**: Setup time <1 hour
- Result: **45 minutes** from account creation to first database insert

✅ **Criterion 2**: Auth works without custom implementation
- Result: Email/password auth working with zero custom code

✅ **Criterion 3**: File storage works for resume uploads
- Result: PDF/DOCX files uploading and downloading successfully

✅ **Criterion 4**: Can migrate to raw PostgreSQL if needed
- Result: Database is standard PostgreSQL, export works via pg_dump

⏳ **Criterion 5**: Free tier sufficient for MVP
- Result: Currently using <10MB database, <100MB storage (well within limits)

## Related Decisions

* [0001-vertical-slice-architecture.md] - Database client sits in core/ (shared by all slices)
* [0009-docker-compose-vs-kubernetes.md] - Simple deployment matches Supabase managed service

## Migration Path (If Needed Later)

If we ever need to migrate away from Supabase:

1. **Export database**: `pg_dump` to get full PostgreSQL dump
2. **Set up raw PostgreSQL**: Railway, Render, or AWS RDS
3. **Replace auth**: Implement JWT auth with FastAPI-Users or similar
4. **Replace storage**: Migrate to AWS S3 or local filesystem
5. **Replace API client**: Use SQLAlchemy or raw psycopg2

**Estimated migration effort**: 8-12 hours

## References

* [Supabase Documentation](https://supabase.com/docs)
* [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
* Setup script: `scripts/setup/setup_supabase.py`
