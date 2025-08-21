# 🐳 GornBot Docker Deployment Setup

## ✅ What's Been Created

Your GornBot now has a complete Docker Compose deployment setup with the following files:

### Core Docker Files
- **`Dockerfile`** - Defines the bot application container
- **`docker-compose.yml`** - Main deployment configuration
- **`docker-compose.override.yml`** - Development-specific overrides
- **`docker-compose.prod.yml`** - Production-optimized configuration
- **`.dockerignore`** - Excludes unnecessary files from build

### Deployment Tools
- **`deploy.sh`** - Convenient deployment script with commands
- **`health_check.py`** - Health monitoring script

### Documentation
- **`DOCKER_README.md`** - Comprehensive deployment guide
- **`DEPLOYMENT_SUMMARY.md`** - This summary

## 🚀 Quick Start Commands

```bash
# 1. Build and start the bot
./deploy.sh build && ./deploy.sh up

# 2. Check if everything is running
./deploy.sh status

# 3. View logs
./deploy.sh logs -f

# 4. Stop the bot
./deploy.sh down
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   GornBot App   │    │     Redis       │
│   (Python)      │◄──►│   (State Mgmt)  │
│   Container     │    │   Container     │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
                    │
              Docker Network
```

## 📋 Services

### Bot Service (`gornbot-app`)
- **Purpose**: Runs your Telegram bot
- **Image**: Built from your code
- **Dependencies**: Redis
- **Health Check**: Configuration and Redis connectivity

### Redis Service (`gornbot-redis`)
- **Purpose**: State management and caching
- **Image**: `redis:7-alpine`
- **Port**: `6379` (accessible from host)
- **Data**: Persistent storage

## 🔧 Configuration

### Development Mode
- Source code is mounted for live editing
- Automatic code reloading
- Simplified health checks

### Production Mode
- Optimized for performance
- Resource limits
- Enhanced security (optional Redis password)

## 📊 Monitoring

### Health Checks
- **Bot**: Configuration validation + Redis connectivity
- **Redis**: Ping test
- **Frequency**: Every 30 seconds

### Logs
```bash
# All services
./deploy.sh logs

# Specific service
docker-compose logs bot
docker-compose logs redis
```

## 🛠️ Common Operations

### Development
```bash
# Start with live code reloading
./deploy.sh up

# View real-time logs
./deploy.sh logs -f

# Restart after code changes
./deploy.sh restart
```

### Production
```bash
# Use production config
docker-compose -f docker-compose.prod.yml up -d

# Update config.yaml for production settings
# Then restart the services
docker-compose -f docker-compose.prod.yml restart
```

### Maintenance
```bash
# Update bot code
./deploy.sh down
./deploy.sh build
./deploy.sh up

# Clean up everything
./deploy.sh clean

# Check resource usage
docker stats
```

## 🔒 Security Notes

1. **API Keys**: Your `config.yaml` contains sensitive data - keep it secure
2. **Redis**: Runs without password by default (consider adding one for production)
3. **Network**: Services communicate over internal Docker network
4. **Volumes**: Config is mounted read-only
5. **Configuration**: All settings managed through `config.yaml`

## 📈 Next Steps

1. **Test the deployment**: Run `./deploy.sh build && ./deploy.sh up`
2. **Verify bot functionality**: Check logs and test bot commands
3. **Set up monitoring**: Consider adding Prometheus/Grafana
4. **Configure backups**: Set up Redis data backups
5. **Production hardening**: Review security settings

## 🆘 Troubleshooting

### Bot won't start?
```bash
# Check logs
./deploy.sh logs

# Verify config
docker-compose exec bot python health_check.py

# Check Redis connection
docker-compose exec redis redis-cli ping
```

### Build fails?
```bash
# Clean and rebuild
./deploy.sh clean
./deploy.sh build
```

### Port conflicts?
```bash
# Check what's using port 6379
lsof -i :6379

# Change port in docker-compose.yml if needed
```

## 📚 Additional Resources

- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **Redis Documentation**: https://redis.io/documentation
- **aiogram Documentation**: https://docs.aiogram.dev/

---

🎉 **Your GornBot is now ready for Docker deployment!**

The setup provides both development and production configurations, making it easy to deploy your bot in any environment. The health checks and monitoring ensure your bot stays running smoothly.
