#!/usr/bin/env bash
################################################################################
# Event Horizon - Build Script
# Installs uv package manager and project dependencies
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_step() {
    echo -e "\n${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!] Error: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] Warning: $1${NC}"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="Mac";;
        MINGW*|MSYS*|CYGWIN*)    OS="Windows";;
        *)          OS="Unknown";;
    esac
    echo "$OS"
}

# Check if uv is installed
check_uv() {
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -n1)
        print_success "uv is already installed: $UV_VERSION"
        return 0
    else
        return 1
    fi
}

# Install uv
install_uv() {
    print_step "Installing uv package manager..."
    
    OS=$(detect_os)
    
    if [ "$OS" = "Windows" ]; then
        print_error "Windows detected. Please install uv manually:"
        echo "  PowerShell: irm https://astral.sh/uv/install.ps1 | iex"
        echo "  Or use WSL for automatic installation"
        exit 1
    fi
    
    # Install for Unix-like systems (Linux/Mac)
    if command -v curl &> /dev/null; then
        print_step "Downloading and installing uv via curl..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        print_error "curl is not installed. Please install curl first:"
        if [ "$OS" = "Linux" ]; then
            echo "  Ubuntu/Debian: sudo apt-get install curl"
            echo "  Fedora/RHEL: sudo dnf install curl"
            echo "  Arch: sudo pacman -S curl"
        elif [ "$OS" = "Mac" ]; then
            echo "  Homebrew: brew install curl"
        fi
        exit 1
    fi
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    # Verify installation
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -n1)
        print_success "uv installed successfully: $UV_VERSION"
    else
        print_error "uv installation failed. You may need to restart your shell or add ~/.cargo/bin to PATH"
        echo "  Add to ~/.bashrc or ~/.zshrc: export PATH=\"\$HOME/.cargo/bin:\$PATH\""
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    print_step "Installing Python dependencies with uv..."
    
    if [ -f "uv.lock" ]; then
        print_step "uv.lock found, syncing dependencies..."
        uv sync
    else
        print_step "No uv.lock found, installing from pyproject.toml..."
        uv sync
    fi
    
    print_success "Python dependencies installed"
}

# Install Node.js dependencies (optional)
install_node_deps() {
    if [ -f "package.json" ]; then
        print_step "package.json found, checking for Node.js..."
        
        if command -v npm &> /dev/null; then
            print_step "Installing Node.js dependencies..."
            npm install
            print_success "Node.js dependencies installed"
            
            # Build Tailwind CSS
            print_step "Building Tailwind CSS..."
            npm run build:css
            print_success "Tailwind CSS built"
        else
            print_warning "npm not found. Skipping Node.js dependencies."
            print_warning "Install Node.js from: https://nodejs.org/"
        fi
    else
        print_success "No package.json found, skipping Node.js setup"
    fi
}

# Verify installation
verify_installation() {
    print_step "Verifying installation..."
    
    # Check Python can import Django
    if uv run python -c "import django; print('Django:', django.get_version())" 2>&1; then
        print_success "Django is accessible"
    else
        print_error "Django import failed"
        return 1
    fi
    
    # Check if required packages are installed
    print_step "Checking installed packages..."
    uv pip list | head -n 20
    
    print_success "Installation verified"
}

# Main execution
main() {
    print_header "Event Horizon Build Script"
    
    echo -e "This script will:"
    echo "  1. Install uv package manager (if not present)"
    echo "  2. Install Python dependencies"
    echo "  3. Install Node.js dependencies (if available)"
    echo "  4. Build frontend assets"
    echo ""
    
    # Check/Install uv
    if ! check_uv; then
        install_uv
    fi
    
    # Install dependencies
    install_dependencies
    
    # Install Node.js dependencies and build CSS
    install_node_deps
    
    # Verify installation
    verify_installation
    
    # Success message
    print_header "Build Complete!"
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "  1. Configure .env file:"
    echo "     cp .env.example .env"
    echo "     # Edit .env with your settings"
    echo ""
    echo "  2. Run database migrations:"
    echo "     uv run python manage.py migrate"
    echo ""
    echo "  3. Create a superuser:"
    echo "     uv run python manage.py createsuperuser"
    echo ""
    echo "  4. Start the development server:"
    echo "     uv run python manage.py runserver"
    echo ""
    echo -e "${BLUE}For interactive setup, run:${NC}"
    echo "     python init_project.py"
    echo ""
    echo -e "${GREEN}Documentation:${NC}"
    echo "     README.md, DEVELOPMENT.md, docs/"
    echo ""
}

# Run main function
main
