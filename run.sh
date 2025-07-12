#!/bin/bash

chmod +x scripts/*.sh

case $1 in
    "dev"|"start")
        ./scripts/dev.sh
        ;;
    "setup")
        ./scripts/setup.sh
        ;;
    "sync")
        ./scripts/sync.sh
        ;;
    "status")
        ./scripts/status.sh
        ;;
    "stop")
        echo "Stopping all services..."
        docker-compose down
        echo "All services stopped"
        ;;
    "restart")
        echo "Restarting services..."
        docker-compose restart
        echo "Services restarted"
        ;;
    "db-setup")
        ./scripts/db-setup.sh
        ;;
    "db-reset")
        ./scripts/db-reset.sh
        ;;
    "db-shell")
        ./scripts/db-shell.sh
        ;;
    "django-shell")
        ./scripts/django-shell.sh
        ;;
    "superuser")
        ./scripts/create-superuser.sh
        ;;
    "migrate")
        ./scripts/migrate.sh
        ;;
    "test")
        ./scripts/test.sh
        ;;
    "logs")
        ./scripts/logs.sh $2
        ;;
    "clean")
        ./scripts/clean.sh
        ;;
    "deps")
        ./scripts/install-deps.sh
        ;;
    "build")
        ./scripts/build-prod.sh
        ;;
    *)
        echo "DRF-JWT Development Scripts"
        echo ""
        echo "Usage: ./run.sh <command>"
        echo ""
        echo "Main Commands:"
        echo "  setup          Initial project setup (run once)"
        echo "  dev|start      Start development environment"
        echo "  stop           Stop all services"
        echo "  restart        Restart all services"
        echo "  status         Show environment status"
        echo "  sync           Sync with remote & update deps"
        echo ""
        echo "Database Commands:"
        echo "  db-setup       Set up database"
        echo "  db-reset       Reset database (destructive)"
        echo "  db-shell       Access database shell"
        echo "  migrate        Run Django migrations"
        echo ""
        echo "Development Commands:"
        echo "  django-shell   Access Django shell"
        echo "  superuser      Create Django superuser"
        echo "  test           Run all tests"
        echo "  logs [service] View logs (all or specific service)"
        echo "  deps           Install/update dependencies"
        echo ""
        echo "Utility Commands:"
        echo "  clean          Clean up Docker resources"
        echo "  build          Build for production"
        echo ""
        echo "Quick Start:"
        echo "  ./run.sh setup     # First time only"
        echo "  ./run.sh dev       # Daily development"
        echo "  ./run.sh sync      # After git pull"
        ;;
esac
