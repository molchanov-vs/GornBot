#!/bin/bash
# dev-bot.sh
# Helper script to manage only the bot service in docker-compose.dev.yml

COMPOSE="docker-compose -f docker-compose.dev.yml -p gornbot-dev"

# Stream bot logs with optional tail argument and trimmed timestamps
stream_logs() {
  local tail_flag=""
  if [[ -n "$1" ]]; then
    tail_flag="--tail=$1"
  fi

  # Remove fractional seconds from the RFC3339 timestamp
  $COMPOSE logs -f --timestamps $tail_flag bot | \
    sed -E 's/(T[0-9]{2}:[0-9]{2}:[0-9]{2})\.[0-9]+Z/\1Z/'
}

case "$1" in
  up)
    $COMPOSE up -d bot
    ;;
  down)
    $COMPOSE stop bot
    ;;
  restart)
    $COMPOSE restart bot
    stream_logs "$2"
    ;;
  build)
    $COMPOSE build bot
    ;;
  rebuild)
    $COMPOSE build bot && $COMPOSE up -d bot
    ;;
  logs)
    stream_logs "$2"
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
