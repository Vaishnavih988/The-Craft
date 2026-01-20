"""
GitHub Issue Assistant - Streamlit Frontend
A simple and elegant UI for analyzing GitHub issues with AI
"""

import streamlit as st
import requests
import json
from typing import Optional


# Page configuration
st.set_page_config(
    page_title="GitHub Issue Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1557a0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        padding: 0.8rem;
        border-radius: 5px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin-bottom: 1rem;
    }
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
        with st.spinner("🔍 Fetching issue data from GitHub..."):
            response = requests.post(
                f"{api_url}/analyze",
                json={
                    "repo_url": repo_url,
                    "issue_number": issue_number
                },
                timeout=30
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.json().get("detail", "Unknown error")
            st.error(f"❌ Error: {error_detail}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("""
        ❌ **Cannot connect to backend API**
        
        Please make sure the backend server is running:
        ```bash
        cd backend
        python -m uvicorn main:app --reload
        ```
        """)
        return None
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. The issue might be too large or the API is slow.")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None


def display_analysis(analysis: dict):
    """Display the analysis results in a nice format"""
    
    st.success("✅ Analysis Complete!")
    
    # Summary
    st.markdown("### 📝 Summary")
    st.info(analysis["summary"])
    
    # Create columns for type and priority
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏷️ Type")
        type_emoji = {
            "bug": "🐛",
            "feature_request": "✨",
            "documentation": "📚",
            "question": "❓",
            "other": "📌"
        }
        issue_type = analysis["type"]
        emoji = type_emoji.get(issue_type, "📌")
        st.markdown(f"**{emoji} {issue_type.replace('_', ' ').title()}**")
    
    with col2:
        st.markdown("### ⚡ Priority Score")
        priority = analysis["priority_score"]
        st.markdown(f"**{priority}**")
    
    # Suggested Labels
    st.markdown("### 🏷️ Suggested Labels")
    labels_html = " ".join([
        f'<span style="background-color: #e1e4e8; padding: 3px 10px; border-radius: 10px; margin: 2px; display: inline-block;">{label}</span>'
        for label in analysis["suggested_labels"]
    ])
    st.markdown(labels_html, unsafe_allow_html=True)
    
    # Potential Impact
    st.markdown("### 💥 Potential Impact")
    st.warning(analysis["potential_impact"])
    
    # JSON Output (collapsible)
    with st.expander("📄 View Raw JSON Output"):
        st.json(analysis)
        
        # Copy button
        json_str = json.dumps(analysis, indent=2)
        st.code(json_str, language="json")
        st.button("📋 Copy JSON", key="copy_json", help="Click to copy JSON to clipboard")


def main():
    """Main application"""
    
    # Header
    st.markdown("<h1 class='main-header'>🤖 AI-Powered GitHub Issue Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
    <b>How it works:</b> Enter a GitHub repository URL and issue number. 
    The AI will analyze the issue and provide insights including summary, type, priority, labels, and potential impact.
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    with st.form("issue_form"):
        st.markdown("### 🔗 Enter GitHub Issue Details")
        
        # Repository URL
        repo_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/facebook/react",
            help="Enter the full GitHub repository URL"
        )
        
        # Issue number
        issue_number = st.number_input(
            "Issue Number",
            min_value=1,
            value=1,
            step=1,
            help="Enter the issue number (must be greater than 0)"
        )
        
        # Submit button
        submit_button = st.form_submit_button("🚀 Analyze Issue")
    
    # Process form submission
    if submit_button:
        if not repo_url:
            st.error("❌ Please enter a repository URL")
        elif not repo_url.startswith("http"):
            st.error("❌ Please enter a valid URL starting with http:// or https://")
        elif "github.com" not in repo_url:
            st.error("❌ Please enter a valid GitHub repository URL")
        else:
            # Analyze the issue
            analysis = analyze_issue(repo_url, issue_number)
            
            if analysis:
                display_analysis(analysis)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
    Built with ❤️ using FastAPI, LangChain, and Streamlit | 
    <a href='https://github.com/yourusername/github-issue-assistant' target='_blank'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with instructions
    with st.sidebar:
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. Enter a **public** GitHub repository URL
        2. Enter the **issue number** you want to analyze
        3. Click **Analyze Issue**
        4. View the AI-generated analysis
        
        ### 💡 Example Repositories
        - `https://github.com/facebook/react`
        - `https://github.com/microsoft/vscode`
        - `https://github.com/vercel/next.js`
        
        ### ⚙️ Configuration
        Make sure your `.env` file has:
        - `OPENAI_API_KEY` - Your OpenAI API key
        - `GITHUB_TOKEN` - (Optional) For higher rate limits
        """)


if __name__ == "__main__":
    main()
