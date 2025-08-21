# 🚀 GornBot Development Guide

## 🎯 **Development Philosophy**

The best practice for containerized development is to:
1. **Develop locally** - Edit code on your host machine
2. **Run in container** - Execute and test in the containerized environment
3. **Iterate quickly** - Use live mounting and quick restarts

## 🛠️ **Development Workflow**

### **1. Start Development Environment**
```bash
# Start the bot in development mode
./dev.sh start

# Or use the full deploy script
./deploy.sh up
```

### **2. Edit Your Code**
```bash
# Edit files in your local src/ directory
# Changes are automatically mounted into the container
vim src/handlers/your_handler.py
vim src/utils/your_utility.py
```

### **3. Restart After Changes**
```bash
# Quick restart (recommended for most changes)
./dev.sh restart

# Or restart just the bot service
docker-compose restart bot
```

### **4. Monitor Development**
```bash
# Watch logs in real-time
./dev.sh follow

# Check status
./dev.sh status
```

## 🔧 **Development Commands**

### **Quick Reference**
```bash
./dev.sh start      # Start development environment
./dev.sh restart    # Restart bot after code changes
./dev.sh follow     # Watch logs in real-time
./dev.sh shell      # Enter container for debugging
./dev.sh test       # Run configuration tests
./dev.sh stop       # Stop development environment
```

### **Advanced Commands**
```bash
./dev.sh clean      # Clean rebuild (when dependencies change)
./dev.sh logs       # View recent logs
./dev.sh status     # Check container status
```

## 🐛 **Debugging Inside Container**

### **Enter Container Shell**
```bash
./dev.sh shell
```

### **Useful Debugging Commands**
```bash
# Inside the container shell:
python -c "import sys; print(sys.path)"  # Check Python path
python config_check.py                   # Test configuration
python health_check.py                   # Test health
python -c "import src.config; print(src.config)"  # Test imports
ls -la src/                              # Check mounted files
```

### **Test Individual Components**
```bash
# Test locale generation
docker-compose exec bot python scripts/get_locales.py

# Test specific modules
docker-compose exec bot python -c "from src.config import load_config; print(load_config())"
```

## 📁 **File Structure for Development**

```
GornBot/
├── src/                    # Your source code (mounted live)
│   ├── handlers/          # Bot handlers
│   ├── utils/             # Utilities
│   ├── config.py          # Configuration loading
│   └── locales/           # Localization files
├── bot.py                 # Main entry point
├── config.yaml            # Configuration (mounted read-only)
├── requirements.txt       # Dependencies
└── scripts/               # Utility scripts
```

## 🔄 **Development vs Production**

### **Development Mode (Current)**
- ✅ **Live code mounting**: `src/` directory is mounted for live editing
- ✅ **Quick restarts**: No rebuild needed for code changes
- ✅ **Easy debugging**: Direct access to container shell
- ✅ **Real-time logs**: Watch logs as you develop

### **Production Mode**
```bash
# Switch to production
rm docker-compose.override.yml
docker-compose -f docker-compose.prod.yml up -d
```

## 🚨 **Common Development Scenarios**

### **Scenario 1: Adding a New Handler**
```bash
# 1. Create new handler file
vim src/handlers/new_handler.py

# 2. Restart bot to load changes
./dev.sh restart

# 3. Watch logs for any errors
./dev.sh follow
```

### **Scenario 2: Updating Dependencies**
```bash
# 1. Update requirements.txt
vim requirements.txt

# 2. Clean rebuild (needed for dependency changes)
./dev.sh clean

# 3. Start development environment
./dev.sh start
```

### **Scenario 3: Debugging Issues**
```bash
# 1. Check logs
./dev.sh logs

# 2. Enter container for debugging
./dev.sh shell

# 3. Test specific components
python config_check.py
python health_check.py
```

### **Scenario 4: Testing Configuration Changes**
```bash
# 1. Edit config.yaml
vim config.yaml

# 2. Test configuration
./dev.sh test

# 3. Restart bot to apply changes
./dev.sh restart
```

## 📊 **Monitoring Development**

### **Real-time Monitoring**
```bash
# Watch bot logs
./dev.sh follow

# Watch all services
docker-compose logs -f

# Monitor resource usage
docker stats
```

### **Health Checks**
```bash
# Test configuration
./dev.sh test

# Check container health
./dev.sh status

# Manual health check
docker-compose exec bot python health_check.py
```

## 🔧 **Troubleshooting**

### **Bot Won't Start**
```bash
# Check logs
./dev.sh logs

# Test configuration
./dev.sh test

# Enter container to debug
./dev.sh shell
```

### **Code Changes Not Reflected**
```bash
# Restart bot
./dev.sh restart

# Check if files are mounted
docker-compose exec bot ls -la src/
```

### **Dependency Issues**
```bash
# Clean rebuild
./dev.sh clean

# Check requirements
docker-compose exec bot pip list
```

## 🎯 **Best Practices**

### **1. Code Organization**
- Keep handlers in `src/handlers/`
- Keep utilities in `src/utils/`
- Use clear, descriptive file names
- Follow Python naming conventions

### **2. Development Workflow**
- Make small, incremental changes
- Test frequently with `./dev.sh restart`
- Use `./dev.sh follow` to monitor logs
- Commit working changes regularly

### **3. Configuration Management**
- Use `config.yaml` for all settings
- Test configuration with `./dev.sh test`
- Keep sensitive data secure

### **4. Debugging**
- Use container shell for debugging: `./dev.sh shell`
- Test individual components
- Check logs for error messages
- Use health checks to verify setup

## 🚀 **Next Steps**

1. **Start developing**: Use `./dev.sh start` to begin
2. **Add features**: Edit code in `src/` directory
3. **Test changes**: Use `./dev.sh restart` and `./dev.sh follow`
4. **Debug issues**: Use `./dev.sh shell` for container access
5. **Deploy to production**: When ready, use production compose file

---

🎉 **Happy coding! Your containerized development environment is ready!**

