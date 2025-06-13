from typing import List, Dict, Optional
import os
from pathlib import Path
import logging
from .document_processor import DocumentProcessor, Rule
from .vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, data_dir: str, vector_store_dir: str, processor: Optional[DocumentProcessor] = None):
        """Initialize the knowledge base."""
        self.data_dir = Path(data_dir)
        self.vector_store_dir = Path(vector_store_dir)
        self.processor = processor or DocumentProcessor()
        self.vector_store = None
        self.skipped_rules = 0  # Track skipped rules
        
        # Create directories if they don't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize vector store
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize or load the vector store."""
        try:
            if (self.vector_store_dir / "index.faiss").exists():
                logger.info("Loading existing vector store...")
                self.vector_store = VectorStore()
                self.vector_store.load(str(self.vector_store_dir))
            else:
                logger.info("Creating new vector store...")
                self.vector_store = VectorStore()
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
    
    def process_documents(self, force_reprocess: bool = False) -> Dict[str, int]:
        """Process all documents in the data directory."""
        try:
            stats = {"processed": 0, "skipped": 0}
            
            # Check if vector store exists
            if not force_reprocess and self._vector_store_exists():
                logger.info("Vector store exists, skipping document processing")
                self.vector_store.load(self.vector_store_dir)
                return stats
            
            # Process each PDF in the data directory
            for pdf_file in self.data_dir.glob("*.pdf"):
                try:
                    # Determine source from filename
                    source = "GFR 2017" if "GFR" in pdf_file.name else "PM 2025"
                    
                    logger.info(f"Processing {pdf_file.name}...")
                    
                    # Process document
                    rules = self.processor.process_document(
                        str(pdf_file),
                        source
                    )
                    
                    # Validate rules
                    valid_rules = [
                        rule for rule in rules
                        if self.processor.validate_rule(rule)
                    ]
                    
                    # Add rules to vector store
                    self.vector_store.add_rules(valid_rules)
                    
                    stats["processed"] += len(valid_rules)
                    stats["skipped"] += len(rules) - len(valid_rules)
                    
                except Exception as e:
                    logger.error(f"Error processing {pdf_file.name}: {str(e)}")
                    continue
            
            # Save vector store
            self.vector_store.save(self.vector_store_dir)
            
            self.skipped_rules = stats["skipped"]  # Store skipped rules
            return stats
            
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search the knowledge base for relevant rules."""
        try:
            # Ensure vector store is loaded
            if not self._vector_store_exists():
                self.process_documents()
            
            # Perform search
            results = self.vector_store.search(query, k)
            
            # Add categories to results
            for result in results:
                rule = result["rule"]
                result["categories"] = self.processor.categorize_rule(rule)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            raise
    
    def get_rule(self, rule_number: str) -> Optional[Rule]:
        """Get a specific rule by its number."""
        try:
            # Ensure vector store is loaded
            if not self._vector_store_exists():
                self.process_documents()
            
            return self.vector_store.get_rule_by_number(rule_number)
            
        except Exception as e:
            logger.error(f"Error getting rule: {str(e)}")
            raise
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """Get all rules in a specific category."""
        try:
            # Ensure vector store is loaded
            if not self._vector_store_exists():
                self.process_documents()
            
            return self.vector_store.get_rules_by_category(category)
            
        except Exception as e:
            logger.error(f"Error getting rules by category: {str(e)}")
            raise
    
    def _vector_store_exists(self) -> bool:
        """Check if vector store files exist."""
        index_file = self.vector_store_dir / "index.faiss"
        rules_file = self.vector_store_dir / "rules.pkl"
        return index_file.exists() and rules_file.exists()
    
    def get_statistics(self) -> Dict:
        """Get statistics about the knowledge base."""
        try:
            # Ensure vector store is loaded
            if not self._vector_store_exists():
                self.process_documents()
            
            # Count rules by source
            gfr_rules = len([
                rule for rule in self.vector_store.rules
                if rule.source == "GFR 2017"
            ])
            
            pm_rules = len([
                rule for rule in self.vector_store.rules
                if rule.source == "PM 2025"
            ])
            
            # Count rules by category
            categories = {}
            for rule in self.vector_store.rules:
                for category in self.processor.categorize_rule(rule):
                    categories[category] = categories.get(category, 0) + 1
            
            return {
                "total_rules": len(self.vector_store.rules),
                "gfr_rules": gfr_rules,
                "pm_rules": pm_rules,
                "rules_by_category": categories,
                "skipped_rules": self.skipped_rules
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            raise 