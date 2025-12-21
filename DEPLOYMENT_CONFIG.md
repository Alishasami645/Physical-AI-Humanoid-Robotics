# Deployment Configuration Files

## 1. Heroku Procfile

If deploying to Heroku, create `backend/Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 2. Railway.toml

If deploying to Railway, create `railway.toml` in project root:

```toml
[build]
builder = "dockerfile"
dockerfilePath = "backend/Dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

## 3. Vercel for Frontend

Frontend is already deployed. To redeploy:

```bash
vercel deploy
```

## 4. Environment Variables for Production

Set these in your deployment platform:

```
OPENAI_API_KEY=<your-key>
DATABASE_URL=<your-neon-url>
QDRANT_URL=<your-qdrant-url>
QDRANT_API_KEY=<your-key>
BACKEND_URL=<your-backend-url>
CORS_ORIGINS=<comma-separated-origins>
```

## 5. CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
          appdir: "backend"
```

## Setup Instructions by Platform

### Heroku Deployment

```bash
# Create app
heroku create your-robotics-backend

# Set environment variables
heroku config:set -a your-robotics-backend \
  OPENAI_API_KEY="sk-..." \
  DATABASE_URL="postgresql://..." \
  QDRANT_URL="https://..." \
  QDRANT_API_KEY="..."

# Deploy
git push heroku main

# View logs
heroku logs -a your-robotics-backend --tail
```

### Railway Deployment

```bash
# Login
railway login

# Link project
railway link

# Set variables
railway variables add OPENAI_API_KEY sk-...
railway variables add DATABASE_URL postgresql://...
railway variables add QDRANT_URL https://...
railway variables add QDRANT_API_KEY ...

# Deploy
railway up

# Get URL
railway open
```

### Docker Local Development

```bash
# Build and run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Stop
docker-compose down
```

### AWS Lambda + API Gateway

Package requirements for Lambda:
```bash
pip install -t backend/package -r backend/requirements.txt
cd backend/package && zip -r ../lambda.zip . && cd ..
zip lambda.zip *.py
```

Use AWS SAM template or Serverless Framework for deployment.

## SSL/TLS Configuration

For production, always use HTTPS. Most hosting platforms (Vercel, Heroku, Railway) provide free SSL certificates.

Update CORS_ORIGINS to use https:
```
CORS_ORIGINS=https://physical-ai-humanoid-robotics.vercel.app,https://your-backend.com
```

## Monitoring and Logging

### Application Performance Monitoring

Consider using:
- **Sentry**: Error tracking (`pip install sentry-sdk`)
- **DataDog**: Monitoring and logging
- **New Relic**: Performance monitoring
- **Grafana**: Metrics visualization

### Log Aggregation

- Heroku: Built-in logging via `heroku logs`
- Railway: Dashboard logging
- Custom: Use CloudWatch, ELK Stack, or Splunk

## Database Backups

### Neon Postgres

- Automatic backups included in free tier
- Manual backup: Use `pg_dump`
  ```bash
  pg_dump $DATABASE_URL > backup.sql
  ```

### Restore

```bash
psql $DATABASE_URL < backup.sql
```

## Scaling Considerations

1. **Vector Store (Qdrant)**
   - Free tier includes up to 1M vectors
   - Upgrade to paid tier if needed
   - Consider caching frequent queries

2. **Database (Neon)**
   - Free tier includes generous limits
   - Auto-scaling available on paid plans
   - Connection pooling enabled

3. **LLM API (OpenAI)**
   - Pay-per-use model
   - Implement caching for common questions
   - Consider rate limiting

4. **Backend (FastAPI)**
   - Stateless design allows horizontal scaling
   - Use load balancer in production
   - Consider CDN for static assets
