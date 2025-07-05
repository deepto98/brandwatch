"""Industry-specific configurations for prompt generation"""

INDUSTRIES = {
    'FinTech': {
        'terms': [
            'fintech', 'financial technology', 'digital banking', 'mobile payments',
            'cryptocurrency', 'blockchain', 'digital wallet', 'peer-to-peer lending',
            'robo-advisory', 'insurtech', 'regtech', 'neobank'
        ],
        'regions': [
            'India', 'Asia', 'globally', 'internationally', 'domestically',
            'in emerging markets', 'in developed markets'
        ],
        'business_types': [
            'startup', 'enterprise', 'small business', 'individual',
            'corporation', 'SME', 'freelancer', 'family business'
        ],
        'pain_points': [
            'high transaction fees', 'slow transfers', 'poor customer service',
            'limited access to credit', 'complex onboarding', 'security concerns',
            'regulatory compliance', 'lack of transparency'
        ],
        'actions': [
            'transfer money', 'invest funds', 'get a loan', 'open an account',
            'make payments', 'manage finances', 'build credit', 'save money'
        ],
        'needs': [
            'financial inclusion', 'cost reduction', 'process automation',
            'risk management', 'compliance support', 'customer acquisition',
            'data analytics', 'mobile-first solutions'
        ],
        'use_cases': [
            'international remittances', 'business banking', 'personal finance',
            'investment management', 'payment processing', 'credit scoring',
            'fraud detection', 'regulatory reporting'
        ],
        'features': [
            'real-time payments', 'multi-currency support', 'AI-powered insights',
            'mobile app', 'API integration', 'security features', 'analytics dashboard',
            'customer support', 'compliance tools'
        ],
        'capabilities': [
            'fraud detection', 'risk assessment', 'automated underwriting',
            'real-time processing', 'cross-border payments', 'digital identity',
            'smart contracts', 'predictive analytics'
        ],
        'benefits': [
            'cost savings', 'faster processing', 'better security', 'improved accessibility',
            'enhanced user experience', 'regulatory compliance', 'scalability',
            'transparency', 'financial inclusion'
        ]
    },
    
    'E-commerce': {
        'terms': [
            'e-commerce', 'online shopping', 'digital marketplace', 'retail platform',
            'online store', 'shopping cart', 'payment gateway', 'inventory management',
            'dropshipping', 'omnichannel', 'social commerce', 'mobile commerce'
        ],
        'regions': [
            'India', 'Asia-Pacific', 'globally', 'North America', 'Europe',
            'emerging markets', 'tier-2 cities', 'rural areas'
        ],
        'business_types': [
            'retailer', 'marketplace', 'brand', 'wholesaler', 'distributor',
            'manufacturer', 'startup', 'enterprise', 'small business'
        ],
        'pain_points': [
            'high cart abandonment', 'poor conversion rates', 'inventory management',
            'shipping delays', 'customer acquisition costs', 'return management',
            'payment failures', 'competition'
        ],
        'actions': [
            'increase sales', 'reduce costs', 'improve customer experience',
            'expand market reach', 'optimize inventory', 'enhance security',
            'boost conversions', 'streamline operations'
        ],
        'needs': [
            'customer acquisition', 'retention strategies', 'supply chain optimization',
            'payment processing', 'fraud prevention', 'mobile optimization',
            'personalization', 'analytics and insights'
        ],
        'use_cases': [
            'B2B marketplace', 'B2C retail', 'fashion e-commerce', 'electronics store',
            'grocery delivery', 'subscription commerce', 'digital products',
            'international selling'
        ],
        'features': [
            'product catalog', 'search functionality', 'payment integration',
            'shipping management', 'customer reviews', 'wish lists',
            'recommendation engine', 'mobile app'
        ],
        'capabilities': [
            'inventory tracking', 'order management', 'customer analytics',
            'marketing automation', 'multi-channel selling', 'price optimization',
            'fraud detection', 'personalization'
        ],
        'benefits': [
            'increased revenue', 'better customer experience', 'operational efficiency',
            'market expansion', 'cost reduction', 'data-driven insights',
            'scalability', 'competitive advantage'
        ]
    },
    
    'SaaS': {
        'terms': [
            'SaaS', 'software as a service', 'cloud software', 'business software',
            'enterprise software', 'productivity tools', 'collaboration platform',
            'CRM', 'project management', 'automation tools'
        ],
        'regions': [
            'globally', 'North America', 'Europe', 'Asia-Pacific', 'India',
            'enterprise markets', 'SMB segment', 'remote teams'
        ],
        'business_types': [
            'startup', 'enterprise', 'SMB', 'remote team', 'agency',
            'consultancy', 'freelancer', 'corporation', 'non-profit'
        ],
        'pain_points': [
            'manual processes', 'data silos', 'poor collaboration', 'scalability issues',
            'integration challenges', 'security concerns', 'high costs',
            'user adoption', 'customization needs'
        ],
        'actions': [
            'automate workflows', 'improve collaboration', 'integrate systems',
            'scale operations', 'reduce costs', 'enhance security',
            'increase productivity', 'streamline processes'
        ],
        'needs': [
            'process automation', 'team collaboration', 'data integration',
            'scalability', 'security compliance', 'user training',
            'custom workflows', 'analytics and reporting'
        ],
        'use_cases': [
            'customer relationship management', 'project management',
            'team collaboration', 'marketing automation', 'sales enablement',
            'HR management', 'financial planning', 'business intelligence'
        ],
        'features': [
            'user interface', 'API integration', 'mobile access', 'reporting dashboard',
            'user management', 'data backup', 'customization options',
            'third-party integrations'
        ],
        'capabilities': [
            'workflow automation', 'data analytics', 'real-time collaboration',
            'scalable infrastructure', 'security features', 'integration options',
            'customization', 'mobile support'
        ],
        'benefits': [
            'increased productivity', 'cost savings', 'better collaboration',
            'improved efficiency', 'scalability', 'data insights',
            'competitive advantage', 'reduced IT overhead'
        ]
    },
    
    'Healthcare': {
        'terms': [
            'healthcare', 'medical technology', 'telemedicine', 'health tech',
            'digital health', 'electronic health records', 'patient management',
            'medical devices', 'healthcare analytics', 'clinical software'
        ],
        'regions': [
            'India', 'globally', 'developed countries', 'emerging markets',
            'rural areas', 'urban centers', 'healthcare systems'
        ],
        'business_types': [
            'hospital', 'clinic', 'healthcare provider', 'pharmaceutical company',
            'medical practice', 'healthcare startup', 'research institution',
            'government health department'
        ],
        'pain_points': [
            'patient data management', 'appointment scheduling', 'billing complexity',
            'regulatory compliance', 'staff efficiency', 'patient engagement',
            'interoperability issues', 'cost management'
        ],
        'actions': [
            'improve patient care', 'streamline operations', 'reduce costs',
            'enhance efficiency', 'ensure compliance', 'increase accessibility',
            'optimize workflows', 'improve outcomes'
        ],
        'needs': [
            'patient management', 'clinical decision support', 'regulatory compliance',
            'data security', 'interoperability', 'cost reduction',
            'workflow optimization', 'patient engagement'
        ],
        'use_cases': [
            'electronic health records', 'telemedicine consultations',
            'appointment scheduling', 'medical billing', 'patient monitoring',
            'clinical research', 'pharmaceutical management', 'health analytics'
        ],
        'features': [
            'patient records', 'appointment booking', 'prescription management',
            'billing system', 'clinical notes', 'lab integration',
            'patient portal', 'mobile access'
        ],
        'capabilities': [
            'data analytics', 'clinical decision support', 'patient monitoring',
            'regulatory reporting', 'interoperability', 'security features',
            'mobile health', 'AI-powered insights'
        ],
        'benefits': [
            'improved patient care', 'operational efficiency', 'cost reduction',
            'better outcomes', 'regulatory compliance', 'enhanced accessibility',
            'data-driven decisions', 'patient satisfaction'
        ]
    },
    
    'EdTech': {
        'terms': [
            'education technology', 'e-learning', 'online education', 'digital learning',
            'learning management system', 'educational software', 'online courses',
            'virtual classroom', 'educational platform', 'skill development'
        ],
        'regions': [
            'India', 'globally', 'developing countries', 'remote areas',
            'urban centers', 'K-12 schools', 'higher education', 'corporate training'
        ],
        'business_types': [
            'educational institution', 'corporate training', 'individual learner',
            'teacher', 'school district', 'university', 'training company',
            'online course provider'
        ],
        'pain_points': [
            'student engagement', 'learning outcomes', 'accessibility issues',
            'cost of education', 'personalization needs', 'technology adoption',
            'content quality', 'assessment challenges'
        ],
        'actions': [
            'improve learning outcomes', 'increase engagement', 'reduce costs',
            'enhance accessibility', 'personalize learning', 'track progress',
            'automate assessment', 'facilitate collaboration'
        ],
        'needs': [
            'personalized learning', 'student engagement', 'progress tracking',
            'content creation', 'assessment tools', 'collaboration features',
            'mobile learning', 'accessibility support'
        ],
        'use_cases': [
            'online courses', 'virtual classrooms', 'skill assessments',
            'corporate training', 'K-12 education', 'professional development',
            'language learning', 'certification programs'
        ],
        'features': [
            'course content', 'video lectures', 'interactive exercises',
            'progress tracking', 'discussion forums', 'assessment tools',
            'mobile app', 'certification'
        ],
        'capabilities': [
            'adaptive learning', 'content authoring', 'student analytics',
            'collaboration tools', 'assessment automation', 'mobile learning',
            'gamification', 'personalization'
        ],
        'benefits': [
            'improved learning outcomes', 'increased accessibility', 'cost effectiveness',
            'personalized education', 'flexible learning', 'skill development',
            'career advancement', 'measurable results'
        ]
    }
}
