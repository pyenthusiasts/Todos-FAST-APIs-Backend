# Deployment Guide

Comprehensive guide for deploying the Todo API to various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

- Python 3.9+
- PostgreSQL (for production) or SQLite (for development)
- Docker and Docker Compose (optional)
- Git

## Environment Configuration

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your settings:

```bash
# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=Todo API
VERSION=1.0.0

# Database Configuration
# For SQLite (development)
DATABASE_URL=sqlite:///./todos.db
# For PostgreSQL (production)
# DATABASE_URL=postgresql://username:password@localhost:5432/tododb

# Security
SECRET_KEY=<generate-a-strong-secret-key>
ALGORITHM=HS256

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False  # Set to False in production

# Logging
LOG_LEVEL=INFO
```

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Database Setup

### SQLite (Development)

1. **Initialize database**:
   ```bash
   python scripts/init_db.py
   ```

2. **Run migrations** (optional):
   ```bash
   alembic upgrade head
   ```

3. **Seed sample data**:
   ```bash
   python scripts/seed_data.py
   ```

### PostgreSQL (Production)

1. **Create database**:
   ```bash
   createdb tododb
   ```

2. **Update DATABASE_URL** in `.env`:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/tododb
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

## Local Development

### Using Virtual Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use Make
make run
```

### Using Docker

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Production Deployment

### 1. Prepare the Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip postgresql nginx -y
```

### 2. Deploy Application

```bash
# Clone repository
git clone https://github.com/your-org/Todos-FAST-APIs-Backend.git
cd Todos-FAST-APIs-Backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production settings

# Initialize database
python scripts/init_db.py
alembic upgrade head
```

### 3. Configure Systemd Service

Create `/etc/systemd/system/todo-api.service`:

```ini
[Unit]
Description=Todo API
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/Todos-FAST-APIs-Backend
Environment="PATH=/path/to/Todos-FAST-APIs-Backend/venv/bin"
ExecStart=/path/to/Todos-FAST-APIs-Backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable todo-api
sudo systemctl start todo-api
sudo systemctl status todo-api
```

### 4. Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/todo-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        access_log off;
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/todo-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configure SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Cloud Platforms

### AWS (Elastic Beanstalk)

1. Install EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize:
   ```bash
   eb init -p python-3.11 todo-api
   ```

3. Create environment:
   ```bash
   eb create todo-api-env
   ```

4. Deploy:
   ```bash
   eb deploy
   ```

### Google Cloud Platform (Cloud Run)

1. Build container:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/todo-api
   ```

2. Deploy:
   ```bash
   gcloud run deploy todo-api \
     --image gcr.io/PROJECT_ID/todo-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Heroku

1. Create app:
   ```bash
   heroku create your-todo-api
   ```

2. Add PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

4. Run migrations:
   ```bash
   heroku run alembic upgrade head
   ```

### DigitalOcean App Platform

1. Create `app.yaml`:
   ```yaml
   name: todo-api
   services:
   - name: api
     github:
       repo: your-org/Todos-FAST-APIs-Backend
       branch: main
     build_command: pip install -r requirements.txt
     run_command: uvicorn app.main:app --host 0.0.0.0 --port 8080
     http_port: 8080
   databases:
   - name: tododb
     engine: PG
   ```

2. Deploy via UI or CLI

## Monitoring and Maintenance

### Health Checks

- Basic: `GET /health`
- Detailed: `GET /health/detailed`
- Readiness: `GET /health/ready`
- Liveness: `GET /health/live`

### Database Backups

```bash
# Create backup
python scripts/db_backup.py backup

# List backups
python scripts/db_backup.py list

# Restore from backup
python scripts/db_backup.py restore --file backups/todos_backup_20250113_120000.db
```

### Log Management

View application logs:

```bash
# Systemd service
sudo journalctl -u todo-api -f

# Docker
docker-compose logs -f api

# Log files (if configured)
tail -f /var/log/todo-api/app.log
```

### Database Maintenance

```bash
# PostgreSQL vacuum
psql tododb -c "VACUUM ANALYZE;"

# Backup PostgreSQL
pg_dump tododb > backup.sql

# Restore PostgreSQL
psql tododb < backup.sql
```

### Performance Tuning

1. **Adjust worker count**:
   ```bash
   # Formula: (2 x CPU cores) + 1
   uvicorn app.main:app --workers 9
   ```

2. **Enable caching** (add Redis if needed)

3. **Database connection pooling**:
   Update `app/db/database.py` with pool settings

4. **Monitor with tools**:
   - New Relic
   - DataDog
   - Prometheus + Grafana

### Security Checklist

- [ ] Update SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up rate limiting
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor logs for suspicious activity

### Scaling

**Horizontal Scaling**:
- Use load balancer (Nginx, HAProxy, AWS ELB)
- Deploy multiple instances
- Share database across instances
- Use Redis for session management

**Vertical Scaling**:
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add indexes
- Use database read replicas

## Troubleshooting

### Common Issues

**Database connection errors**:
```bash
# Check database connectivity
psql -h localhost -U username -d tododb

# Verify DATABASE_URL in .env
```

**Permission errors**:
```bash
# Fix file permissions
sudo chown -R www-data:www-data /path/to/app
```

**Port already in use**:
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill process
sudo kill -9 PID
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
