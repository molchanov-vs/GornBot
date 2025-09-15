#!/bin/bash
# dev-bot.sh
# Helper script to manage only the bot service in docker-compose.dev.yml

COMPOSE="docker-compose -f docker-compose.dev.yml -p gornbot-dev"

case "$1" in
  up)
    $COMPOSE up -d bot
    ;;
  down)
    $COMPOSE stop bot
    ;;
  restart)
    $COMPOSE restart bot
    ;;
  build)
    $COMPOSE build bot
    ;;
  rebuild)
    $COMPOSE build bot && $COMPOSE up -d bot
    ;;
  logs)
    $COMPOSE logs -f bot
    ;;
  shell)
    # Open interactive bash shell inside the running bot container
    $COMPOSE exec bot bash
    ;;
  *)
    echo "Usage: $0 {up|down|restart|build|rebuild|logs|shell}"
    exit 1
    ;;
esac
