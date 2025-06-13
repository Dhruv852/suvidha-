#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_virtual_environment():
    """Create a Python virtual environment."""
    try:
        venv_path = Path("venv")
        if not venv_path.exists():
            logger.info("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        else:
            logger.info("Virtual environment already exists")
    except Exception as e:
        logger.error(f"Error creating virtual environment: {str(e)}")
        raise

def install_dependencies():
    """Install Python dependencies."""
    try:
        # Determine pip path based on OS
        if os.name == "nt":  # Windows
            pip_path = Path("venv/Scripts/pip")
        else:  # Unix-like
            pip_path = Path("venv/bin/pip")
        
        # Upgrade pip
        logger.info("Upgrading pip...")
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        logger.info("Installing dependencies...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        
        # Install spaCy model
        logger.info("Installing spaCy model...")
        subprocess.run([str(pip_path), "install", "spacy"], check=True)
        subprocess.run([str(pip_path), "run", "python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        
    except Exception as e:
        logger.error(f"Error installing dependencies: {str(e)}")
        raise

def setup_pre_commit_hooks():
    """Set up pre-commit hooks for code quality."""
    try:
        # Install pre-commit
        logger.info("Installing pre-commit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
        
        # Create pre-commit config
        pre_commit_config = """
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
"""
        
        with open(".pre-commit-config.yaml", "w") as f:
            f.write(pre_commit_config)
        
        # Install pre-commit hooks
        logger.info("Installing pre-commit hooks...")
        subprocess.run(["pre-commit", "install"], check=True)
        
    except Exception as e:
        logger.error(f"Error setting up pre-commit hooks: {str(e)}")
        raise

def main():
    """Main function to set up the development environment."""
    try:
        # Change to backend directory
        os.chdir(Path(__file__).parent.parent)
        
        # Create virtual environment
        create_virtual_environment()
        
        # Install dependencies
        install_dependencies()
        
        # Set up pre-commit hooks
        setup_pre_commit_hooks()
        
        logger.info("\nSetup complete! Next steps:")
        logger.info("1. Activate virtual environment:")
        logger.info("   - Windows: .\\venv\\Scripts\\activate")
        logger.info("   - Unix: source venv/bin/activate")
        logger.info("2. Run document processing:")
        logger.info("   python scripts/process_documents.py")
        logger.info("3. Start the development server:")
        logger.info("   uvicorn main:app --reload")
        
    except Exception as e:
        logger.error(f"Error in setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 