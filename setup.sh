#!/bin/bash

# Dionysuss All-in-One Setup Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z $host $port 2>/dev/null; then
            print_success "$service_name is ready!"
            return 0
        fi
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start"
    return 1
}

kill_process_on_port() {
    local port=$1
    if port_in_use $port; then
        print_warning "Port $port is in use. Killing existing process..."
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

setup_python_env() {
    print_status "Setting up Python environment..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed."
        exit 1
    fi
    
    if command_exists pyenv; then
        print_status "Using pyenv to set Python version..."
        pyenv shell 3.13.5 2>/dev/null || print_warning "Python 3.13.5 not available"
    fi
    
    if [ -f "backend/requirements.txt" ]; then
        print_status "Installing Python dependencies..."
        cd backend
        pip install -r requirements.txt
        cd ..
    fi
}

setup_node_env() {
    print_status "Setting up Node.js environment..."
    
    if ! command_exists node; then
        print_error "Node.js is not installed."
        exit 1
    fi
    
    if [ -f "webapp/package.json" ]; then
        print_status "Installing Node.js dependencies..."
        cd webapp
        npm install
        cd ..
    fi
}

setup_weaviate() {
    print_status "Setting up Weaviate..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed."
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running."
        exit 1
    fi
    
    if [ ! -f "backend/.env" ] && [ -f ".env" ]; then
        print_status "Copying .env file to backend directory..."
        cp .env backend/
    fi
    
    print_status "Starting Weaviate container..."
    cd backend
    docker-compose -f weaviate-docker-compose.yml down 2>/dev/null || true
    docker-compose -f weaviate-docker-compose.yml up -d
    
    wait_for_service "localhost" 8080 "Weaviate"
    
    print_status "Creating Weaviate schema..."
    sleep 5
    
    curl -X POST "http://localhost:8080/v1/schema" \
        -H "Content-Type: application/json" \
        -d '{
            "class": "Chatpdf",
            "properties": [
                {"name": "source", "dataType": ["text"]},
                {"name": "code", "dataType": ["text"]},
                {"name": "summary", "dataType": ["text"]}
            ],
            "vectorizer": "none"
        }' 2>/dev/null || print_warning "Schema creation failed (might already exist)"
    
    cd ..
    print_success "Weaviate setup complete!"
}

start_backend() {
    print_status "Starting backend server..."
    kill_process_on_port 8008
    
    cd backend
    nohup python main.py > ../backend.log 2>&1 &
    echo $! > ../backend.pid
    cd ..
    
    wait_for_service "localhost" 8008 "Backend"
    print_success "Backend started successfully!"
}

start_frontend() {
    print_status "Starting frontend server..."
    kill_process_on_port 3000
    
    cd webapp
    nohup npm run dev > ../frontend.log 2>&1 &
    echo $! > ../frontend.pid
    cd ..
    
    wait_for_service "localhost" 3000 "Frontend"
    print_success "Frontend started successfully!"
}

cleanup() {
    print_status "Cleaning up..."
    if [ -f "backend.pid" ]; then
        kill $(cat backend.pid) 2>/dev/null || true
        rm -f backend.pid
    fi
    if [ -f "frontend.pid" ]; then
        kill $(cat frontend.pid) 2>/dev/null || true
        rm -f frontend.pid
    fi
}

show_status() {
    echo
    print_status "=== Application Status ==="
    
    if port_in_use 8080; then
        print_success "Weaviate: Running on http://localhost:8080"
    else
        print_error "Weaviate: Not running"
    fi
    
    if port_in_use 8008; then
        print_success "Backend: Running on http://localhost:8008"
    else
        print_error "Backend: Not running"
    fi
    
    if port_in_use 3000; then
        print_success "Frontend: Running on http://localhost:3000"
    else
        print_error "Frontend: Not running"
    fi
    
    echo
    print_status "=== Access URLs ==="
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8008"
    echo "Weaviate: http://localhost:8080"
    echo
}

stop_all() {
    print_status "Stopping all services..."
    
    if [ -f "frontend.pid" ]; then
        kill $(cat frontend.pid) 2>/dev/null || true
        rm -f frontend.pid
    fi
    
    if [ -f "backend.pid" ]; then
        kill $(cat backend.pid) 2>/dev/null || true
        rm -f backend.pid
    fi
    
    cd backend
    docker-compose -f weaviate-docker-compose.yml down 2>/dev/null || true
    cd ..
    
    print_success "All services stopped!"
}

main() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Dionysuss Setup Script                    ║"
    echo "║                    All-in-One Launcher                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    trap cleanup EXIT
    
    case "${1:-start}" in
        "start")
            print_status "Starting complete Dionysuss stack..."
            setup_python_env
            setup_node_env
            setup_weaviate
            start_backend
            start_frontend
            show_status
            print_success "🎉 Dionysuss is now running!"
            print_status "Press Ctrl+C to stop all services"
            while true; do sleep 10; done
            ;;
        "stop")
            stop_all
            ;;
        "restart")
            stop_all
            sleep 2
            exec "$0" start
            ;;
        "status")
            show_status
            ;;
        "clean")
            print_status "Cleaning up all data..."
            stop_all
            if [ -f "webapp/prisma/dev.db" ]; then
                print_status "Clearing frontend database..."
                sqlite3 webapp/prisma/dev.db "DELETE FROM Project; DELETE FROM User; DELETE FROM _ProjectToUser; DELETE FROM Question; DELETE FROM Issue; DELETE FROM \"Commit\"; DELETE FROM Meeting;" 2>/dev/null || true
            fi
            print_status "Clearing Weaviate database..."
            curl -X DELETE "http://localhost:8080/v1/schema/Chatpdf" 2>/dev/null || true
            print_success "All data cleared!"
            ;;
        *)
            echo "Usage: $0 [start|stop|restart|status|clean]"
            echo
            echo "Commands:"
            echo "  start   - Start all services (default)"
            echo "  stop    - Stop all services"
            echo "  restart - Restart all services"
            echo "  status  - Show service status"
            echo "  clean   - Clear all data"
            exit 1
            ;;
    esac
}

main "$@" 