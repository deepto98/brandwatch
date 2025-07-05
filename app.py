import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import asyncio
import json
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from services.ai_platforms import AIPlatformManager
from services.prompt_generator import PromptGenerator
from services.brand_analyzer import BrandAnalyzer
from services.competitor_analyzer import CompetitorAnalyzer
from services.visibility_scorer import VisibilityScorer
from config.industries import INDUSTRIES

# Page configuration
st.set_page_config(
    page_title="BrandwatchAI - Brand Visibility Monitor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'brand_profile' not in st.session_state:
    st.session_state.brand_profile = None

def apply_custom_css():
    """Apply custom CSS for professional SaaS-like appearance"""
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0;
    }
    
    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 1rem 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .app-header h1 {
        color: white;
        font-weight: 700;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 0.5rem;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(99, 102, 241, 0.3);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #F9FAFB;
    }
    
    .sidebar .sidebar-content {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        background: transparent;
        border: none;
        color: #6B7280;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #6366F1;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #6366F1;
        border-bottom: 3px solid #6366F1;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #E5E7EB;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 0.75rem;
        border: none;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* DataFrame styling */
    .dataframe {
        border: none !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Section headers */
    .section-header {
        background: #F3F4F6;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #6366F1;
    }
    
    .section-header h3 {
        margin: 0;
        color: #1F2937;
        font-weight: 600;
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .platform-openai {
        background: #10B981;
        color: white;
    }
    
    .platform-gemini {
        background: #3B82F6;
        color: white;
    }
    
    .platform-perplexity {
        background: #8B5CF6;
        color: white;
    }
    
    /* Copilot and Meta styles removed - platforms disabled */
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_custom_css()
    
    # Professional header with logo
    st.markdown("""
    <div class="app-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem;">
            <div style="width: 60px; height: 60px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: #6366F1;">
                👁️
            </div>
            <div>
                <h1 style="margin: 0;">BrandwatchAI</h1>
                <p style="margin: 0;">Track and analyze your brand's presence across major AI platforms</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for brand profile setup
    with st.sidebar:
        # Sidebar logo and branding
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 50px; height: 50px; background: #6366F1; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; margin: 0 auto;">
                👁️
            </div>
            <h3 style="margin-top: 0.5rem; color: #1F2937;">BrandwatchAI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🏢 Brand Profile")
        st.markdown("---")
        
        # Brand Information Section
        with st.container():
            st.markdown("#### Company Details")
            brand_name = st.text_input("Brand Name", placeholder="e.g., PolicyBazaar", label_visibility="visible")
            
            # Industry selection - single field for both predefined and custom
            predefined_industries = list(INDUSTRIES.keys())
            
            industry = st.text_input(
                "Industry",
                placeholder="Enter your industry (e.g., FinTech, Legal Tech, Food Delivery)",
                help="Enter any industry name - predefined industries have optimized prompts"
            )
            
            # Check if it's a predefined or custom industry
            custom_industry = None
            if industry:
                if industry in predefined_industries:
                    st.success(f"✓ Using predefined industry: {industry}")
                else:
                    custom_industry = industry
                    st.info(f"✓ Using custom industry: {custom_industry}")
            
            # Location field (optional)
            location = st.text_input("Location (Optional)", 
                                   placeholder="e.g., India, New York, Europe",
                                   help="Enter a country, city, or region for location-specific prompts")
        
        st.markdown("---")
        
        # Competitor Information
        with st.container():
            st.markdown("#### Competitors")
            competitor_count = st.number_input("Number of Competitors", min_value=1, max_value=10, value=3)
            
            competitors = []
            for i in range(competitor_count):
                competitor = st.text_input(f"Competitor {i+1}", key=f"competitor_{i}")
                if competitor:
                    competitors.append(competitor)
        
        st.markdown("---")
        
        # Analysis Settings
        with st.container():
            st.markdown("#### Analysis Configuration")
            prompt_count = st.slider("Number of Prompts", min_value=10, max_value=50, value=20, 
                                   help="More prompts provide deeper insights")
            
            st.markdown("##### AI Platforms")
            st.markdown("###### Available Platforms")
            col1, col2, col3 = st.columns(3)
            with col1:
                use_openai = st.checkbox("ChatGPT", value=True)
            with col2:
                use_gemini = st.checkbox("Gemini", value=True)
            with col3:
                use_perplexity = st.checkbox("Perplexity", value=True)
        
        platforms = []
        if use_openai:
            platforms.append("openai")
        if use_gemini:
            platforms.append("gemini")
        if use_perplexity:
            platforms.append("perplexity")
        
        st.markdown("---")
        
        # Start Analysis Button
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if not brand_name:
                st.error("Please enter a brand name")
            elif not industry:
                st.error("Please enter an industry")
            elif not competitors:
                st.error("Please add at least one competitor")
            elif not platforms:
                st.error("Please select at least one AI platform")
            else:
                # Store brand profile
                st.session_state.brand_profile = {
                    'brand_name': brand_name,
                    'industry': industry,
                    'is_custom_industry': industry not in predefined_industries,
                    'location': location if location else None,
                    'competitors': competitors,
                    'prompt_count': prompt_count,
                    'platforms': platforms
                }
                run_analysis()

    # Main content area
    if st.session_state.brand_profile is None:
        # Welcome screen with professional cards
        st.markdown('<div class="section-header"><h3>Getting Started</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 How It Works</h3>
                <p>Our AI-powered system analyzes brand visibility across major AI platforms by:</p>
                <ul style="margin-left: 1rem;">
                    <li>Generating industry-specific search queries</li>
                    <li>Analyzing responses from multiple AI platforms</li>
                    <li>Tracking brand mentions and sentiment</li>
                    <li>Comparing performance against competitors</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 What You'll Get</h3>
                <p>Comprehensive insights including:</p>
                <ul style="margin-left: 1rem;">
                    <li>Visibility score across platforms</li>
                    <li>Competitive positioning analysis</li>
                    <li>Platform-specific performance metrics</li>
                    <li>Actionable recommendations</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-header"><h3>Supported AI Platforms</h3></div>', unsafe_allow_html=True)
        
        # Core Platform cards
        st.markdown("#### Core Platforms")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <span class="platform-badge platform-openai">OpenAI</span>
                <h4>ChatGPT</h4>
                <p style="color: #6B7280;">Leading conversational AI platform</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <span class="platform-badge platform-gemini">Google</span>
                <h4>Gemini</h4>
                <p style="color: #6B7280;">Google's advanced AI assistant</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="metric-card" style="text-align: center;">
                <span class="platform-badge platform-perplexity">Perplexity</span>
                <h4>Perplexity AI</h4>
                <p style="color: #6B7280;">AI-powered answer engine</p>
            </div>
            """, unsafe_allow_html=True)
        

        
        # CTA Section
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3>Ready to monitor your brand with BrandwatchAI?</h3>
            <p style="color: #6B7280;">Fill in your brand details in the sidebar and click "Start Analysis"</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif not st.session_state.analysis_complete:
        # Analysis in progress
        display_analysis_progress()
    
    else:
        # Display results
        display_analysis_results()

def run_analysis():
    """Run the complete brand visibility analysis"""
    st.session_state.analysis_complete = False
    
    with st.spinner("Analyzing brand visibility..."):
        try:
            profile = st.session_state.brand_profile
            
            # Initialize services
            prompt_generator = PromptGenerator()
            ai_manager = AIPlatformManager()
            brand_analyzer = BrandAnalyzer()
            competitor_analyzer = CompetitorAnalyzer()
            visibility_scorer = VisibilityScorer()
            
            # Generate prompts
            st.info("🔄 Generating industry-specific prompts...")
            prompts = prompt_generator.generate_prompts(
                profile['industry'], 
                profile['prompt_count'],
                location=profile.get('location'),
                is_custom=profile.get('is_custom_industry', False)
            )
            
            # Query AI platforms with concurrency
            st.info("🔄 Querying AI platforms concurrently...")
            all_responses = {}
            total_queries = len(profile['platforms']) * len(prompts)
            completed_queries = 0
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            # Thread-safe counter
            lock = threading.Lock()
            
            def query_single_prompt(platform, prompt):
                """Query a single prompt on a platform"""
                response = ai_manager.query_platform(platform, prompt)
                return platform, prompt, response
            
            def update_progress():
                """Update progress bar in thread-safe manner"""
                nonlocal completed_queries
                with lock:
                    completed_queries += 1
                    progress = completed_queries / total_queries
                    progress_bar.progress(progress)
                    progress_text.text(f"Processing: {completed_queries}/{total_queries} queries completed")
            
            # Use ThreadPoolExecutor for concurrent API calls
            # Optimize worker count based on platforms and prompts
            max_workers = min(
                len(profile['platforms']) * 5,  # 5 concurrent requests per platform
                total_queries,  # Don't exceed total queries
                20  # Cap at 20 to avoid overwhelming APIs
            )
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                futures = []
                for platform in profile['platforms']:
                    all_responses[platform] = []
                    for prompt in prompts:
                        future = executor.submit(query_single_prompt, platform, prompt)
                        futures.append(future)
                
                # Process completed tasks
                for future in as_completed(futures):
                    try:
                        platform, prompt, response = future.result()
                        all_responses[platform].append({
                            'prompt': prompt,
                            'response': response
                        })
                        update_progress()
                    except Exception as e:
                        st.warning(f"Error in concurrent query: {str(e)}")
                        update_progress()
            
            # Sort responses to maintain order
            for platform in all_responses:
                all_responses[platform].sort(key=lambda x: prompts.index(x['prompt']))
            
            progress_text.empty()
            
            # Analyze brand mentions
            st.info("🔄 Analyzing brand mentions...")
            brand_analysis = brand_analyzer.analyze_mentions(
                all_responses, 
                profile['brand_name']
            )
            
            # Analyze competitors
            st.info("🔄 Analyzing competitor mentions...")
            competitor_analysis = competitor_analyzer.analyze_competitors(
                all_responses, 
                profile['competitors']
            )
            
            # Calculate visibility score
            st.info("🔄 Calculating visibility score...")
            visibility_score = visibility_scorer.calculate_score(
                brand_analysis, 
                competitor_analysis
            )
            
            # Store results
            st.session_state.analysis_data = {
                'prompts': prompts,
                'responses': all_responses,
                'brand_analysis': brand_analysis,
                'competitor_analysis': competitor_analysis,
                'visibility_score': visibility_score,
                'timestamp': datetime.now().isoformat()
            }
            
            st.session_state.analysis_complete = True
            st.success("✅ Analysis complete!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.session_state.analysis_complete = False

def display_analysis_progress():
    """Display analysis progress"""
    st.markdown("## 🔄 Analysis in Progress")
    st.markdown("Please wait while we analyze your brand visibility across AI platforms...")
    
    # Show brand profile summary
    profile = st.session_state.brand_profile
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Brand Profile")
        st.write(f"**Brand:** {profile['brand_name']}")
        st.write(f"**Industry:** {profile['industry']}")
        if profile.get('location'):
            st.write(f"**Location:** {profile['location']}")
        st.write(f"**Prompts:** {profile['prompt_count']}")
    
    with col2:
        st.markdown("### Analysis Scope")
        st.write(f"**Competitors:** {', '.join(profile['competitors'])}")
        st.write(f"**Platforms:** {', '.join(profile['platforms'])}")

def display_analysis_results():
    """Display the analysis results"""
    data = st.session_state.analysis_data
    profile = st.session_state.brand_profile
    
    # Professional results header
    st.markdown(f"""
    <div class="section-header">
        <h3>Analysis Results for {profile['brand_name']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = data['visibility_score']['overall_score']
        score_color = "#10B981" if score >= 70 else "#F59E0B" if score >= 40 else "#EF4444"
        st.markdown(f"""
        <div class="metric-card">
            <h5 style="color: #6B7280; margin: 0;">Visibility Score</h5>
            <h2 style="color: {score_color}; margin: 0.5rem 0;">{score}/100</h2>
            <p style="color: #9CA3AF; font-size: 0.875rem;">Overall brand presence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_mentions = sum(data['brand_analysis']['platform_mentions'].values())
        st.markdown(f"""
        <div class="metric-card">
            <h5 style="color: #6B7280; margin: 0;">Total Mentions</h5>
            <h2 style="color: #1F2937; margin: 0.5rem 0;">{total_mentions}</h2>
            <p style="color: #9CA3AF; font-size: 0.875rem;">Across all platforms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_ranking = data['brand_analysis']['average_ranking']
        ranking_display = "No Ranking Data" if not avg_ranking else f"#{avg_ranking}"
        st.markdown(f"""
        <div class="metric-card">
            <h5 style="color: #6B7280; margin: 0;">Average Ranking</h5>
            <h2 style="color: #1F2937; margin: 0.5rem 0;">{ranking_display}</h2>
            <p style="color: #9CA3AF; font-size: 0.875rem;">Position in results</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        platforms_count = len(profile['platforms'])
        st.markdown(f"""
        <div class="metric-card">
            <h5 style="color: #6B7280; margin: 0;">Platforms Analyzed</h5>
            <h2 style="color: #1F2937; margin: 0.5rem 0;">{platforms_count}</h2>
            <p style="color: #9CA3AF; font-size: 0.875rem;">AI systems queried</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview Dashboard", 
        "🎯 Platform Analysis", 
        "🏆 Competitor Comparison", 
        "📋 Detailed Results",
        "💡 Insights & Recommendations"
    ])
    
    with tab1:
        display_overview_dashboard(data, profile)
    
    with tab2:
        display_platform_analysis(data, profile)
    
    with tab3:
        display_competitor_comparison(data, profile)
    
    with tab4:
        display_detailed_results(data, profile)
    
    with tab5:
        display_insights_recommendations(data, profile)

def display_overview_dashboard(data, profile):
    """Display the overview dashboard"""
    # Platform performance section
    st.markdown('<div class="section-header"><h3>Platform Performance</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform mentions pie chart with better styling
        platform_mentions = data['brand_analysis']['platform_mentions']
        if any(platform_mentions.values()):
            # Create custom color scheme for platforms
            colors = {
                'openai': '#10B981',
                'gemini': '#3B82F6',
                'perplexity': '#8B5CF6'
            }
            
            fig = px.pie(
                values=list(platform_mentions.values()),
                names=[p.upper() for p in platform_mentions.keys()],
                title="Brand Mentions Distribution",
                color_discrete_map={k.upper(): v for k, v in colors.items()}
            )
            fig.update_layout(
                font=dict(family="sans serif", size=14),
                title_font_size=18,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="metric-card" style="text-align: center; padding: 3rem;">
                <p style="color: #6B7280;">No brand mentions found across platforms</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Visibility score gauge with modern styling
        score = data['visibility_score']['overall_score']
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Visibility Score", 'font': {'size': 18}},
            delta = {'reference': 50, 'relative': False},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#6366F1"},
                'steps': [
                    {'range': [0, 25], 'color': "#FEE2E2"},
                    {'range': [25, 50], 'color': "#FEF3C7"},
                    {'range': [50, 75], 'color': "#D1FAE5"},
                    {'range': [75, 100], 'color': "#A7F3D0"}
                ],
                'threshold': {
                    'line': {'color': "#1F2937", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(
            font=dict(family="sans serif", size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Brand vs Competitors comparison
    st.markdown('<div class="section-header"><h3>Competitive Landscape</h3></div>', unsafe_allow_html=True)
    
    competitor_data = data['competitor_analysis']
    brand_name = profile['brand_name']
    
    # Create comparison data
    comparison_data = {
        'Entity': [brand_name] + profile['competitors'],
        'Total Mentions': [sum(data['brand_analysis']['platform_mentions'].values())] + 
                         [competitor_data.get(comp, {}).get('total_mentions', 0) for comp in profile['competitors']],
        'Average Ranking': [data['brand_analysis']['average_ranking'] or 0] + 
                          [competitor_data.get(comp, {}).get('average_ranking', 0) for comp in profile['competitors']]
    }
    
    df = pd.DataFrame(comparison_data)
    
    # Create modern bar charts
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('<b>Total Mentions</b>', '<b>Market Position</b>'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Color mapping
    colors = ['#6366F1' if x == brand_name else '#E5E7EB' for x in df['Entity']]
    
    fig.add_trace(
        go.Bar(
            x=df['Entity'], 
            y=df['Total Mentions'], 
            name='Mentions',
            marker_color=colors,
            text=df['Total Mentions'],
            textposition='auto',
        ),
        row=1, col=1
    )
    
    # For ranking, lower is better but we display it inverted for visual clarity
    max_rank = max(df['Average Ranking']) if any(df['Average Ranking']) else 1
    inverted_rankings = [max_rank - r + 1 if r > 0 else 0 for r in df['Average Ranking']]
    
    fig.add_trace(
        go.Bar(
            x=df['Entity'], 
            y=inverted_rankings,
            name='Position',
            marker_color=colors,
            text=[f"#{int(r)}" if r > 0 else "N/A" for r in df['Average Ranking']],
            textposition='auto',
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="sans serif", size=12),
        title_font_size=16,
        hovermode='x unified'
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#F3F4F6')
    
    st.plotly_chart(fig, use_container_width=True)

def display_platform_analysis(data, profile):
    """Display platform-specific analysis"""
    st.markdown('<div class="section-header"><h3>Platform-Specific Performance</h3></div>', unsafe_allow_html=True)
    
    # Platform performance cards
    platform_colors = {
        'openai': {'bg': '#10B981', 'name': 'ChatGPT'},
        'gemini': {'bg': '#3B82F6', 'name': 'Google Gemini'},
        'perplexity': {'bg': '#8B5CF6', 'name': 'Perplexity AI'},
        'copilot': {'bg': '#0078D4', 'name': 'Microsoft Copilot'},
        'meta': {'bg': '#0866FF', 'name': 'Meta AI'}
    }
    
    for platform in profile['platforms']:
        platform_data = data['brand_analysis']['platform_details'].get(platform, {})
        platform_info = platform_colors.get(platform, {'bg': '#6366F1', 'name': platform.upper()})
        
        # Platform header with badge
        st.markdown(f"""
        <div style="margin: 1.5rem 0;">
            <span class="platform-badge" style="background: {platform_info['bg']}; font-size: 1rem; padding: 0.5rem 1rem;">
                {platform_info['name']}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mentions = platform_data.get('mentions', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h5 style="color: #6B7280; margin: 0;">Mentions</h5>
                <h3 style="color: #1F2937; margin: 0.5rem 0;">{mentions}</h3>
                <p style="color: #9CA3AF; font-size: 0.875rem;">Brand occurrences</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_rank = platform_data.get('average_ranking')
            rank_display = "No Data" if not avg_rank else f"#{int(avg_rank)}"
            st.markdown(f"""
            <div class="metric-card">
                <h5 style="color: #6B7280; margin: 0;">Avg. Ranking</h5>
                <h3 style="color: #1F2937; margin: 0.5rem 0;">{rank_display}</h3>
                <p style="color: #9CA3AF; font-size: 0.875rem;">Position in results</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            mention_rate = platform_data.get('mention_rate', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h5 style="color: #6B7280; margin: 0;">Mention Rate</h5>
                <h3 style="color: #1F2937; margin: 0.5rem 0;">{mention_rate:.1%}</h3>
                <p style="color: #9CA3AF; font-size: 0.875rem;">Response coverage</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample mentions section
        if 'sample_mentions' in platform_data and platform_data['sample_mentions']:
            st.markdown("#### Sample Brand Mentions")
            
            for i, sample in enumerate(platform_data['sample_mentions'][:3]):
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom: 1rem;">
                    <p style="color: #6366F1; font-weight: 500; margin-bottom: 0.5rem;">
                        Query: {sample['prompt']}
                    </p>
                    <p style="color: #4B5563; line-height: 1.6;">
                        {sample['response'][:250]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")

def display_competitor_comparison(data, profile):
    """Display competitor comparison"""
    st.markdown("### Competitor Performance Analysis")
    
    competitor_data = data['competitor_analysis']
    brand_name = profile['brand_name']
    
    # Create detailed comparison table
    comparison_rows = []
    
    # Add brand data
    brand_analysis = data['brand_analysis']
    comparison_rows.append({
        'Entity': f"🎯 {brand_name}",
        'Total Mentions': sum(brand_analysis['platform_mentions'].values()),
        'Average Ranking': brand_analysis['average_ranking'] or 0,
        'OpenAI Mentions': brand_analysis['platform_mentions'].get('openai', 0),
        'Gemini Mentions': brand_analysis['platform_mentions'].get('gemini', 0),
        'Perplexity Mentions': brand_analysis['platform_mentions'].get('perplexity', 0)
    })
    
    # Add competitor data
    for competitor in profile['competitors']:
        comp_data = competitor_data.get(competitor, {})
        comparison_rows.append({
            'Entity': f"🏢 {competitor}",
            'Total Mentions': comp_data.get('total_mentions', 0),
            'Average Ranking': comp_data.get('average_ranking', 0),
            'OpenAI Mentions': comp_data.get('platform_mentions', {}).get('openai', 0),
            'Gemini Mentions': comp_data.get('platform_mentions', {}).get('gemini', 0),
            'Perplexity Mentions': comp_data.get('platform_mentions', {}).get('perplexity', 0)
        })
    
    df_comparison = pd.DataFrame(comparison_rows)
    
    # Style the dataframe
    st.dataframe(
        df_comparison,
        use_container_width=True,
        hide_index=True
    )
    
    # Competitive positioning chart
    st.markdown("### Competitive Positioning")
    
    if len(comparison_rows) > 1:
        fig = px.scatter(
            df_comparison,
            x='Total Mentions',
            y='Average Ranking',
            size='Total Mentions',
            color='Entity',
            title="Competitive Positioning (Higher mentions + Lower ranking = Better)",
            labels={'Average Ranking': 'Average Ranking (Lower is Better)'}
        )
        st.plotly_chart(fig, use_container_width=True)

def display_detailed_results(data, profile):
    """Display detailed results"""
    st.markdown("### Detailed Analysis Results")
    
    # Generated prompts
    with st.expander("📝 Generated Prompts"):
        for i, prompt in enumerate(data['prompts'], 1):
            st.write(f"{i}. {prompt}")
    
    # Platform responses
    with st.expander("🤖 AI Platform Responses"):
        for platform, responses in data['responses'].items():
            st.markdown(f"#### {platform.upper()} Responses")
            
            for i, response_data in enumerate(responses[:5], 1):  # Show first 5
                with st.expander(f"Response {i}: {response_data['prompt'][:50]}..."):
                    st.markdown(f"**Prompt:** {response_data['prompt']}")
                    st.markdown(f"**Response:** {response_data['response']}")
    
    # Export functionality
    st.markdown("### 📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Analysis Report"):
            export_data = {
                'brand_profile': profile,
                'analysis_results': data,
                'export_timestamp': datetime.now().isoformat()
            }
            
            st.download_button(
                label="Download JSON Report",
                data=json.dumps(export_data, indent=2),
                file_name=f"{profile['brand_name']}_visibility_analysis.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Export Summary CSV"):
            # Create summary DataFrame
            summary_data = {
                'Metric': ['Overall Visibility Score', 'Total Brand Mentions', 'Average Ranking', 'Top Platform'],
                'Value': [
                    data['visibility_score']['overall_score'],
                    sum(data['brand_analysis']['platform_mentions'].values()),
                    data['brand_analysis']['average_ranking'] or 0,
                    max(data['brand_analysis']['platform_mentions'], key=data['brand_analysis']['platform_mentions'].get)
                ]
            }
            
            df_summary = pd.DataFrame(summary_data)
            csv = df_summary.to_csv(index=False)
            
            st.download_button(
                label="Download CSV Summary",
                data=csv,
                file_name=f"{profile['brand_name']}_summary.csv",
                mime="text/csv"
            )

def display_insights_recommendations(data, profile):
    """Display insights and recommendations"""
    st.markdown("### 💡 Key Insights & Recommendations")
    
    insights = data['visibility_score']['insights']
    recommendations = data['visibility_score']['recommendations']
    
    # Key insights
    st.markdown("#### 🔍 Key Insights")
    for insight in insights:
        st.info(f"💡 {insight}")
    
    # Recommendations
    st.markdown("#### 📋 Actionable Recommendations")
    for i, recommendation in enumerate(recommendations, 1):
        st.success(f"✅ {i}. {recommendation}")
    
    # Performance trends
    st.markdown("#### 📈 Performance Analysis")
    
    score = data['visibility_score']['overall_score']
    
    if score >= 75:
        st.success("🎉 Excellent brand visibility! Your brand is well-represented across AI platforms.")
    elif score >= 50:
        st.warning("⚠️ Good visibility with room for improvement. Focus on underperforming platforms.")
    else:
        st.error("🚨 Low brand visibility. Immediate action needed to improve AI platform presence.")
    
    # Strategic recommendations based on score
    st.markdown("#### 🎯 Strategic Focus Areas")
    
    brand_mentions = data['brand_analysis']['platform_mentions']
    lowest_platform = min(brand_mentions, key=brand_mentions.get)
    highest_platform = max(brand_mentions, key=brand_mentions.get)
    
    st.markdown(f"""
    **Priority Actions:**
    1. **Focus on {lowest_platform.upper()}**: This platform shows the lowest brand mentions ({brand_mentions[lowest_platform]})
    2. **Leverage {highest_platform.upper()}**: This platform shows the highest brand mentions ({brand_mentions[highest_platform]})
    3. **Competitor Analysis**: Monitor competitor strategies on platforms where they outperform you
    4. **Content Strategy**: Develop content that naturally includes your brand for AI training
    """)

if __name__ == "__main__":
    main()
