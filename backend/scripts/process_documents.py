#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
import logging
import google.generativeai as genai

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from utils.document_processor import DocumentProcessor
from utils.knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Gemini API with specific model and key
GEMINI_API_KEY = "AIzaSyA7zvS_Z97Eeb1Ue5M0ZNn-H8UFIKBcY4M"
genai.configure(api_key=GEMINI_API_KEY)

def setup():
    """Set up the environment for document processing."""
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Copy PDF files to data directory
    pdf_files = ["GFR2017.pdf", "pm2025.pdf"]
    for pdf in pdf_files:
        src = Path("..") / pdf
        dst = data_dir / pdf
        if not dst.exists():
            logger.info(f"Copying {pdf} to data directory...")
            shutil.copy(src, dst)
        else:
            logger.info(f"{pdf} already exists in data directory")

def main():
    """Process documents and create knowledge base."""
    try:
        # Set up environment
        setup()
        
        # Initialize document processor with debug mode
        processor = DocumentProcessor(debug=True)
        
        # Initialize knowledge base with data directory
        kb = KnowledgeBase(
            data_dir="data",
            vector_store_dir="vector_store",
            processor=processor
        )
        
        # Process documents
        logger.info("Processing documents...")
        kb.process_documents()
        
        # Print statistics
        stats = kb.get_statistics()
        logger.info("\nProcessing complete!")
        logger.info(f"Processed {stats['total_rules']} rules")
        logger.info(f"Skipped {stats['skipped_rules']} invalid rules")
        logger.info("\nKnowledge Base Statistics:")
        logger.info(f"Total Rules: {stats['total_rules']}")
        logger.info(f"GFR Rules: {stats['gfr_rules']}")
        logger.info(f"PM Rules: {stats['pm_rules']}")
        logger.info("\nRules by Category:")
        for category, count in stats['rules_by_category'].items():
            logger.info(f"{category}: {count}")
            
    except Exception as e:
        logger.error(f"Error processing documents: {str(e)}")
        raise

if __name__ == "__main__":
    main() 