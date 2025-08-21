#!/usr/bin/env python3
"""
Simple health check script for GornBot
Can be used to verify the bot is running and Redis is accessible
"""

import sys
import redis
import yaml
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from config.yaml"""
    try:
        config_path = Path("config.yaml")
        if not config_path.exists():
            logger.error("config.yaml not found")
            return None
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return None

def check_redis(config):
    """Check Redis connection"""
    try:
        # Get Redis host from config, default to 'redis' (Docker service name)
        redis_host = config.get('redis', {}).get('host', 'redis')
        r = redis.Redis(host=redis_host, port=6379, db=0, socket_connect_timeout=5)
        r.ping()
        logger.info(f"✅ Redis connection successful to {redis_host}")
        return True
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        return False

def check_config(config):
    """Check if essential config is present"""
    try:
        # Check bot token
        bot_token = config.get('bot', {}).get('token')
        if not bot_token:
            logger.error("❌ Bot token not found in config")
            return False
        
        # Check OpenAI API key
        openai_key = config.get('openai', {}).get('api_key')
        if not openai_key:
            logger.error("❌ OpenAI API key not found in config")
            return False
        
        logger.info("✅ Configuration looks good")
        return True
    except Exception as e:
        logger.error(f"❌ Config check failed: {e}")
        return False

def main():
    """Main health check function"""
    logger.info("🔍 Starting GornBot health check...")
    
    # Load config
    config = load_config()
    if not config:
        sys.exit(1)
    
    # Check configuration
    if not check_config(config):
        sys.exit(1)
    
    # Check Redis
    if not check_redis(config):
        sys.exit(1)
    
    logger.info("✅ All health checks passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()
