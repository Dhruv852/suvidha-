from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
import logging
from .document_processor import Rule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the vector store with a sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.rules = []
        self.rule_texts = []
        
    def add_rules(self, rules: List[Rule]):
        """Add rules to the vector store."""
        try:
            # Extract rule texts
            texts = [f"{rule.rule_number}: {rule.text}" for rule in rules]
            
            # Generate embeddings
            embeddings = self.model.encode(texts, show_progress_bar=True)
            
            # Initialize or update FAISS index
            if self.index is None:
                self.index = faiss.IndexFlatL2(embeddings.shape[1])
            
            # Add vectors to index
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Store rules and texts
            self.rules.extend(rules)
            self.rule_texts.extend(texts)
            
            logger.info(f"Added {len(rules)} rules to vector store")
            
        except Exception as e:
            logger.error(f"Error adding rules to vector store: {str(e)}")
            raise
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar rules using semantic search."""
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Search in FAISS index
            distances, indices = self.index.search(
                np.array(query_embedding).astype('float32'), 
                k
            )
            
            # Prepare results
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.rules):  # Ensure index is valid
                    rule = self.rules[idx]
                    results.append({
                        "rule": rule,
                        "score": float(1 / (1 + distances[0][i])),  # Convert distance to similarity score
                        "text": self.rule_texts[idx]
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
    
    def save(self, path: str):
        """Save the vector store to disk."""
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.index, str(path / "index.faiss"))
            
            # Save rules and texts
            with open(path / "rules.pkl", "wb") as f:
                pickle.dump({
                    "rules": self.rules,
                    "texts": self.rule_texts
                }, f)
            
            logger.info(f"Saved vector store to {path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load(self, path: str):
        """Load the vector store from disk."""
        try:
            path = Path(path)
            
            # Load FAISS index
            self.index = faiss.read_index(str(path / "index.faiss"))
            
            # Load rules and texts
            with open(path / "rules.pkl", "rb") as f:
                data = pickle.load(f)
                self.rules = data["rules"]
                self.rule_texts = data["texts"]
            
            logger.info(f"Loaded vector store from {path}")
            
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
    
    def get_rule_by_number(self, rule_number: str) -> Optional[Rule]:
        """Get a rule by its rule number."""
        try:
            for rule in self.rules:
                if rule.rule_number == rule_number:
                    return rule
            return None
            
        except Exception as e:
            logger.error(f"Error getting rule by number: {str(e)}")
            raise
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """Get rules by category."""
        try:
            from .document_processor import DocumentProcessor
            processor = DocumentProcessor()
            
            return [
                rule for rule in self.rules
                if category in processor.categorize_rule(rule)
            ]
            
        except Exception as e:
            logger.error(f"Error getting rules by category: {str(e)}")
            raise 