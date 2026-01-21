#!/bin/bash

# Jarvis AI Assistant - Start Script

echo "🤖 Starting Jarvis AI Assistant..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend/.env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env not found${NC}"
    echo "Please run setup.sh first and configure .env"
    exit 1
fi

# Start backend in background
echo -e "${GREEN}Starting backend...${NC}"
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo -e "${GREEN}Starting frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
cd ..

echo ""
echo -e "${GREEN}🚀 Jarvis is running!${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Handle cleanup
trap 'kill $BACKEND_PID $FRONTEND_PID' EXIT

wait
