"""
GitHub Issue Assistant - Streamlit Frontend
Production-grade UI for analyzing GitHub issues with AI
"""

import streamlit as st
import requests
import json
from typing import Optional
import time


# Page configuration
st.set_page_config(
    page_title="GitHub Issue Assistant | AI-Powered Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/github-issue-assistant',
        'Report a bug': 'https://github.com/yourusername/github-issue-assistant/issues',
        'About': "AI-Powered GitHub Issue Assistant - Built with FastAPI, LangChain, and Streamlit"
    }
)

# Custom CSS for production-grade UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Example button styling */
    div[data-testid="column"] .stButton>button {
        width: 100%;
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
    }
    
    div[data-testid="column"] .stButton>button:hover {
        background: #667eea;
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #e0e7ff 0%, #f0e7ff 100%);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Success message */
    .success-badge {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Label badges */
    .label-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #667eea;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Priority indicator */
    .priority-high {
        color: #ef4444;
        font-weight: 700;
    }
    
    .priority-medium {
        color: #f59e0b;
        font-weight: 700;
    }
    
    .priority-low {
        color: #10b981;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: white !important;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def get_api_url() -> str:
    """Get the API URL (configurable for different environments)"""
    return "http://localhost:8000"


def analyze_issue(repo_url: str, issue_number: int) -> Optional[dict]:
    """
    Call the backend API to analyze a GitHub issue
    
    Args:
        repo_url: GitHub repository URL
        issue_number: Issue number to analyze
        
    Returns:
        Analysis results or None if error occurs
    """
    api_url = get_api_url()
    
    try:
        response = requests.post(
            f"{api_url}/analyze",
            json={
                "repo_url": repo_url,
                "issue_number": issue_number
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json().get("detail", "Unknown error")
            st.error(f"❌ **Error:** {error_detail}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("""
        ### ❌ Cannot Connect to Backend API
        
        **Please make sure the backend server is running:**
        
        ```bash
        cd backend
        python -m uvicorn main:app --reload
        ```
        
        The backend should be running on `http://localhost:8000`
        """)
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ **Request timed out.** The issue might be very large or the API is busy. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ **Unexpected error:** {str(e)}")
        return None


def get_priority_class(priority_score: str) -> str:
    """Determine CSS class based on priority score"""
    score = priority_score.split()[0]
    if score in ['4', '5']:
        return 'priority-high'
    elif score in ['2', '3']:
        return 'priority-medium'
    else:
        return 'priority-low'


def copy_to_clipboard(text: str):
    """Create a copy button for text"""
    st.code(text, language="json")
    if st.button("📋 Copy to Clipboard", key="copy_btn"):
        st.success("✅ Copied to clipboard! (Use Ctrl+C to copy the JSON above)")


def display_analysis(analysis: dict):
    """Display the analysis results in a beautiful format"""
    
    # Success badge
    st.markdown("""
    <div class="success-badge">
        ✅ Analysis Complete
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "� Full Report", "💻 Raw JSON"])
    
    with tab1:
        # Metrics row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            issue_type = analysis["type"].replace("_", " ").title()
            type_emoji = {
                "Bug": "🐛",
                "Feature Request": "✨",
                "Documentation": "📚",
                "Question": "❓",
                "Other": "📌"
            }
            emoji = type_emoji.get(issue_type, "📌")
            st.metric("Type", f"{emoji} {issue_type}")
        
        with col2:
            priority_score = analysis["priority_score"].split()[0]
            priority_class = get_priority_class(analysis["priority_score"])
            st.metric("Priority Score", priority_score, delta="out of 5")
        
        with col3:
            label_count = len(analysis["suggested_labels"])
            st.metric("Suggested Labels", label_count)
        
        st.markdown("---")
        
        # Summary card
        st.markdown("### 📝 Summary")
        st.info(analysis["summary"])
        
        # Priority details
        st.markdown("### ⚡ Priority Analysis")
        priority_class = get_priority_class(analysis["priority_score"])
        st.markdown(f"""
        <div class="card">
            <p class="{priority_class}" style="font-size: 1.2rem; margin: 0;">
                {analysis["priority_score"]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Suggested labels
        st.markdown("### 🏷️ Suggested Labels")
        labels_html = " ".join([
            f'<span class="label-badge">{label}</span>'
            for label in analysis["suggested_labels"]
        ])
        st.markdown(labels_html, unsafe_allow_html=True)
        
        # Potential impact
        st.markdown("### 💥 Potential Impact")
        st.warning(analysis["potential_impact"])
    
    with tab2:
        # Full detailed report
        st.markdown("## � Detailed Analysis Report")
        
        st.markdown(f"""
        <div class="card">
            <h3>Summary</h3>
            <p>{analysis["summary"]}</p>
        </div>
        
        <div class="card">
            <h3>Classification</h3>
            <p><strong>Type:</strong> {analysis["type"].replace("_", " ").title()}</p>
            <p><strong>Priority:</strong> {analysis["priority_score"]}</p>
        </div>
        
        <div class="card">
            <h3>Recommended Labels</h3>
            <p>{", ".join(analysis["suggested_labels"])}</p>
        </div>
        
        <div class="card">
            <h3>Impact Assessment</h3>
            <p>{analysis["potential_impact"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download button
        json_str = json.dumps(analysis, indent=2)
        st.download_button(
            label="📥 Download Report as JSON",
            data=json_str,
            file_name="issue_analysis.json",
            mime="application/json",
            use_container_width=True
        )
    
    with tab3:
        # Raw JSON with copy functionality
        st.markdown("### Raw JSON Output")
        json_str = json.dumps(analysis, indent=2)
        st.code(json_str, language="json")
        
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name="issue_analysis.json",
            mime="application/json",
            use_container_width=True
        )


def main():
    """Main application"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🤖 AI-Powered GitHub Issue Assistant</div>
        <div class="hero-subtitle">Intelligent issue analysis powered by GPT-4 | Instant insights for better project management</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick examples section
    st.markdown("### 🚀 Quick Start - Try These Examples")
    
    col1, col2, col3 = st.columns(3)
    
    example_clicked = None
    
    with col1:
        if st.button("📘 React Issue", use_container_width=True):
            example_clicked = ("https://github.com/facebook/react", 28324)
    
    with col2:
        if st.button("⚡ Next.js Issue", use_container_width=True):
            example_clicked = ("https://github.com/vercel/next.js", 60000)
    
    with col3:
        if st.button("💻 VS Code Issue", use_container_width=True):
            example_clicked = ("https://github.com/microsoft/vscode", 200000)
    
    st.markdown("---")
    
    # Initialize session state for form values
    if 'repo_url' not in st.session_state:
        st.session_state.repo_url = ""
    if 'issue_number' not in st.session_state:
        st.session_state.issue_number = 1
    
    # Update session state if example clicked
    if example_clicked:
        st.session_state.repo_url = example_clicked[0]
        st.session_state.issue_number = example_clicked[1]
    
    # Main input form
    with st.container():
        st.markdown("### 🔗 Enter GitHub Issue Details")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            repo_url = st.text_input(
                "Repository URL",
                value=st.session_state.repo_url,
                placeholder="https://github.com/facebook/react",
                help="Enter the full GitHub repository URL",
                key="repo_input"
            )
        
        with col2:
            issue_number = st.number_input(
                "Issue Number",
                min_value=1,
                value=st.session_state.issue_number,
                step=1,
                help="Enter the issue number",
                key="issue_input"
            )
        
        # Analyze button
        analyze_button = st.button("🚀 Analyze Issue", type="primary", use_container_width=True)
    
    # Process analysis
    if analyze_button:
        if not repo_url:
            st.error("❌ Please enter a repository URL")
        elif not repo_url.startswith("http"):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        elif "github.com" not in repo_url:
            st.error("❌ Please enter a valid GitHub repository URL")
        else:
            # Update session state
            st.session_state.repo_url = repo_url
            st.session_state.issue_number = issue_number
            
            # Show progress
            with st.spinner("🔍 Fetching issue from GitHub..."):
                time.sleep(0.5)
            
            with st.spinner("🤖 Analyzing with AI... This may take 10-20 seconds"):
                analysis = analyze_issue(repo_url, issue_number)
            
            if analysis:
                st.balloons()
                display_analysis(analysis)
    
    # Info section
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <strong>💡 How it works:</strong> Enter a GitHub repository URL and issue number. 
        Our AI analyzes the issue content, comments, and context to provide:
        <ul>
            <li>📝 Concise summary</li>
            <li>🏷️ Automatic classification</li>
            <li>⚡ Priority scoring with justification</li>
            <li>🎯 Relevant label suggestions</li>
            <li>💥 User impact assessment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p style='font-size: 0.9rem; margin-bottom: 0.5rem;'>
            Built with ❤️ using <strong>FastAPI</strong>, <strong>LangChain</strong>, <strong>OpenAI GPT-4</strong>, and <strong>Streamlit</strong>
        </p>
        <p style='font-size: 0.85rem; opacity: 0.8;'>
            <a href='https://github.com/yourusername/github-issue-assistant' target='_blank' style='color: #667eea; text-decoration: none;'>
                View on GitHub →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📖 Guide")
        
        st.markdown("""
        ### How to Use
        
        1. **Quick Start:** Click an example button above
        2. **Or Enter Manually:**
           - Paste a GitHub repo URL
           - Enter the issue number
        3. **Analyze:** Click the analyze button
        4. **Review:** Get instant AI insights
        
        ---
        
        ### 💡 Features
        
        - ✅ Real-time issue analysis
        - ✅ AI-powered classification
        - ✅ Priority scoring
        - ✅ Smart label suggestions
        - ✅ Impact assessment
        - ✅ Export to JSON
        
        ---
        
        ### 📊 Example Repositories
        
        **Popular Projects:**
        - `facebook/react`
        - `vercel/next.js`
        - `microsoft/vscode`
        - `nodejs/node`
        - `python/cpython`
        
        **Note:** Use issue numbers > 1000 for active issues
        
        ---
        
        ### ⚙️ Requirements
        
        - ✅ OpenAI API Key
        - ✅ GitHub Token (Optional)
        - ✅ Backend Server Running
        
        ---
        
        ### 🔒 Privacy
        
        All analysis happens in real-time. We don't store any issue data.
        """)
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Status:** 🟢 Production Ready")


if __name__ == "__main__":
    main()
