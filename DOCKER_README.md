# GornBot Docker Deployment

This document explains how to deploy GornBot using Docker Compose.

## 🐳 Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git
- At least 2GB of available RAM

## 📁 Project Structure

```
GornBot/
├── bot.py                 # Main bot entry point
├── config.yaml           # Bot configuration
├── requirements.txt      # Python dependencies
├── src/                 # Source code
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Production deployment
├── docker-compose.override.yml  # Development overrides
├── .dockerignore        # Files to exclude from build
├── deploy.sh            # Deployment script
└── DOCKER_README.md     # This file
```

## 🚀 Quick Start

### 1. Build and Deploy

```bash
# Make the deployment script executable (if not already)
chmod +x deploy.sh

# Build and start the services
./deploy.sh build && ./deploy.sh up
```

### 2. Check Status

```bash
# View service status
./deploy.sh status

# View logs
./deploy.sh logs

# Follow logs in real-time
./deploy.sh logs -f
```

### 3. Stop Services

```bash
./deploy.sh down
```

## 🔧 Manual Docker Commands

If you prefer to use Docker Compose directly:

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart
```

## 🏗️ Services

### Bot Service (`gornbot-app`)
- **Image**: Built from local Dockerfile
- **Port**: Internal port 8000 (for health checks)
- **Dependencies**: Redis
- **Volumes**: 
  - `./logs` → `/app/logs` (log files)
  - `./config.yaml` → `/app/config.yaml` (read-only config)

### Redis Service (`gornbot-redis`)
- **Image**: `redis:7-alpine`
- **Port**: `6379:6379` (accessible from host)
- **Data**: Persistent volume `redis_data`
- **Features**: AOF persistence enabled

## 🔄 Development Mode

The `docker-compose.override.yml` file provides development-specific configurations:

- Source code is mounted for live reloading
- Health checks are simplified
- Additional environment variables for debugging

To use development mode, simply run the same commands - Docker Compose will automatically merge the override file.

## 📊 Monitoring

### Health Checks
- **Redis**: Ping test every 30s
- **Bot**: HTTP health check (if implemented) every 30s

### Logs
```bash
# All services
./deploy.sh logs

# Specific service
docker-compose logs bot
docker-compose logs redis

# Follow logs
./deploy.sh logs -f
```

### Status
```bash
./deploy.sh status
```

## 🔧 Configuration

### Configuration
- **config.yaml**: Main configuration file (mounted read-only)
- **Timezone**: Set to Europe/Moscow
- **Redis Host**: Configured as 'redis' (Docker service name)

### Volumes
- **Redis Data**: `redis_data` (persistent)
- **Logs**: `./logs` (host directory)
- **Config**: `./config.yaml` (read-only)

## 🛠️ Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 6379
lsof -i :6379

# Stop conflicting service or change port in docker-compose.yml
```

#### 2. Permission Issues
```bash
# Fix log directory permissions
mkdir -p logs
chmod 755 logs
```

#### 3. Build Failures
```bash
# Clean build
./deploy.sh clean
./deploy.sh build
```

#### 4. Redis Connection Issues
```bash
# Check Redis container
docker-compose logs redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

#### 5. Bot Not Starting
```bash
# Check bot logs
docker-compose logs bot

# Check configuration
docker-compose exec bot cat /app/config.yaml
```

### Debugging

#### Enter Container
```bash
# Bot container
docker-compose exec bot bash

# Redis container
docker-compose exec redis sh
```

#### View Container Resources
```bash
# Resource usage
docker stats

# Container details
docker-compose ps
```

## 🔒 Security Considerations

1. **API Keys**: Ensure your `config.yaml` contains valid API keys
2. **Redis**: Redis runs without password by default (consider adding one for production)
3. **Network**: Services communicate over internal Docker network
4. **Volumes**: Config file is mounted read-only
5. **Configuration**: All settings are managed through `config.yaml`

## 📈 Production Deployment

For production deployment:

1. **Remove override file**: `rm docker-compose.override.yml`
2. **Update config.yaml**: Ensure all settings are production-ready
3. **Set up proper logging**: Configure log rotation
4. **Add monitoring**: Consider Prometheus/Grafana
5. **Backup strategy**: Set up Redis data backups
6. **SSL/TLS**: If exposing services externally

## 🧹 Cleanup

```bash
# Stop and remove containers
./deploy.sh down

# Remove containers, networks, and volumes
./deploy.sh clean

# Remove images (optional)
docker rmi gornbot_bot
```

## 📝 Useful Commands

```bash
# View all containers
docker ps -a

# View all images
docker images

# View all volumes
docker volume ls

# View all networks
docker network ls

# System cleanup
docker system prune -a
```

## 🤝 Support

If you encounter issues:

1. Check the logs: `./deploy.sh logs`
2. Verify configuration: `docker-compose config`
3. Check Docker status: `docker info`
4. Review this documentation

For additional help, check the main project README or create an issue in the repository.
