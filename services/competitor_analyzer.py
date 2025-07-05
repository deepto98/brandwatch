from typing import Dict, List, Any
from utils.nlp_processor import NLPProcessor
from services.brand_analyzer import BrandAnalyzer
from concurrent.futures import ThreadPoolExecutor, as_completed

class CompetitorAnalyzer:
    """Analyzes competitor mentions and performance"""
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.brand_analyzer = BrandAnalyzer()
        
    def analyze_competitors(self, platform_responses: Dict[str, List[Dict]], competitors: List[str]) -> Dict[str, Any]:
        """Analyze competitor mentions across all platforms - now with concurrency"""
        competitor_analysis = {}
        
        # Use ThreadPoolExecutor to analyze competitors in parallel
        with ThreadPoolExecutor(max_workers=min(len(competitors), 5)) as executor:
            # Submit all competitor analysis tasks
            future_to_competitor = {
                executor.submit(self._analyze_single_competitor, platform_responses, competitor): competitor
                for competitor in competitors
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_competitor):
                competitor = future_to_competitor[future]
                try:
                    result = future.result()
                    competitor_analysis[competitor] = result
                except Exception as e:
                    print(f"Error analyzing competitor {competitor}: {str(e)}")
                    # Provide fallback data in case of error
                    competitor_analysis[competitor] = {
                        'name': competitor,
                        'total_mentions': 0,
                        'platform_mentions': {},
                        'average_ranking': None,
                        'mention_contexts': [],
                        'sentiment_analysis': {},
                        'visibility_score': 0
                    }
        
        return competitor_analysis
    
    def _analyze_single_competitor(self, platform_responses: Dict[str, List[Dict]], competitor: str) -> Dict[str, Any]:
        """Analyze a single competitor's performance"""
        # Use the brand analyzer to analyze this competitor as if it were a brand
        competitor_results = self.brand_analyzer.analyze_mentions(platform_responses, competitor)
        
        # Transform results to competitor-specific format
        competitor_analysis = {
            'name': competitor,
            'total_mentions': competitor_results['total_mentions'],
            'platform_mentions': competitor_results['platform_mentions'],
            'average_ranking': competitor_results['average_ranking'],
            'mention_contexts': competitor_results['mention_contexts'],
            'sentiment_analysis': competitor_results['sentiment_analysis'],
            'visibility_score': self.brand_analyzer.calculate_brand_visibility_score(competitor_results)
        }
        
        return competitor_analysis
    
    def generate_competitive_insights(self, brand_analysis: Dict[str, Any], 
                                    competitor_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive insights and recommendations"""
        insights = {
            'market_position': self._analyze_market_position(brand_analysis, competitor_analysis),
            'platform_performance': self._analyze_platform_performance(brand_analysis, competitor_analysis),
            'opportunities': self._identify_opportunities(brand_analysis, competitor_analysis),
            'threats': self._identify_threats(brand_analysis, competitor_analysis),
            'recommendations': self._generate_recommendations(brand_analysis, competitor_analysis)
        }
        
        return insights
    
    def _analyze_market_position(self, brand_analysis: Dict[str, Any], 
                               competitor_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market position relative to competitors"""
        brand_mentions = brand_analysis['total_mentions']
        brand_ranking = brand_analysis['average_ranking'] or float('inf')
        
        # Calculate position metrics
        better_than = 0
        worse_than = 0
        total_competitors = len(competitor_analysis)
        
        for competitor, comp_data in competitor_analysis.items():
            comp_mentions = comp_data['total_mentions']
            comp_ranking = comp_data['average_ranking'] or float('inf')
            
            # Compare mentions
            if brand_mentions > comp_mentions:
                better_than += 1
            elif brand_mentions < comp_mentions:
                worse_than += 1
            
            # Compare rankings (lower is better)
            if brand_ranking < comp_ranking:
                better_than += 0.5
            elif brand_ranking > comp_ranking:
                worse_than += 0.5
        
        position_score = (better_than / (total_competitors * 1.5)) * 100 if total_competitors > 0 else 0
        
        return {
            'position_score': round(position_score, 1),
            'better_than_count': int(better_than),
            'worse_than_count': int(worse_than),
            'market_rank': self._calculate_market_rank(brand_analysis, competitor_analysis)
        }
    
    def _analyze_platform_performance(self, brand_analysis: Dict[str, Any], 
                                    competitor_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance across different platforms"""
        platform_performance = {}
        
        for platform in brand_analysis['platform_mentions'].keys():
            brand_mentions = brand_analysis['platform_mentions'][platform]
            
            # Compare with competitors on this platform
            competitor_mentions = []
            for competitor, comp_data in competitor_analysis.items():
                comp_mentions = comp_data['platform_mentions'].get(platform, 0)
                competitor_mentions.append(comp_mentions)
            
            if competitor_mentions:
                avg_competitor_mentions = sum(competitor_mentions) / len(competitor_mentions)
                performance_ratio = brand_mentions / avg_competitor_mentions if avg_competitor_mentions > 0 else 0
                
                platform_performance[platform] = {
                    'brand_mentions': brand_mentions,
                    'avg_competitor_mentions': avg_competitor_mentions,
                    'performance_ratio': performance_ratio,
                    'status': 'leading' if performance_ratio > 1.2 else 'competitive' if performance_ratio > 0.8 else 'lagging'
                }
        
        return platform_performance
    
    def _identify_opportunities(self, brand_analysis: Dict[str, Any], 
                              competitor_analysis: Dict[str, Any]) -> List[str]:
        """Identify opportunities for improvement"""
        opportunities = []
        
        # Platform-specific opportunities
        for platform, brand_mentions in brand_analysis['platform_mentions'].items():
            competitor_mentions = []
            for comp_data in competitor_analysis.values():
                competitor_mentions.append(comp_data['platform_mentions'].get(platform, 0))
            
            if competitor_mentions:
                max_competitor_mentions = max(competitor_mentions)
                if brand_mentions < max_competitor_mentions * 0.7:
                    opportunities.append(f"Improve presence on {platform.upper()} - competitors are performing significantly better")
        
        # Ranking opportunities
        if brand_analysis['average_ranking'] and brand_analysis['average_ranking'] > 3:
            opportunities.append("Focus on improving search result rankings - currently not in top 3")
        
        # Sentiment opportunities
        total_negative = sum(
            sentiment_data.get('negative', 0) 
            for sentiment_data in brand_analysis['sentiment_analysis'].values()
        )
        if total_negative > 0:
            opportunities.append("Address negative sentiment in AI responses")
        
        return opportunities
    
    def _identify_threats(self, brand_analysis: Dict[str, Any], 
                         competitor_analysis: Dict[str, Any]) -> List[str]:
        """Identify competitive threats"""
        threats = []
        
        # Strong competitors
        for competitor, comp_data in competitor_analysis.items():
            if comp_data['total_mentions'] > brand_analysis['total_mentions'] * 1.5:
                threats.append(f"{competitor} has significantly higher mention frequency")
            
            if (comp_data['average_ranking'] and brand_analysis['average_ranking'] and 
                comp_data['average_ranking'] < brand_analysis['average_ranking'] - 1):
                threats.append(f"{competitor} consistently ranks higher in AI responses")
        
        # Market position threats
        brand_mentions = brand_analysis['total_mentions']
        if brand_mentions == 0:
            threats.append("No brand mentions found - complete lack of AI visibility")
        
        return threats
    
    def _generate_recommendations(self, brand_analysis: Dict[str, Any], 
                                competitor_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Platform-specific recommendations
        weakest_platform = min(
            brand_analysis['platform_mentions'].items(), 
            key=lambda x: x[1]
        )[0]
        recommendations.append(f"Prioritize content strategy for {weakest_platform.upper()} platform")
        
        # Competitor-based recommendations
        top_competitor = max(
            competitor_analysis.items(), 
            key=lambda x: x[1]['total_mentions']
        )[0]
        recommendations.append(f"Study {top_competitor}'s content strategy and positioning")
        
        # SEO and content recommendations
        if brand_analysis['average_ranking'] and brand_analysis['average_ranking'] > 2:
            recommendations.append("Optimize content for AI training data to improve ranking positions")
        
        # Sentiment recommendations
        total_sentiment = sum(
            sum(sentiment_data.values()) 
            for sentiment_data in brand_analysis['sentiment_analysis'].values()
        )
        if total_sentiment > 0:
            positive_ratio = sum(
                sentiment_data.get('positive', 0) 
                for sentiment_data in brand_analysis['sentiment_analysis'].values()
            ) / total_sentiment
            
            if positive_ratio < 0.6:
                recommendations.append("Improve brand messaging to increase positive sentiment in AI responses")
        
        return recommendations
    
    def _calculate_market_rank(self, brand_analysis: Dict[str, Any], 
                             competitor_analysis: Dict[str, Any]) -> int:
        """Calculate market rank based on total mentions"""
        all_entities = [(brand_analysis['brand_name'], brand_analysis['total_mentions'])]
        
        for competitor, comp_data in competitor_analysis.items():
            all_entities.append((competitor, comp_data['total_mentions']))
        
        # Sort by mentions (descending)
        all_entities.sort(key=lambda x: x[1], reverse=True)
        
        # Find brand's position
        for rank, (entity, mentions) in enumerate(all_entities, 1):
            if entity == brand_analysis['brand_name']:
                return rank
        
        return len(all_entities)
