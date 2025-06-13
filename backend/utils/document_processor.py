from typing import List, Dict, Optional
import re
from pathlib import Path
from pypdf import PdfReader
import spacy
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Rule:
    rule_number: str
    text: str
    chapter: str
    section: str
    subsection: Optional[str]
    page: int
    source: str

class DocumentProcessor:
    def __init__(self, debug: bool = False):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")
        self.debug = debug
        
        # Common patterns for rule extraction
        self.gfr_patterns = [
            r"(\d+(?:\.\d+)*)\s+(.*?)(?=\s*\d+(?:\.\d+)*|$)",
            r"Rule\s+(\d+)\s*-\s*(.*?)(?=Rule\s+\d+|$)"
        ]
        
        self.pm_patterns = [
            r"(\d+\.\d+\.\d+)\s+(.*?)(?=\d+\.\d+\.\d+|$)",
            r"Section\s+(\d+)\s*:\s*(.*?)(?=Section\s+\d+|$)"
        ]

    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """Extract text from PDF with page numbers."""
        try:
            reader = PdfReader(pdf_path)
            text_by_page = []
            
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_by_page.append({
                        "page": page_num,
                        "text": text
                    })
            
            return text_by_page
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise

    def extract_rules(self, text_by_page: List[Dict[str, str]], 
                     patterns: List[str], source: str) -> List[Rule]:
        """Extract rules from text using provided patterns."""
        rules = []
        skipped_rules = []
        
        for page_data in text_by_page:
            page_num = page_data["page"]
            text = page_data["text"]
            
            # Try each pattern
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.DOTALL)
                
                for match in matches:
                    try:
                        if len(match.groups()) == 2:
                            rule_num, rule_text = match.groups()
                            
                            # Extract chapter and section from rule number
                            parts = rule_num.split('.')
                            chapter = parts[0] if len(parts) > 0 else ""
                            section = parts[1] if len(parts) > 1 else ""
                            subsection = parts[2] if len(parts) > 2 else None
                            
                            # Clean up rule text
                            rule_text = rule_text.strip()
                            
                            # Create rule object
                            rule = Rule(
                                rule_number=rule_num,
                                text=rule_text,
                                chapter=chapter,
                                section=section,
                                subsection=subsection,
                                page=page_num,
                                source=source
                            )
                            
                            if self.validate_rule(rule):
                                rules.append(rule)
                            else:
                                skipped_rules.append(rule)
                                if self.debug:
                                    logger.warning(f"Skipped invalid rule from {source} - Rule {rule.rule_number}: {rule.text[:100]}...")
                    except Exception as e:
                        logger.warning(f"Error processing rule match: {str(e)}")
                        continue
        
        if self.debug and skipped_rules:
            logger.info(f"\nSkipped Rules Summary for {source}:")
            logger.info(f"Total skipped: {len(skipped_rules)}")
            logger.info("Sample of skipped rules:")
            for rule in skipped_rules[:5]:  # Show first 5 skipped rules
                logger.info(f"Rule {rule.rule_number}: {rule.text[:100]}...")
        
        return rules

    def process_document(self, pdf_path: str, source: str) -> List[Rule]:
        """Process a document and extract all rules."""
        try:
            # Extract text from PDF
            text_by_page = self.extract_text_from_pdf(pdf_path)
            
            # Select patterns based on source
            patterns = self.gfr_patterns if "GFR" in source else self.pm_patterns
            
            # Extract rules
            rules = self.extract_rules(text_by_page, patterns, source)
            
            logger.info(f"Extracted {len(rules)} rules from {source}")
            return rules
            
        except Exception as e:
            logger.error(f"Error processing document {pdf_path}: {str(e)}")
            raise

    def validate_rule(self, rule: Rule) -> bool:
        """Validate if a rule has all required components."""
        try:
            # Basic validation
            if not rule.rule_number or not rule.text:
                if self.debug:
                    logger.warning(f"Skipped rule due to missing rule_number or text: {rule.rule_number}")
                return False
                
            # Validate rule number format
            if not re.match(r"^\d+(\.\d+)*$", rule.rule_number):
                if self.debug:
                    logger.warning(f"Skipped rule due to invalid rule number format: {rule.rule_number}")
                return False
                
            # Validate text length
            if len(rule.text) < 10:  # Minimum reasonable length
                if self.debug:
                    logger.warning(f"Skipped rule due to short text (length {len(rule.text)}): {rule.text[:100]}...")
                return False
                
            return True
            
        except Exception as e:
            logger.warning(f"Error validating rule: {str(e)}")
            return False

    def extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text using spaCy."""
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents]

    def categorize_rule(self, rule: Rule) -> List[str]:
        """Categorize a rule based on its content."""
        categories = []
        
        # Extract entities
        entities = self.extract_entities(rule.text)
        
        # Add basic categorization based on keywords
        keywords = {
            "financial": ["payment", "budget", "expenditure", "fund", "account"],
            "procurement": ["purchase", "tender", "bid", "contract", "vendor"],
            "administrative": ["approval", "authority", "delegation", "procedure"],
            "compliance": ["compliance", "violation", "penalty", "audit"]
        }
        
        for category, words in keywords.items():
            if any(word.lower() in rule.text.lower() for word in words):
                categories.append(category)
        
        return categories 