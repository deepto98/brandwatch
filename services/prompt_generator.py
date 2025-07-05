import random
from typing import List, Dict, Optional
from config.industries import INDUSTRIES

class PromptGenerator:
    """Generates industry-specific prompts for brand visibility analysis"""
    
    def __init__(self):
        self.prompt_templates = {
            'direct_comparison': [
                "What are the best {industry} companies in {region}?",
                "Which {industry} platforms should I choose in {region}?",
                "Compare the top {industry} services available in {region}",
                "List the leading {industry} providers in {region}"
            ],
            'recommendation': [
                "I need recommendations for {industry} solutions in {region}",
                "What {industry} service would you recommend for a {business_type} in {region}?",
                "Help me choose the right {industry} platform in {region}",
                "Which {industry} company offers the best value in {region}?"
            ],
            'problem_solving': [
                "How can I solve {pain_point} using {industry} services in {region}?",
                "What's the best way to {action} in {industry} in {region}?",
                "I'm looking for {industry} solutions in {region} that can help with {need}",
                "How do I choose the right {industry} provider for {use_case} in {region}?"
            ],
            'feature_specific': [
                "Which {industry} companies in {region} offer {feature}?",
                "What {industry} platforms in {region} have the best {capability}?",
                "Compare {feature} across different {industry} providers in {region}",
                "Find {industry} services in {region} with strong {benefit}"
            ],
            'buying_journey': [
                "How do I get started with {industry} services in {region}?",
                "What should I look for when choosing {industry} providers in {region}?",
                "Steps to implement {industry} solutions in my business in {region}",
                "Beginner's guide to {industry} platforms in {region}"
            ]
        }
        
        # Location-agnostic templates for when no location is specified
        self.generic_templates = {
            'direct_comparison': [
                "What are the best {industry} companies?",
                "Which {industry} platforms should I choose?",
                "Compare the top {industry} services available today",
                "List the leading {industry} providers"
            ],
            'recommendation': [
                "I need recommendations for {industry} solutions",
                "What {industry} service would you recommend for a {business_type}?",
                "Help me choose the right {industry} platform",
                "Which {industry} company offers the best value?"
            ],
            'problem_solving': [
                "How can I solve {pain_point} using {industry} services?",
                "What's the best way to {action} in {industry}?",
                "I'm looking for {industry} solutions that can help with {need}",
                "How do I choose the right {industry} provider for {use_case}?"
            ],
            'feature_specific': [
                "Which {industry} companies offer {feature}?",
                "What {industry} platforms have the best {capability}?",
                "Compare {feature} across different {industry} providers",
                "Find {industry} services with strong {benefit}"
            ],
            'buying_journey': [
                "How do I get started with {industry} services?",
                "What should I look for when choosing {industry} providers?",
                "Steps to implement {industry} solutions in my business",
                "Beginner's guide to {industry} platforms"
            ]
        }
    
    def generate_prompts(self, industry: str, count: int = 20, location: Optional[str] = None, is_custom: bool = False) -> List[str]:
        """Generate industry-specific prompts"""
        if is_custom:
            # Generate custom industry config
            industry_config = self._generate_custom_industry_config(industry, location)
        else:
            if industry not in INDUSTRIES:
                raise ValueError(f"Industry {industry} not supported")
            industry_config = INDUSTRIES[industry].copy()
            
            # Add location to regions if provided
            if location:
                if 'regions' in industry_config:
                    # Add the specific location to the front of regions list
                    industry_config['regions'] = [location] + [r for r in industry_config['regions'] if r != location]
                else:
                    industry_config['regions'] = [location, 'globally', 'internationally']
        
        prompts = []
        
        # Determine which templates to use based on location availability
        templates_to_use = self.prompt_templates if location else self.generic_templates
        
        # Distribute prompts across different categories
        categories = list(templates_to_use.keys())
        prompts_per_category = max(1, count // len(categories))
        
        for category in categories:
            category_prompts = self._generate_category_prompts(
                category, industry_config, prompts_per_category, has_location=bool(location)
            )
            prompts.extend(category_prompts)
        
        # Add extra prompts if needed
        while len(prompts) < count:
            category = random.choice(categories)
            extra_prompt = self._generate_category_prompts(
                category, industry_config, 1, has_location=bool(location)
            )
            prompts.extend(extra_prompt)
        
        # Validate prompts include location when specified
        final_prompts = []
        for prompt in prompts[:count]:
            # If location is provided and not in prompt, try to add it
            if location and location not in prompt:
                # Try to add location context at the end
                if prompt.endswith('?'):
                    prompt = prompt[:-1] + f" in {location}?"
                else:
                    prompt = prompt + f" in {location}"
            final_prompts.append(prompt)
        
        return final_prompts
    
    def _generate_category_prompts(self, category: str, industry_config: Dict, count: int, has_location: bool = True) -> List[str]:
        """Generate prompts for a specific category"""
        # Use location-aware templates if location is provided, otherwise use generic templates
        templates = self.prompt_templates[category] if has_location else self.generic_templates[category]
        prompts = []
        
        for _ in range(count):
            template = random.choice(templates)
            prompt = self._fill_template(template, industry_config)
            prompts.append(prompt)
        
        return prompts
    
    def _fill_template(self, template: str, industry_config: Dict) -> str:
        """Fill a template with industry-specific information"""
        # Replace placeholders with industry-specific terms
        replacements = {
            'industry': random.choice(industry_config['terms']),
            'region': random.choice(industry_config['regions']),
            'business_type': random.choice(industry_config['business_types']),
            'pain_point': random.choice(industry_config['pain_points']),
            'action': random.choice(industry_config['actions']),
            'need': random.choice(industry_config['needs']),
            'use_case': random.choice(industry_config['use_cases']),
            'feature': random.choice(industry_config['features']),
            'capability': random.choice(industry_config['capabilities']),
            'benefit': random.choice(industry_config['benefits'])
        }
        
        # Replace placeholders in template
        filled_template = template
        for placeholder, value in replacements.items():
            filled_template = filled_template.replace(f'{{{placeholder}}}', value)
        
        return filled_template
    
    def generate_competitor_analysis_prompts(self, industry: str, brand_name: str, competitors: List[str], location: Optional[str] = None) -> List[str]:
        """Generate prompts specifically for competitor analysis"""
        if industry in INDUSTRIES:
            industry_config = INDUSTRIES[industry]
        else:
            # Custom industry
            industry_config = self._generate_custom_industry_config(industry, location)
            
        competitor_prompts = []
        
        # Direct comparison prompts
        competitor_prompts.extend([
            f"Compare {brand_name} vs {competitor}" + (f" in {location}" if location else "") for competitor in competitors
        ])
        
        # Feature comparison prompts
        features = industry_config.get('features', ['quality', 'price', 'service'])[:3]
        for feature in features:
            prompt = f"Which is better for {feature}: {brand_name} or {random.choice(competitors)}?"
            if location:
                prompt = prompt[:-1] + f" in {location}?"
            competitor_prompts.append(prompt)
        
        # Market position prompts
        competitor_prompts.extend([
            f"What are the advantages of {brand_name} over {competitor}" + (f" in {location}" if location else "") + "?" for competitor in competitors[:2]
        ])
        
        return competitor_prompts
    
    def validate_prompts(self, prompts: List[str]) -> List[str]:
        """Validate and clean generated prompts"""
        valid_prompts = []
        
        for prompt in prompts:
            # Remove prompts with unfilled placeholders
            if '{' not in prompt and '}' not in prompt:
                # Remove duplicates
                if prompt not in valid_prompts:
                    valid_prompts.append(prompt)
        
        return valid_prompts
    
    def _generate_custom_industry_config(self, industry_name: str, location: Optional[str] = None) -> Dict:
        """Generate configuration for custom industries"""
        regions = ['globally', 'internationally', 'in the market']
        if location:
            regions = [location] + regions
        
        return {
            'terms': [industry_name.lower(), industry_name, f'{industry_name} solutions', f'{industry_name} services'],
            'regions': regions,
            'business_types': [
                'startup', 'enterprise', 'small business', 'individual',
                'corporation', 'SME', 'organization', 'company'
            ],
            'pain_points': [
                'high costs', 'inefficiency', 'poor service quality',
                'limited options', 'complex processes', 'lack of transparency',
                'scalability issues', 'integration challenges'
            ],
            'actions': [
                'find solutions', 'compare options', 'get services', 'improve processes',
                'reduce costs', 'increase efficiency', 'solve problems', 'get started'
            ],
            'needs': [
                'better solutions', 'cost optimization', 'process improvement',
                'quality service', 'reliable providers', 'trusted partners',
                'innovative approaches', 'competitive advantage'
            ],
            'use_cases': [
                'business operations', 'service delivery', 'customer needs',
                'market requirements', 'industry challenges', 'growth objectives',
                'efficiency goals', 'competitive positioning'
            ],
            'features': [
                'quality service', 'competitive pricing', 'reliability',
                'customer support', 'innovation', 'flexibility',
                'scalability', 'expertise'
            ],
            'capabilities': [
                'service delivery', 'problem solving', 'customer satisfaction',
                'operational excellence', 'market expertise', 'industry knowledge',
                'proven track record', 'professional service'
            ],
            'benefits': [
                'cost savings', 'better outcomes', 'improved efficiency',
                'competitive advantage', 'customer satisfaction', 'growth potential',
                'market leadership', 'operational excellence'
            ]
        }
