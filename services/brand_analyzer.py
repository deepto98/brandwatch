import re
from typing import Dict, List, Any, Optional
from utils.nlp_processor import NLPProcessor
from utils.data_processor import DataProcessor

class BrandAnalyzer:
    """Analyzes brand mentions in AI platform responses"""
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.data_processor = DataProcessor()
        
    def analyze_mentions(self, platform_responses: Dict[str, List[Dict]], brand_name: str) -> Dict[str, Any]:
        """Analyze brand mentions across all platform responses"""
        analysis_results = {
            'brand_name': brand_name,
            'platform_mentions': {},
            'platform_details': {},
            'total_mentions': 0,
            'average_ranking': None,
            'mention_contexts': [],
            'sentiment_analysis': {}
        }
        
        all_rankings = []
        
        for platform, responses in platform_responses.items():
            platform_analysis = self._analyze_platform_mentions(responses, brand_name)
            
            analysis_results['platform_mentions'][platform] = platform_analysis['mentions']
            analysis_results['platform_details'][platform] = platform_analysis
            analysis_results['total_mentions'] += platform_analysis['mentions']
            
            # Collect rankings for average calculation
            if platform_analysis['rankings']:
                all_rankings.extend(platform_analysis['rankings'])
            
            # Collect mention contexts
            analysis_results['mention_contexts'].extend(platform_analysis['mention_contexts'])
            
            # Sentiment analysis
            analysis_results['sentiment_analysis'][platform] = platform_analysis['sentiment']
        
        # Calculate average ranking (as integer)
        if all_rankings:
            analysis_results['average_ranking'] = round(sum(all_rankings) / len(all_rankings))
        
        return analysis_results
    
    def _analyze_platform_mentions(self, responses: List[Dict], brand_name: str) -> Dict[str, Any]:
        """Analyze brand mentions for a specific platform"""
        platform_analysis = {
            'mentions': 0,
            'rankings': [],
            'mention_contexts': [],
            'sentiment': {'positive': 0, 'neutral': 0, 'negative': 0},
            'mention_rate': 0.0,
            'average_ranking': None,
            'sample_mentions': []
        }
        
        total_responses = len(responses)
        
        for response_data in responses:
            response_text = response_data['response']
            prompt = response_data['prompt']
            
            # Check for brand mentions
            mentions = self._find_brand_mentions(response_text, brand_name)
            
            if mentions:
                # Count this as ONE mention regardless of how many times the brand appears
                platform_analysis['mentions'] += 1
                
                # Analyze ranking if this is a list/comparison response
                ranking = self._extract_ranking(response_text, brand_name)
                if ranking:
                    platform_analysis['rankings'].append(ranking)
                
                # Extract mention context
                for mention in mentions:
                    context = self._extract_mention_context(response_text, mention)
                    platform_analysis['mention_contexts'].append({
                        'prompt': prompt,
                        'mention': mention,
                        'context': context,
                        'platform': response_data.get('platform', 'unknown')
                    })
                
                # Sentiment analysis
                sentiment = self.nlp_processor.analyze_sentiment(response_text, brand_name)
                platform_analysis['sentiment'][sentiment] += 1
                
                # Store sample mentions
                if len(platform_analysis['sample_mentions']) < 5:
                    platform_analysis['sample_mentions'].append({
                        'prompt': prompt,
                        'response': response_text,
                        'mentions': mentions
                    })
        
        # Calculate metrics
        platform_analysis['mention_rate'] = platform_analysis['mentions'] / total_responses if total_responses > 0 else 0
        
        if platform_analysis['rankings']:
            platform_analysis['average_ranking'] = sum(platform_analysis['rankings']) / len(platform_analysis['rankings'])
        
        return platform_analysis
    
    def _find_brand_mentions(self, text: str, brand_name: str) -> List[str]:
        """Find all mentions of the brand in the text"""
        mentions = []
        
        # Direct brand name mentions
        brand_pattern = re.compile(re.escape(brand_name), re.IGNORECASE)
        direct_mentions = brand_pattern.findall(text)
        mentions.extend(direct_mentions)
        
        # Brand name variations (e.g., "PolicyBazaar" -> "Policy Bazaar")
        brand_variations = self._generate_brand_variations(brand_name)
        for variation in brand_variations:
            variation_pattern = re.compile(re.escape(variation), re.IGNORECASE)
            variation_mentions = variation_pattern.findall(text)
            mentions.extend(variation_mentions)
        
        return mentions
    
    def _generate_brand_variations(self, brand_name: str) -> List[str]:
        """Generate possible variations of the brand name"""
        variations = []
        
        # Add space between camelCase
        spaced_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', brand_name)
        if spaced_name != brand_name:
            variations.append(spaced_name)
        
        # Common abbreviations
        words = brand_name.split()
        if len(words) > 1:
            # First letter of each word
            abbreviation = ''.join(word[0].upper() for word in words)
            variations.append(abbreviation)
        
        return variations
    
    def _extract_ranking(self, text: str, brand_name: str) -> Optional[int]:
        """Extract ranking position of the brand in the response"""
        # Look for numbered lists or ranking indicators
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if brand_name.lower() in line.lower():
                # Check for numbered list patterns
                number_match = re.search(r'^(\d+)\.', line.strip())
                if number_match:
                    return int(number_match.group(1))
                
                # Check for ranking words
                ranking_patterns = [
                    r'(?:first|#1|number one)',
                    r'(?:second|#2|number two)',
                    r'(?:third|#3|number three)',
                    r'(?:fourth|#4|number four)',
                    r'(?:fifth|#5|number five)'
                ]
                
                for rank, pattern in enumerate(ranking_patterns, 1):
                    if re.search(pattern, line.lower()):
                        return rank
        
        return None
    
    def _extract_mention_context(self, text: str, mention: str) -> str:
        """Extract context around a brand mention"""
        # Find the mention in the text
        mention_index = text.lower().find(mention.lower())
        
        if mention_index == -1:
            return ""
        
        # Extract context (50 characters before and after)
        start = max(0, mention_index - 50)
        end = min(len(text), mention_index + len(mention) + 50)
        
        context = text[start:end]
        
        # Clean up the context
        context = context.strip()
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
        
        return context
    
    def calculate_brand_visibility_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate overall brand visibility score"""
        total_possible_mentions = sum(
            len(responses) for responses in analysis_results.get('platform_responses', {}).values()
        )
        
        if total_possible_mentions == 0:
            return 0.0
        
        # Base score from mention frequency
        mention_score = (analysis_results['total_mentions'] / total_possible_mentions) * 100
        
        # Ranking bonus (lower rankings are better)
        ranking_bonus = 0
        if analysis_results['average_ranking']:
            # Give bonus for top 3 positions
            if analysis_results['average_ranking'] <= 3:
                ranking_bonus = 20 - (analysis_results['average_ranking'] * 5)
        
        # Sentiment bonus
        sentiment_bonus = 0
        total_sentiment = sum(analysis_results['sentiment_analysis'].get(platform, {}).values() 
                            for platform in analysis_results['sentiment_analysis'])
        if total_sentiment > 0:
            positive_ratio = sum(analysis_results['sentiment_analysis'].get(platform, {}).get('positive', 0) 
                               for platform in analysis_results['sentiment_analysis']) / total_sentiment
            sentiment_bonus = positive_ratio * 10
        
        # Calculate final score
        final_score = min(100, mention_score + ranking_bonus + sentiment_bonus)
        
        return round(final_score, 1)
