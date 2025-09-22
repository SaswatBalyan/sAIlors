#!/bin/bash

# sAIlors Business Feasibility Analyzer - Webapp Launcher
# This script sets up and runs the integrated webapp with backend and frontend

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
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

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}  sAIlors Business Feasibility  ${NC}"
    echo -e "${PURPLE}        Analyzer Webapp         ${NC}"
    echo -e "${PURPLE}================================${NC}"
    echo ""
}

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python $python_version found"
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip3."
        exit 1
    fi
    print_success "pip3 found"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -f "business_feasibility/requirements.txt" ]; then
        print_error "requirements.txt not found in business_feasibility directory"
        exit 1
    fi
    
    cd business_feasibility
    pip3 install -r requirements.txt
    cd ..
    print_success "Dependencies installed successfully"
}

# Check for environment variables
check_env() {
    print_status "Checking environment configuration..."
    
    if [ ! -f "business_feasibility/.env" ]; then
        print_warning ".env file not found. Creating template..."
        cat > business_feasibility/.env << EOF
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Instructions:
# 1. Get your Google API key from: https://console.cloud.google.com/
# 2. Enable the following APIs:
#    - Google Places API
#    - Google Generative AI API
# 3. Replace 'your_google_api_key_here' with your actual API key
EOF
        print_warning "Please edit business_feasibility/.env and add your Google API key"
        print_warning "You can get a free API key from: https://console.cloud.google.com/"
        print_warning "Make sure to enable Google Places API and Google Generative AI API"
        echo ""
        read -p "Press Enter to continue after adding your API key, or Ctrl+C to exit..."
    fi
    
    # Check if API key is set
    if grep -q "your_google_api_key_here" business_feasibility/.env; then
        print_error "Please update your Google API key in business_feasibility/.env"
        exit 1
    fi
    
    print_success "Environment configuration looks good"
}

# Create static images directory if it doesn't exist
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p business_feasibility/static/images
    print_success "Directories created"
}

# Add a placeholder hero image
add_placeholder_image() {
    if [ ! -f "business_feasibility/static/images/hero-bg.jpg" ]; then
        print_status "Adding placeholder hero image..."
        # Create a simple gradient image using ImageMagick if available, otherwise skip
        if command -v convert &> /dev/null; then
            convert -size 1920x1080 gradient:#05000A-#1B1125 business_feasibility/static/images/hero-bg.jpg
            print_success "Placeholder hero image created"
        else
            print_warning "ImageMagick not found. Hero background will use CSS gradient."
        fi
    fi
}

# Start the Flask application
start_webapp() {
    print_status "Starting sAIlors Business Feasibility Analyzer..."
    print_status "The webapp will be available at: http://localhost:5001"
    print_status "Press Ctrl+C to stop the server"
    echo ""
    
    cd business_feasibility
    python3 app.py
}

# Main execution
main() {
    print_header
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Run checks and setup
    check_python
    check_pip
    create_directories
    add_placeholder_image
    install_dependencies
    check_env
    
    # Start the webapp
    start_webapp
}

# Handle script interruption
trap 'print_warning "Shutting down webapp..."; exit 0' INT

# Run main function
main "$@"
