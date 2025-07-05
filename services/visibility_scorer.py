from typing import Dict, List, Any
import math

class VisibilityScorer:
    """Calculates overall visibility scores and generates insights"""
    
    def __init__(self):
        self.weights = {
            'mention_frequency': 0.3,
            'ranking_position': 0.25,
            'platform_coverage': 0.20,
            'sentiment_quality': 0.15,
            'competitive_position': 0.10
        }
    
    def calculate_score(self, brand_analysis: Dict[str, Any], 
                       competitor_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive visibility score"""
        
        # Calculate individual component scores
        mention_score = self._calculate_mention_score(brand_analysis)
        ranking_score = self._calculate_ranking_score(brand_analysis)
        platform_score = self._calculate_platform_score(brand_analysis)
        sentiment_score = self._calculate_sentiment_score(brand_analysis)
        competitive_score = self._calculate_competitive_score(brand_analysis, competitor_analysis)
        
        # Calculate weighted overall score
        overall_score = (
            mention_score * self.weights['mention_frequency'] +
            ranking_score * self.weights['ranking_position'] +
            platform_score * self.weights['platform_coverage'] +
            sentiment_score * self.weights['sentiment_quality'] +
            competitive_score * self.weights['competitive_position']
        )
        
        # Generate insights and recommendations
        insights = self._generate_insights(brand_analysis, competitor_analysis)
        recommendations = self._generate_recommendations(brand_analysis, competitor_analysis)
        
        return {
            'overall_score': round(overall_score, 1),
            'component_scores': {
                'mention_frequency': round(mention_score, 1),
                'ranking_position': round(ranking_score, 1),
                'platform_coverage': round(platform_score, 1),
                'sentiment_quality': round(sentiment_score, 1),
                'competitive_position': round(competitive_score, 1)
            },
            'insights': insights,
            'recommendations': recommendations,
            'score_breakdown': self._generate_score_breakdown(
                mention_score, ranking_score, platform_score, 
                sentiment_score, competitive_score
            )
        }
    
    def _calculate_mention_score(self, brand_analysis: Dict[str, Any]) -> float:
        """Calculate score based on mention frequency"""
        total_mentions = brand_analysis['total_mentions']
        
        # Calculate total possible mentions (assuming we know the number of queries)
        total_queries = sum(
            len(responses) for responses in brand_analysis.get('platform_responses', {}).values()
        ) if 'platform_responses' in brand_analysis else 100  # Default assumption
        
        if total_queries == 0:
            return 0.0
        
        # Calculate mention rate
        mention_rate = total_mentions / total_queries
        
        # Convert to score (scale 0-100)
        # Use logarithmic scaling to avoid extreme scores
        score = min(100, mention_rate * 100 * 2)  # Multiply by 2 to make it easier to achieve higher scores
        
        return score
    
    def _calculate_ranking_score(self, brand_analysis: Dict[str, Any]) -> float:
        """Calculate score based on ranking positions"""
        avg_ranking = brand_analysis.get('average_ranking')
        
        if avg_ranking is None:
            return 0.0
        
        # Convert ranking to score (lower ranking = higher score)
        # Rank 1 = 100, Rank 2 = 85, Rank 3 = 70, etc.
        if avg_ranking <= 1:
            score = 100
        elif avg_ranking <= 2:
            score = 85
        elif avg_ranking <= 3:
            score = 70
        elif avg_ranking <= 5:
            score = 50
        elif avg_ranking <= 10:
            score = 25
        else:
            score = 10
        
        return score
    
    def _calculate_platform_score(self, brand_analysis: Dict[str, Any]) -> float:
        """Calculate score based on platform coverage"""
        platform_mentions = brand_analysis['platform_mentions']
        
        # Check how many platforms have mentions
        platforms_with_mentions = sum(1 for mentions in platform_mentions.values() if mentions > 0)
        total_platforms = len(platform_mentions)
        
        if total_platforms == 0:
            return 0.0
        
        # Base score from platform coverage
        coverage_score = (platforms_with_mentions / total_platforms) * 100
        
        # Bonus for consistent performance across platforms
        if platforms_with_mentions > 0:
            mention_values = [mentions for mentions in platform_mentions.values() if mentions > 0]
            if len(mention_values) > 1:
                # Calculate coefficient of variation (lower = more consistent)
                mean_mentions = sum(mention_values) / len(mention_values)
                std_dev = math.sqrt(sum((x - mean_mentions) ** 2 for x in mention_values) / len(mention_values))
                cv = std_dev / mean_mentions if mean_mentions > 0 else 0
                
                # Bonus for consistency (up to 20 points)
                consistency_bonus = max(0, 20 - (cv * 20))
                coverage_score = min(100, coverage_score + consistency_bonus)
        
        return coverage_score
    
    def _calculate_sentiment_score(self, brand_analysis: Dict[str, Any]) -> float:
        """Calculate score based on sentiment quality"""
        sentiment_analysis = brand_analysis.get('sentiment_analysis', {})
        
        if not sentiment_analysis:
            return 50.0  # Neutral score if no sentiment data
        
        total_positive = 0
        total_neutral = 0
        total_negative = 0
        
        for platform_sentiment in sentiment_analysis.values():
            total_positive += platform_sentiment.get('positive', 0)
            total_neutral += platform_sentiment.get('neutral', 0)
            total_negative += platform_sentiment.get('negative', 0)
        
        total_sentiment = total_positive + total_neutral + total_negative
        
        if total_sentiment == 0:
            return 50.0  # Neutral score if no sentiment data
        
        # Calculate sentiment score
        positive_ratio = total_positive / total_sentiment
        negative_ratio = total_negative / total_sentiment
        
        # Score based on sentiment distribution
        sentiment_score = (positive_ratio * 100) - (negative_ratio * 50)
        
        return max(0, min(100, sentiment_score))
    
    def _calculate_competitive_score(self, brand_analysis: Dict[str, Any], 
                                   competitor_analysis: Dict[str, Any]) -> float:
        """Calculate score based on competitive position"""
        brand_mentions = brand_analysis['total_mentions']
        
        if not competitor_analysis:
            return 50.0  # Neutral score if no competitor data
        
        # Calculate relative position
        better_than = 0
        total_competitors = len(competitor_analysis)
        
        for competitor_data in competitor_analysis.values():
            competitor_mentions = competitor_data['total_mentions']
            
            if brand_mentions > competitor_mentions:
                better_than += 1
            elif brand_mentions == competitor_mentions:
                better_than += 0.5  # Tie
        
        # Calculate competitive score
        competitive_score = (better_than / total_competitors) * 100 if total_competitors > 0 else 50
        
        return competitive_score
    
    def _generate_insights(self, brand_analysis: Dict[str, Any], 
                          competitor_analysis: Dict[str, Any]) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        # Mention frequency insights
        total_mentions = brand_analysis['total_mentions']
        if total_mentions == 0:
            insights.append("No brand mentions found across AI platforms - this indicates zero AI visibility")
        elif total_mentions < 5:
            insights.append("Low brand mention frequency suggests limited AI platform visibility")
        elif total_mentions >= 20:
            insights.append("Strong brand mention frequency indicates good AI platform visibility")
        
        # Platform performance insights
        platform_mentions = brand_analysis['platform_mentions']
        if platform_mentions:
            best_platform = max(platform_mentions, key=platform_mentions.get)
            worst_platform = min(platform_mentions, key=platform_mentions.get)
            
            insights.append(f"{best_platform.upper()} is your strongest platform with {platform_mentions[best_platform]} mentions")
            if platform_mentions[worst_platform] < platform_mentions[best_platform] * 0.5:
                insights.append(f"{worst_platform.upper()} shows significant room for improvement")
        
        # Competitive insights
        if competitor_analysis:
            top_competitor = max(competitor_analysis.items(), key=lambda x: x[1]['total_mentions'])
            if top_competitor[1]['total_mentions'] > total_mentions:
                insights.append(f"{top_competitor[0]} leads in AI visibility with {top_competitor[1]['total_mentions']} mentions")
        
        # Ranking insights
        avg_ranking = brand_analysis.get('average_ranking')
        if avg_ranking:
            if avg_ranking <= 2:
                insights.append("Excellent ranking position - typically appearing in top 2 results")
            elif avg_ranking <= 5:
                insights.append("Good ranking position but opportunity to reach top 3")
            else:
                insights.append("Low ranking position - focus needed on improving search result placement")
        
        return insights
    
    def _generate_recommendations(self, brand_analysis: Dict[str, Any], 
                                competitor_analysis: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Platform-specific recommendations
        platform_mentions = brand_analysis['platform_mentions']
        if platform_mentions:
            worst_platform = min(platform_mentions, key=platform_mentions.get)
            if platform_mentions[worst_platform] < max(platform_mentions.values()) * 0.5:
                recommendations.append(f"Develop targeted content strategy for {worst_platform.upper()} to improve visibility")
        
        # Mention frequency recommendations
        if brand_analysis['total_mentions'] < 10:
            recommendations.append("Increase content production and SEO efforts to improve AI platform indexing")
        
        # Ranking recommendations
        avg_ranking = brand_analysis.get('average_ranking')
        if avg_ranking and avg_ranking > 3:
            recommendations.append("Optimize content for featured snippets and AI-friendly formats")
        
        # Competitive recommendations
        if competitor_analysis:
            top_competitor = max(competitor_analysis.items(), key=lambda x: x[1]['total_mentions'])
            if top_competitor[1]['total_mentions'] > brand_analysis['total_mentions']:
                recommendations.append(f"Analyze {top_competitor[0]}'s content strategy and digital presence")
        
        # Sentiment recommendations
        sentiment_analysis = brand_analysis.get('sentiment_analysis', {})
        if sentiment_analysis:
            total_negative = sum(
                platform_sentiment.get('negative', 0) 
                for platform_sentiment in sentiment_analysis.values()
            )
            if total_negative > 0:
                recommendations.append("Address negative sentiment through improved brand messaging and PR")
        
        # General recommendations
        recommendations.append("Regularly monitor AI platform responses to track visibility changes")
        recommendations.append("Create AI-friendly content that answers common industry questions")
        
        return recommendations
    
    def _generate_score_breakdown(self, mention_score: float, ranking_score: float, 
                                platform_score: float, sentiment_score: float, 
                                competitive_score: float) -> Dict[str, str]:
        """Generate detailed score breakdown explanations"""
        breakdown = {}
        
        # Mention frequency breakdown
        if mention_score >= 80:
            breakdown['mention_frequency'] = "Excellent mention frequency across platforms"
        elif mention_score >= 60:
            breakdown['mention_frequency'] = "Good mention frequency with room for improvement"
        elif mention_score >= 40:
            breakdown['mention_frequency'] = "Moderate mention frequency - needs attention"
        else:
            breakdown['mention_frequency'] = "Low mention frequency - immediate action required"
        
        # Ranking breakdown
        if ranking_score >= 80:
            breakdown['ranking_position'] = "Excellent ranking positions in AI responses"
        elif ranking_score >= 60:
            breakdown['ranking_position'] = "Good ranking positions with improvement potential"
        else:
            breakdown['ranking_position'] = "Poor ranking positions - focus on SEO optimization"
        
        # Platform coverage breakdown
        if platform_score >= 80:
            breakdown['platform_coverage'] = "Strong presence across multiple AI platforms"
        elif platform_score >= 60:
            breakdown['platform_coverage'] = "Good platform coverage with some gaps"
        else:
            breakdown['platform_coverage'] = "Limited platform coverage - expand presence"
        
        # Sentiment breakdown
        if sentiment_score >= 70:
            breakdown['sentiment_quality'] = "Positive sentiment in AI responses"
        elif sentiment_score >= 50:
            breakdown['sentiment_quality'] = "Neutral sentiment - opportunity for improvement"
        else:
            breakdown['sentiment_quality'] = "Negative sentiment - address messaging issues"
        
        # Competitive breakdown
        if competitive_score >= 70:
            breakdown['competitive_position'] = "Leading competitive position"
        elif competitive_score >= 50:
            breakdown['competitive_position'] = "Competitive position with room for growth"
        else:
            breakdown['competitive_position'] = "Lagging behind competitors - strategic focus needed"
        
        return breakdown
