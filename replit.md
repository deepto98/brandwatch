# Brand Visibility AI Monitor

## Overview

The Brand Visibility AI Monitor is a Streamlit-based Python application that analyzes brand mentions and visibility across major AI platforms. The system generates industry-specific prompts, queries multiple AI platforms (OpenAI, Google Gemini, Perplexity), and provides comprehensive analysis of brand performance compared to competitors.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Interface**: Single-page application with sidebar navigation
- **Visualization**: Plotly for interactive charts and graphs
- **State Management**: Streamlit session state for maintaining analysis results

### Backend Architecture
- **Language**: Python 3.x
- **Architecture Pattern**: Service-oriented architecture with modular components
- **Data Processing**: Pandas for data manipulation and analysis
- **NLP Processing**: spaCy for natural language processing tasks

### Key Design Decisions
- **Modular Service Architecture**: Separated concerns into distinct services (AI platforms, brand analysis, competitor analysis, etc.)
- **Async Processing**: Supports asynchronous operations for querying multiple AI platforms
- **Configuration-Driven**: Industry-specific configurations stored in separate modules
- **Error Handling**: Graceful fallbacks for API failures and missing dependencies

## Key Components

### Core Services
1. **AIPlatformManager** (`services/ai_platforms.py`)
   - Integrates with OpenAI GPT-4, Google Gemini, and Perplexity AI
   - Handles API authentication and request management
   - Provides unified interface for querying different platforms

2. **PromptGenerator** (`services/prompt_generator.py`)
   - Generates industry-specific prompts based on business context
   - Uses template-based approach with dynamic content insertion
   - Covers different customer journey stages and query types

3. **BrandAnalyzer** (`services/brand_analyzer.py`)
   - Analyzes brand mentions in AI platform responses
   - Calculates mention frequency, ranking positions, and sentiment
   - Provides detailed context analysis for each mention

4. **CompetitorAnalyzer** (`services/competitor_analyzer.py`)
   - Compares brand performance against competitors
   - Generates competitive insights and market positioning analysis
   - Identifies opportunities and threats in the competitive landscape

5. **VisibilityScorer** (`services/visibility_scorer.py`)
   - Calculates comprehensive visibility scores using weighted metrics
   - Generates actionable insights and recommendations
   - Provides component-level scoring for detailed analysis

### Utility Components
1. **NLPProcessor** (`utils/nlp_processor.py`)
   - Handles text processing and sentiment analysis
   - Provides brand mention detection and context extraction
   - Falls back gracefully if spaCy model is unavailable

2. **DataProcessor** (`utils/data_processor.py`)
   - Processes platform responses into structured data
   - Calculates statistical metrics and performance indicators
   - Handles data transformation and aggregation

### Configuration
- **Industry Definitions** (`config/industries.py`)
  - Comprehensive industry-specific terminology and contexts
  - Supports FinTech and other industry verticals
  - Includes terms, regions, business types, and use cases

## Data Flow

1. **Brand Profile Setup**: User inputs brand name, industry, and competitors
2. **Prompt Generation**: System generates 20-30 industry-specific prompts
3. **AI Platform Querying**: Parallel queries to OpenAI, Gemini, and Perplexity
4. **Response Analysis**: Brand and competitor mentions are extracted and analyzed
5. **Scoring and Insights**: Comprehensive visibility scores calculated with recommendations
6. **Visualization**: Results presented through interactive charts and tables

## External Dependencies

### AI Platform APIs
- **OpenAI API**: GPT-4 integration for conversational AI analysis
- **Google Gemini API**: Google's AI assistant platform
- **Perplexity API**: AI-powered search and answer engine

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization
- **spacy**: Natural language processing (optional)
- **openai**: OpenAI API client
- **google.genai**: Google Gemini API client

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API authentication
- `GEMINI_API_KEY`: Google Gemini API authentication
- `PERPLEXITY_API_KEY`: Perplexity API authentication

## Deployment Strategy

### Current Setup
- **Platform**: Designed for Replit deployment
- **Runtime**: Python 3.x environment
- **Dependencies**: Managed through standard Python package management
- **Configuration**: Environment variables for API keys

### Scalability Considerations
- **API Rate Limiting**: Built-in error handling for API limitations
- **Async Processing**: Supports concurrent API calls for better performance
- **Modular Architecture**: Easy to extend with additional AI platforms
- **Caching**: Session state management for analysis results

## Changelog

- July 05, 2025. Initial setup
- July 05, 2025. Major UI overhaul to professional SaaS design:
  - Added custom CSS styling with modern color scheme (#6366F1 primary)
  - Implemented professional header with gradient background
  - Created metric cards with hover effects and shadows
  - Added platform-specific color badges (OpenAI green, Gemini blue, Perplexity purple)
  - Improved sidebar organization with clear sections
  - Enhanced chart styling with modern colors and layouts
  - Fixed percentage calculation bug - multiple mentions in one response now count as one
  - Improved industry selection with single text field for both predefined and custom industries
  - Re-enabled ranking functionality with integer display instead of decimals
  - Added two new search-enhanced AI platforms:
    - Microsoft Copilot: Bing-integrated AI assistant
    - Meta AI: Facebook's conversational AI platform
  - Updated UI to categorize platforms as "Core Platforms" and "Search-Enhanced AI"
  - Added platform-specific color styling (Copilot: #0078D4, Meta: #0866FF)
  - Implemented concurrent API calls using ThreadPoolExecutor for massive speed improvements:
    - All platforms and prompts are queried in parallel
    - Dynamic worker sizing (up to 20 concurrent requests)
    - Competitor analysis runs concurrently
    - Real-time progress tracking with thread-safe updates

## User Preferences

Preferred communication style: Simple, everyday language.