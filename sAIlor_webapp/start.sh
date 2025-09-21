#!/bin/bash

# sAIlor Startup Script
# This script helps you start both backend and frontend services

set -e

echo "🚀 Starting sAIlor - AI-Powered Location Intelligence Platform"
echo "=============================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi

if ! command_exists conda; then
    echo -e "${RED}❌ Conda is not installed. Please install Miniconda or Anaconda${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Check if conda environment exists
if ! conda env list | grep -q "sAIlor-backend"; then
    echo -e "${YELLOW}⚠️  Backend environment not found. Creating it...${NC}"
    conda env create -f backend/environment.yml
fi

# Activate conda environment
echo -e "${BLUE}Activating backend environment...${NC}"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate sAIlor-backend

# Check if environment files exist
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  Backend .env not found. Creating from example...${NC}"
    cp backend/.env.example backend/.env
fi

if [ ! -f "geoai-ui/.env.local" ]; then
    echo -e "${YELLOW}⚠️  Frontend .env.local not found. Creating from example...${NC}"
    cp geoai-ui/.env.local.example geoai-ui/.env.local
fi

# Install frontend dependencies if needed
if [ ! -d "geoai-ui/node_modules" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd geoai-ui
    npm install
    cd ..
fi

# Train model if it doesn't exist
if [ ! -f "backend/cache/model.joblib" ]; then
    echo -e "${BLUE}Training ML model...${NC}"
    cd backend
    python app/build_dataset.py
    python app/train.py
    cd ..
fi

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Starting services...${NC}"
echo ""

# Function to start backend
start_backend() {
    echo -e "${GREEN}🔧 Starting Backend (FastAPI)...${NC}"
    cd backend
    uvicorn app.main:app --app-dir . --reload --port 8000 &
    BACKEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Backend started on http://localhost:8000${NC}"
    echo -e "${BLUE}   API Docs: http://localhost:8000/docs${NC}"
}

# Function to start frontend
start_frontend() {
    echo -e "${GREEN}🎨 Starting Frontend (Next.js)...${NC}"
    cd geoai-ui
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Frontend started on http://localhost:3000${NC}"
}

# Start both services
start_backend
sleep 3
start_frontend

echo ""
echo -e "${GREEN}🎉 sAIlor is now running!${NC}"
echo ""
echo -e "${BLUE}📱 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}🔧 Backend:  http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for user to stop
trap 'echo -e "\n${YELLOW}Stopping services...${NC}"; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# Keep script running
wait
