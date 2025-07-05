import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class DataProcessor:
    """Data processing utilities for brand analysis"""
    
    def __init__(self):
        pass
    
    def process_platform_responses(self, responses: Dict[str, List[Dict]]) -> pd.DataFrame:
        """Process platform responses into a structured DataFrame"""
        data = []
        
        for platform, platform_responses in responses.items():
            for i, response_data in enumerate(platform_responses):
                data.append({
                    'platform': platform,
                    'prompt_id': i,
                    'prompt': response_data['prompt'],
                    'response': response_data['response'],
                    'response_length': len(response_data['response']),
                    'timestamp': datetime.now().isoformat()
                })
        
        return pd.DataFrame(data)
    
    def calculate_mention_statistics(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistical metrics for brand mentions"""
        stats = {
            'total_mentions': 0,
            'platform_distribution': {},
            'mention_rate': 0.0,
            'platform_performance': {}
        }
        
        brand_analysis = analysis_data.get('brand_analysis', {})
        platform_mentions = brand_analysis.get('platform_mentions', {})
        
        # Total mentions
        stats['total_mentions'] = sum(platform_mentions.values())
        
        # Platform distribution
        if stats['total_mentions'] > 0:
            for platform, mentions in platform_mentions.items():
                stats['platform_distribution'][platform] = mentions / stats['total_mentions']
        
        # Platform performance metrics
        for platform, mentions in platform_mentions.items():
            platform_details = brand_analysis.get('platform_details', {}).get(platform, {})
            stats['platform_performance'][platform] = {
                'mentions': mentions,
                'mention_rate': platform_details.get('mention_rate', 0.0),
                'average_ranking': platform_details.get('average_ranking'),
                'performance_score': self._calculate_platform_performance_score(platform_details)
            }
        
        return stats
    
    def create_comparison_matrix(self, brand_analysis: Dict[str, Any], 
                               competitor_analysis: Dict[str, Any]) -> pd.DataFrame:
        """Create a comparison matrix for brand vs competitors"""
        data = []
        
        # Add brand data
        brand_data = {
            'entity': brand_analysis['brand_name'],
            'type': 'brand',
            'total_mentions': brand_analysis['total_mentions'],
            'average_ranking': brand_analysis.get('average_ranking', 0)
        }
        
        # Add platform-specific data
        for platform, mentions in brand_analysis['platform_mentions'].items():
            brand_data[f'{platform}_mentions'] = mentions
        
        data.append(brand_data)
        
        # Add competitor data
        for competitor, comp_data in competitor_analysis.items():
            comp_row = {
                'entity': competitor,
                'type': 'competitor',
                'total_mentions': comp_data['total_mentions'],
                'average_ranking': comp_data.get('average_ranking', 0)
            }
            
            # Add platform-specific data
            for platform, mentions in comp_data.get('platform_mentions', {}).items():
                comp_row[f'{platform}_mentions'] = mentions
            
            data.append(comp_row)
        
        return pd.DataFrame(data)
    
    def calculate_competitive_metrics(self, brand_analysis: Dict[str, Any], 
                                    competitor_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate competitive analysis metrics"""
        metrics = {
            'market_share': {},
            'competitive_position': {},
            'performance_gaps': {},
            'opportunities': []
        }
        
        brand_mentions = brand_analysis['total_mentions']
        competitor_mentions = {comp: data['total_mentions'] for comp, data in competitor_analysis.items()}
        
        # Market share calculation
        total_market_mentions = brand_mentions + sum(competitor_mentions.values())
        
        if total_market_mentions > 0:
            metrics['market_share']['brand'] = brand_mentions / total_market_mentions
            for competitor, mentions in competitor_mentions.items():
                metrics['market_share'][competitor] = mentions / total_market_mentions
        
        # Competitive position
        all_entities = [(brand_analysis['brand_name'], brand_mentions)]
        all_entities.extend(competitor_mentions.items())
        all_entities.sort(key=lambda x: x[1], reverse=True)
        
        for rank, (entity, mentions) in enumerate(all_entities, 1):
            if entity == brand_analysis['brand_name']:
                metrics['competitive_position']['rank'] = rank
                metrics['competitive_position']['total_competitors'] = len(all_entities)
                break
        
        # Performance gaps
        for competitor, mentions in competitor_mentions.items():
            gap = mentions - brand_mentions
            metrics['performance_gaps'][competitor] = {
                'mention_gap': gap,
                'gap_percentage': (gap / brand_mentions * 100) if brand_mentions > 0 else 0
            }
        
        # Identify opportunities
        for platform in brand_analysis['platform_mentions']:
            brand_platform_mentions = brand_analysis['platform_mentions'][platform]
            competitor_platform_mentions = [
                comp_data.get('platform_mentions', {}).get(platform, 0)
                for comp_data in competitor_analysis.values()
            ]
            
            if competitor_platform_mentions:
                max_competitor_mentions = max(competitor_platform_mentions)
                if brand_platform_mentions < max_competitor_mentions * 0.7:
                    metrics['opportunities'].append({
                        'platform': platform,
                        'gap': max_competitor_mentions - brand_platform_mentions,
                        'improvement_potential': 'high' if max_competitor_mentions > brand_platform_mentions * 2 else 'medium'
                    })
        
        return metrics
    
    def generate_time_series_data(self, analysis_data: Dict[str, Any]) -> pd.DataFrame:
        """Generate time series data for tracking (placeholder for future implementation)"""
        # This would be used for tracking changes over time
        # For now, create a single data point
        data = {
            'timestamp': datetime.now(),
            'overall_score': analysis_data.get('visibility_score', {}).get('overall_score', 0),
            'total_mentions': analysis_data.get('brand_analysis', {}).get('total_mentions', 0),
            'average_ranking': analysis_data.get('brand_analysis', {}).get('average_ranking', 0)
        }
        
        # Add platform-specific data
        platform_mentions = analysis_data.get('brand_analysis', {}).get('platform_mentions', {})
        for platform, mentions in platform_mentions.items():
            data[f'{platform}_mentions'] = mentions
        
        return pd.DataFrame([data])
    
    def export_analysis_report(self, analysis_data: Dict[str, Any], 
                             brand_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Export complete analysis report"""
        report = {
            'metadata': {
                'brand_name': brand_profile['brand_name'],
                'industry': brand_profile['industry'],
                'analysis_date': datetime.now().isoformat(),
                'platforms_analyzed': brand_profile['platforms'],
                'competitors_analyzed': brand_profile['competitors']
            },
            'executive_summary': {
                'overall_score': analysis_data.get('visibility_score', {}).get('overall_score', 0),
                'total_mentions': analysis_data.get('brand_analysis', {}).get('total_mentions', 0),
                'market_position': self._calculate_market_position(analysis_data),
                'key_findings': analysis_data.get('visibility_score', {}).get('insights', [])
            },
            'detailed_analysis': {
                'brand_analysis': analysis_data.get('brand_analysis', {}),
                'competitor_analysis': analysis_data.get('competitor_analysis', {}),
                'visibility_score': analysis_data.get('visibility_score', {})
            },
            'recommendations': analysis_data.get('visibility_score', {}).get('recommendations', [])
        }
        
        return report
    
    def _calculate_platform_performance_score(self, platform_details: Dict[str, Any]) -> float:
        """Calculate performance score for a platform"""
        mentions = platform_details.get('mentions', 0)
        mention_rate = platform_details.get('mention_rate', 0.0)
        avg_ranking = platform_details.get('average_ranking')
        
        # Base score from mentions and mention rate
        base_score = mention_rate * 100
        
        # Ranking bonus (lower ranking = higher bonus)
        ranking_bonus = 0
        if avg_ranking:
            if avg_ranking <= 2:
                ranking_bonus = 20
            elif avg_ranking <= 3:
                ranking_bonus = 10
            elif avg_ranking <= 5:
                ranking_bonus = 5
        
        total_score = min(100, base_score + ranking_bonus)
        return round(total_score, 1)
    
    def _calculate_market_position(self, analysis_data: Dict[str, Any]) -> str:
        """Calculate market position description"""
        score = analysis_data.get('visibility_score', {}).get('overall_score', 0)
        
        if score >= 80:
            return "Market Leader"
        elif score >= 60:
            return "Strong Competitor"
        elif score >= 40:
            return "Emerging Player"
        else:
            return "Niche Presence"
    
    def calculate_trend_analysis(self, current_data: Dict[str, Any], 
                               historical_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate trend analysis (placeholder for future implementation)"""
        # This would compare current data with historical data
        # For now, return current metrics
        return {
            'current_score': current_data.get('visibility_score', {}).get('overall_score', 0),
            'trend': 'stable',  # Would be calculated from historical data
            'growth_rate': 0.0,  # Would be calculated from historical data
            'insights': ['Baseline analysis completed - historical tracking will begin']
        }
