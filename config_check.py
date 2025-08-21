#!/usr/bin/env python3
"""
Configuration validation script for GornBot Docker deployment
Checks if config.yaml is properly configured for containerized deployment
"""

import yaml
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
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

def validate_bot_config(config):
    """Validate bot configuration"""
    bot_config = config.get('bot', {})
    
    # Check required bot fields
    required_fields = ['id', 'name', 'token']
    for field in required_fields:
        if not bot_config.get(field):
            logger.error(f"❌ Missing required bot field: {field}")
            return False
    
    logger.info("✅ Bot configuration is valid")
    return True

def validate_redis_config(config):
    """Validate Redis configuration for Docker"""
    redis_config = config.get('redis', {})
    
    # Check Redis host
    host = redis_config.get('host')
    if host != 'redis':
        logger.warning(f"⚠️  Redis host is set to '{host}', should be 'redis' for Docker deployment")
        logger.info("   This will be automatically corrected for Docker")
    
    # Check Redis URLs
    redis_urls = ['fsm', 'users', 'temp']
    for url_key in redis_urls:
        url = redis_config.get(url_key, '')
        if 'BotsRedis' in url:
            logger.warning(f"⚠️  Redis URL '{url_key}' contains 'BotsRedis', should use 'redis' for Docker")
            logger.info("   This will be automatically corrected for Docker")
    
    logger.info("✅ Redis configuration is valid")
    return True

def validate_openai_config(config):
    """Validate OpenAI configuration"""
    openai_config = config.get('openai', {})
    
    # Check API key
    api_key = openai_config.get('api_key')
    if not api_key:
        logger.error("❌ Missing OpenAI API key")
        return False
    
    # Check model
    model = openai_config.get('model')
    if not model:
        logger.warning("⚠️  OpenAI model not specified")
    
    logger.info("✅ OpenAI configuration is valid")
    return True

def validate_system_config(config):
    """Validate system configuration"""
    system_config = config.get('system', {})
    
    # Check timezone
    timezone = system_config.get('time_zone')
    if not timezone:
        logger.warning("⚠️  System timezone not specified")
    else:
        logger.info(f"✅ System timezone: {timezone}")
    
    return True

def main():
    """Main validation function"""
    logger.info("🔍 Validating GornBot configuration for Docker deployment...")
    
    # Load config
    config = load_config()
    if not config:
        sys.exit(1)
    
    # Validate all sections
    validations = [
        validate_bot_config,
        validate_redis_config,
        validate_openai_config,
        validate_system_config
    ]
    
    all_valid = True
    for validation in validations:
        if not validation(config):
            all_valid = False
    
    if all_valid:
        logger.info("✅ Configuration is ready for Docker deployment!")
        logger.info("🚀 You can now run: ./deploy.sh build && ./deploy.sh up")
    else:
        logger.error("❌ Configuration validation failed")
        logger.info("📝 Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()
