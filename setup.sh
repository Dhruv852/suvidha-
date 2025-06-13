#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up GFR & PM Assistant...${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Please install Node.js and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is required but not installed. Please install npm and try again."
    exit 1
fi

# Create necessary directories
echo -e "${BLUE}Creating project directories...${NC}"
mkdir -p backend/data
mkdir -p backend/vector_store
mkdir -p frontend/public

# Copy PDF files to backend/data
echo -e "${BLUE}Copying PDF files...${NC}"
cp GFR2017.pdf backend/data/
cp pm2025.pdf backend/data/
cp GFR2017.pdf frontend/public/
cp pm2025.pdf frontend/public/

# Set up backend
echo -e "\n${BLUE}Setting up backend...${NC}"
cd backend
python3 scripts/setup.py
cd ..

# Set up frontend
echo -e "\n${BLUE}Setting up frontend...${NC}"
cd frontend
npm install
cd ..

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "\nTo start the application:"
echo -e "1. Start the backend server:"
echo -e "   ${BLUE}cd backend${NC}"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}uvicorn main:app --reload${NC}"
echo -e "\n2. In a new terminal, start the frontend server:"
echo -e "   ${BLUE}cd frontend${NC}"
echo -e "   ${BLUE}npm run dev${NC}"
echo -e "\n3. Open your browser and navigate to:"
echo -e "   ${BLUE}http://localhost:3000${NC}"
echo -e "\nNote: Make sure to update the GEMINI_API_KEY in backend/.env before starting the application." 