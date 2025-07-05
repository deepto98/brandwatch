import re
from typing import List, Dict, Any, Optional
import spacy

class NLPProcessor:
    """Natural Language Processing utilities for brand analysis"""
    
    def __init__(self):
        try:
            # Try to load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback to None if spaCy model not available
            self.nlp = None
    
    def analyze_sentiment(self, text: str, brand_name: str) -> str:
        """Analyze sentiment of text related to the brand"""
        # Find brand mentions in the text
        brand_mentions = self._find_brand_mentions(text, brand_name)
        
        if not brand_mentions:
            return 'neutral'
        
        # Simple sentiment analysis using keyword matching
        positive_keywords = [
            'best', 'excellent', 'great', 'amazing', 'outstanding', 'superior',
            'top', 'leading', 'recommended', 'popular', 'reliable', 'trusted',
            'innovative', 'effective', 'efficient', 'quality', 'premium',
            'love', 'like', 'prefer', 'choose', 'select', 'winner'
        ]
        
        negative_keywords = [
            'worst', 'terrible', 'bad', 'awful', 'poor', 'inferior',
            'avoid', 'problem', 'issue', 'complaint', 'expensive',
            'slow', 'difficult', 'complicated', 'limited', 'lacking',
            'hate', 'dislike', 'disappointed', 'frustrating', 'annoying'
        ]
        
        # Analyze context around brand mentions
        sentiment_score = 0
        
        for mention in brand_mentions:
            context = self._get_context_around_mention(text, mention)
            context_lower = context.lower()
            
            # Count positive and negative words
            positive_count = sum(1 for word in positive_keywords if word in context_lower)
            negative_count = sum(1 for word in negative_keywords if word in context_lower)
            
            sentiment_score += positive_count - negative_count
        
        # Determine overall sentiment
        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text"""
        entities = []
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
        else:
            # Fallback entity extraction using patterns
            entities = self._extract_entities_fallback(text)
        
        return entities
    
    def extract_rankings(self, text: str) -> List[Dict[str, Any]]:
        """Extract ranking information from text"""
        rankings = []
        
        # Pattern for numbered lists
        numbered_pattern = r'(\d+)\.\s*([^\n]+)'
        matches = re.findall(numbered_pattern, text)
        
        for rank, content in matches:
            rankings.append({
                'rank': int(rank),
                'content': content.strip(),
                'type': 'numbered_list'
            })
        
        # Pattern for ranking words
        ranking_words = {
            'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
            'top': 1, 'best': 1, 'leading': 1, 'primary': 1
        }
        
        for word, rank in ranking_words.items():
            pattern = rf'\b{word}\b[^.]*?([A-Z][a-zA-Z\s]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                rankings.append({
                    'rank': rank,
                    'content': match.strip(),
                    'type': 'ranking_word'
                })
        
        return rankings
    
    def identify_comparison_context(self, text: str) -> List[Dict[str, Any]]:
        """Identify comparison contexts in text"""
        comparisons = []
        
        # Comparison patterns
        comparison_patterns = [
            r'(compared to|vs|versus|against)[\s\w]+',
            r'(better than|worse than|superior to|inferior to)[\s\w]+',
            r'(while|whereas|unlike|in contrast to)[\s\w]+',
            r'(alternatives to|competitors of|similar to)[\s\w]+'
        ]
        
        for pattern in comparison_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                comparisons.append({
                    'type': 'comparison',
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end()
                })
        
        return comparisons
    
    def _find_brand_mentions(self, text: str, brand_name: str) -> List[str]:
        """Find all mentions of the brand in text"""
        mentions = []
        
        # Direct mentions
        brand_pattern = re.compile(re.escape(brand_name), re.IGNORECASE)
        direct_matches = brand_pattern.findall(text)
        mentions.extend(direct_matches)
        
        # Brand variations
        variations = self._generate_brand_variations(brand_name)
        for variation in variations:
            var_pattern = re.compile(re.escape(variation), re.IGNORECASE)
            var_matches = var_pattern.findall(text)
            mentions.extend(var_matches)
        
        return mentions
    
    def _generate_brand_variations(self, brand_name: str) -> List[str]:
        """Generate variations of the brand name"""
        variations = []
        
        # Add spaces in camelCase
        spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', brand_name)
        if spaced != brand_name:
            variations.append(spaced)
        
        # Remove spaces
        no_spaces = brand_name.replace(' ', '')
        if no_spaces != brand_name:
            variations.append(no_spaces)
        
        # Abbreviations
        words = brand_name.split()
        if len(words) > 1:
            abbreviation = ''.join(word[0].upper() for word in words)
            variations.append(abbreviation)
        
        return variations
    
    def _get_context_around_mention(self, text: str, mention: str, context_size: int = 100) -> str:
        """Get context around a brand mention"""
        mention_index = text.lower().find(mention.lower())
        
        if mention_index == -1:
            return ""
        
        start = max(0, mention_index - context_size)
        end = min(len(text), mention_index + len(mention) + context_size)
        
        return text[start:end]
    
    def _extract_entities_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback entity extraction without spaCy"""
        entities = []
        
        # Company patterns
        company_patterns = [
            r'\b[A-Z][a-zA-Z]+\s+(?:Inc|Corp|Ltd|LLC|Company|Co)\b',
            r'\b[A-Z][a-zA-Z]+(?:Inc|Corp|Ltd|LLC)\b'
        ]
        
        for pattern in company_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append({
                    'text': match.group(),
                    'label': 'ORG',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Product patterns
        product_patterns = [
            r'\b[A-Z][a-zA-Z]+[A-Z][a-zA-Z]*\b',  # CamelCase words
        ]
        
        for pattern in product_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                entities.append({
                    'text': match.group(),
                    'label': 'PRODUCT',
                    'start': match.start(),
                    'end': match.end()
                })
        
        return entities
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_key_phrases(self, text: str, max_phrases: int = 10) -> List[str]:
        """Extract key phrases from text"""
        if self.nlp:
            doc = self.nlp(text)
            # Extract noun phrases
            phrases = [chunk.text for chunk in doc.noun_chunks]
        else:
            # Fallback: extract capitalized phrases
            phrases = re.findall(r'\b[A-Z][a-zA-Z\s]+\b', text)
        
        # Filter and limit phrases
        filtered_phrases = []
        for phrase in phrases:
            phrase = phrase.strip()
            if len(phrase) > 3 and len(phrase) < 50:
                filtered_phrases.append(phrase)
        
        return filtered_phrases[:max_phrases]
