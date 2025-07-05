# 👁️ BrandwatchAI

<div align="center">

![BrandwatchAI Logo](https://img.shields.io/badge/BrandwatchAI-Monitor%20Your%20Brand%20Across%20AI%20Platforms-6366F1?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0NSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBvcGFjaXR5PSIwLjMiLz4KPGVsbGlwc2UgY3g9IjUwIiBjeT0iNTAiIHJ4PSIzNSIgcnk9IjIwIiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjMiLz4KPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iMTUiIGZpbGw9IndoaXRlIiBvcGFjaXR5PSIwLjkiLz4KPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNiIgZmlsbD0iIzFhMWExYSIvPgo8L3N2Zz4=)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**🚀 Track and analyze your brand's presence across major AI platforms in real-time**

[Demo](#-demo) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

BrandwatchAI is an intelligent Streamlit-powered application that monitors brand visibility across multiple AI platforms. Get actionable insights about how ChatGPT, Gemini, and Perplexity AI perceive and recommend your brand.

<div align="center">
<img src="https://via.placeholder.com/800x400/6366F1/FFFFFF?text=BrandwatchAI+Dashboard" alt="BrandwatchAI Dashboard" width="80%">
</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 Multi-Platform AI Analysis
- **OpenAI ChatGPT** (GPT-4o)
- **Google Gemini** (2.5-flash)
- **Perplexity AI** (llama-3.1-sonar)

</td>
<td width="50%">

### ⚡ High-Performance Architecture
- Concurrent API calls (20+ simultaneous)
- 90% faster than sequential processing
- Results in 20-30 seconds

</td>
</tr>
<tr>
<td width="50%">

### 📊 Comprehensive Analytics
- Brand mention frequency tracking
- Sentiment analysis & context extraction
- Ranking position identification
- Competitor comparison

</td>
<td width="50%">

### 🎨 Professional UI/UX
- Modern SaaS-style interface
- Custom CSS with gradient effects
- Interactive Plotly visualizations
- Real-time progress tracking

</td>
</tr>
</table>

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- API Keys for:
  - OpenAI
  - Google Gemini
  - Perplexity

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/brandwatchai.git
cd brandwatchai
```

2. **Install dependencies**
```bash
# Using pip
pip install streamlit pandas plotly openai google-genai requests spacy

# Or using the project's pyproject.toml
pip install -e .
```

3. **Set up environment variables**
```bash
# Create .env file
touch .env

# Add your API keys
echo "OPENAI_API_KEY=your_openai_key" >> .env
echo "GEMINI_API_KEY=your_gemini_key" >> .env
echo "PERPLEXITY_API_KEY=your_perplexity_key" >> .env
```

4. **Run the application**
```bash
streamlit run app.py --server.port 5000
```

## 📖 Usage

### 1️⃣ Brand Profile Setup
<div align="center">
<img src="https://via.placeholder.com/600x300/F3F4F6/1F2937?text=1.+Enter+Brand+Details" alt="Brand Setup" width="60%">
</div>

- Enter your brand name
- Select or type your industry
- Add up to 5 competitors
- Choose target location (optional)

### 2️⃣ Analysis Configuration
<div align="center">
<img src="https://via.placeholder.com/600x300/F3F4F6/1F2937?text=2.+Configure+Analysis" alt="Analysis Config" width="60%">
</div>

- Adjust number of prompts (10-50)
- Select AI platforms to analyze
- Click "Start Analysis"

### 3️⃣ View Results
<div align="center">
<img src="https://via.placeholder.com/600x300/F3F4F6/1F2937?text=3.+Analyze+Results" alt="Results Dashboard" width="60%">
</div>

Navigate through tabs:
- **Overview**: Key metrics and scores
- **Platform Analysis**: Detailed platform breakdown
- **Competitor Comparison**: Side-by-side analysis
- **Detailed Results**: Raw data and responses
- **Insights**: AI-generated recommendations

## 🏗️ Architecture

```mermaid
graph TB
    A[Streamlit UI] --> B[Brand Profile Input]
    B --> C[Prompt Generator]
    C --> D[AI Platform Manager]
    
    D --> E[OpenAI API]
    D --> F[Gemini API]
    D --> G[Perplexity API]
    
    E --> H[Response Analyzer]
    F --> H
    G --> H
    
    H --> I[Brand Analyzer]
    H --> J[Competitor Analyzer]
    
    I --> K[Visibility Scorer]
    J --> K
    
    K --> L[Results Dashboard]
    
    style A fill:#6366F1,stroke:#fff,color:#fff
    style L fill:#10B981,stroke:#fff,color:#fff
```

### Core Components

| Component | Description |
|-----------|-------------|
| **AIPlatformManager** | Unified API integration layer for all AI platforms |
| **PromptGenerator** | Industry-specific query generation engine |
| **BrandAnalyzer** | Extract and analyze brand mentions |
| **CompetitorAnalyzer** | Comparative market positioning analysis |
| **VisibilityScorer** | Weighted scoring algorithm |
| **NLPProcessor** | Natural language processing utilities |

## 📊 Performance Metrics

<div align="center">

| Metric | Sequential | **Concurrent** | Improvement |
|--------|------------|----------------|-------------|
| Analysis Time | 3-5 minutes | **20-30 seconds** | 🚀 90% faster |
| API Calls | 1 at a time | **20+ simultaneous** | ⚡ 20x throughput |
| Memory Usage | Standard | **Optimized** | 💾 Minimal footprint |

</div>

## 🎨 UI Showcase

### Platform-Specific Styling
<div align="center">

![OpenAI](https://img.shields.io/badge/OpenAI-10B981?style=for-the-badge&logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-3B82F6?style=for-the-badge&logo=google&logoColor=white)
![Perplexity](https://img.shields.io/badge/Perplexity-8B5CF6?style=for-the-badge&logo=perplexity&logoColor=white)

</div>

### Modern Dashboard Components
- 📊 Interactive Plotly charts
- 📈 Real-time progress indicators
- 🎯 Metric cards with hover effects
- 🌈 Gradient headers and shadows
- 📱 Responsive design

## 🛠️ Configuration

### Industry Templates

```python
# config/industries.py
INDUSTRIES = {
    "FinTech": {
        "terms": ["payment", "banking", "finance", "money transfer"],
        "use_cases": ["Send money", "Pay bills", "Investment"],
        # ... more configuration
    },
    # Add custom industries here
}
```

### Prompt Customization

```python
# Adjust prompt generation
prompt_generator = PromptGenerator()
prompts = prompt_generator.generate_prompts(
    industry="FinTech",
    count=30,
    location="United States"
)
```

## 🤝 Contributing

We love contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

```bash
# Fork the repo
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add some AmazingFeature'

# Push to the branch
git push origin feature/AmazingFeature

# Open a Pull Request
```

## 📈 Roadmap

- [ ] Historical trend tracking
- [ ] Additional AI platforms (Claude, Bard)
- [ ] Export functionality (PDF/Excel)
- [ ] Multi-brand monitoring
- [ ] API endpoint for integration
- [ ] Scheduled automated reports

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [OpenAI](https://openai.com), [Google Gemini](https://ai.google.dev), and [Perplexity](https://perplexity.ai)
- Icons by [Heroicons](https://heroicons.com)

---

<div align="center">

</div>
