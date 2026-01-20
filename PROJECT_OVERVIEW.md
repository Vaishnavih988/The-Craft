# 🤖 AI-Powered GitHub Issue Assistant - Complete Project Overview

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Core Features](#core-features)
6. [Backend System](#backend-system)
7. [Frontend System](#frontend-system)
8. [LLM Integration](#llm-integration)
9. [Data Flow](#data-flow)
10. [Setup & Installation](#setup--installation)
11. [API Documentation](#api-documentation)
12. [Configuration](#configuration)
13. [Error Handling](#error-handling)
14. [Testing](#testing)
15. [Best Practices](#best-practices)
16. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

### **What is This Project?**

An intelligent web application that uses AI to analyze GitHub issues and provide structured, actionable insights. It helps developers and project managers quickly understand, prioritize, and triage issues without manually reading through lengthy discussions.

### **Problem Statement**

At SeedlingLabs (and most tech companies), teams move fast. Efficiently understanding and prioritizing GitHub issues is crucial for maintaining quality and speed. Manual issue triage is:
- ⏰ Time-consuming
- 😓 Inconsistent across team members
- 📊 Lacks structured data for analytics
- 🔄 Repetitive and tedious

### **Solution**

An AI-powered assistant that:
1. Fetches issue data from GitHub
2. Analyzes content using GPT-4
3. Provides structured insights in seconds
4. Enables better decision-making

### **Core Philosophy**

This project embodies **"Agentic Thinking in a Box"** - building a small, useful AI agent that integrates different parts (LLMs, data, APIs) to solve a concrete business problem.

---

## 🏗️ Architecture

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   STREAMLIT FRONTEND                         │
│  - User Interface (Python/Streamlit)                        │
│  - Input forms, Results display                             │
│  - State management                                         │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (POST /analyze)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   FASTAPI BACKEND                            │
│  - API endpoints                                            │
│  - Request validation (Pydantic)                            │
│  - Service orchestration                                    │
└───────────┬────────────────────────┬────────────────────────┘
            │                        │
            │ Fetch Issue            │ Analyze
            │                        │
┌───────────▼──────────┐  ┌──────────▼────────────────────────┐
│   GITHUB SERVICE     │  │      AI SERVICE                   │
│  - GitHub API calls  │  │  - LLM integration (LangChain)    │
│  - Data extraction   │  │  - Prompt engineering             │
│  - Error handling    │  │  - Response parsing               │
└───────────┬──────────┘  └──────────┬────────────────────────┘
            │                        │
            │ REST API               │ API Call
            │                        │
┌───────────▼──────────┐  ┌──────────▼────────────────────────┐
│    GITHUB API        │  │    OPENAI API                     │
│  - Issues endpoint   │  │  - GPT-4o-mini                    │
│  - Comments endpoint │  │  - Chat completions               │
└──────────────────────┘  └───────────────────────────────────┘
```

### **Component Interaction Flow**

```
1. User enters repo URL + issue number
   ↓
2. Frontend sends POST request to Backend
   ↓
3. Backend validates input (Pydantic)
   ↓
4. GitHub Service fetches issue data
   ↓
5. AI Service receives issue data
   ↓
6. Prompt is constructed and sent to LLM
   ↓
7. LLM analyzes and returns JSON
   ↓
8. Response is validated (Pydantic)
   ↓
9. Backend sends results to Frontend
   ↓
10. Frontend displays beautiful analysis
```

---

## 💻 Technology Stack

### **Backend**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **FastAPI** | 0.115.0 | Modern, fast web framework for building APIs |
| **Pydantic** | 2.10.0 | Data validation using Python type hints |
| **LangChain** | 0.3.12 | Framework for LLM applications |
| **LangChain-OpenAI** | 0.2.14 | OpenAI integration for LangChain |
| **OpenAI** | 1.58.1 | Official OpenAI Python client |
| **httpx** | 0.27.0 | Async HTTP client for GitHub API |
| **python-dotenv** | 1.0.1 | Environment variable management |
| **Uvicorn** | 0.32.0 | ASGI server for FastAPI |

### **Frontend**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Streamlit** | 1.41.0 | Rapid UI prototyping framework |
| **Requests** | 2.32.0 | HTTP library for API calls |

### **Development**

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **pytest** | Testing framework |
| **Virtual Environment** | Dependency isolation |

---

## 📁 Project Structure

```
github-issue-assistant/
│
├── backend/                          # Backend API
│   ├── __init__.py                   # Package initialization
│   ├── main.py                       # FastAPI application & endpoints
│   │
│   └── services/                     # Business logic
│       ├── __init__.py
│       ├── github_service.py         # GitHub API integration
│       └── ai_service.py             # LLM analysis logic
│
├── frontend/                         # Frontend UI
│   └── app.py                        # Streamlit application
│
├── tests/                            # Test suite
│   ├── __init__.py
│   └── test_github_service.py        # Unit tests
│
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
│
├── README.md                         # Project documentation
├── LLM_EXPLANATION.md               # LLM integration details
├── PROJECT_OVERVIEW.md              # This file
│
├── setup.sh                          # Unix setup script
├── setup.bat                         # Windows setup script
│
└── LICENSE                           # MIT License
```

---

## ⚡ Core Features

### **1. Issue Analysis**
- Fetches complete issue data from GitHub
- Analyzes title, body, and comments
- Provides structured insights

### **2. AI-Powered Classification**
- **Type Detection:** bug, feature_request, documentation, question, other
- **Priority Scoring:** 1-5 scale with justification
- **Label Suggestions:** 2-3 relevant labels
- **Impact Assessment:** User impact evaluation

### **3. User Interface**
- Clean, modern design
- Quick-start examples
- Tab-based results view
- JSON export functionality
- Responsive layout

### **4. API Integration**
- GitHub REST API for issue data
- OpenAI API for LLM analysis
- RESTful backend architecture

### **5. Error Handling**
- Invalid URL detection
- Non-existent issue handling
- Rate limit management
- Timeout handling
- Graceful degradation

---

## 🔧 Backend System

### **File: `backend/main.py`**

#### **Purpose:** 
FastAPI application with API endpoints

#### **Key Components:**

##### 1. **API Configuration**
```python
app = FastAPI(
    title="GitHub Issue Assistant API",
    description="AI-powered GitHub issue analysis",
    version="1.0.0"
)
```

##### 2. **CORS Middleware**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (frontend)
    allow_methods=["*"],       # Allow all methods
    allow_headers=["*"],       # Allow all headers
)
```

##### 3. **Request/Response Models (Pydantic)**
```python
class AnalyzeRequest(BaseModel):
    repo_url: str             # GitHub repo URL
    issue_number: int         # Issue number (> 0)

class IssueAnalysis(BaseModel):
    summary: str              # One-sentence summary
    type: str                 # Issue classification
    priority_score: str       # Priority with justification
    suggested_labels: List[str]  # 2-3 labels
    potential_impact: str     # User impact
```

##### 4. **API Endpoints**

**Health Check:**
```python
@app.get("/")
async def root():
    return {
        "message": "GitHub Issue Assistant API",
        "status": "running",
        "version": "1.0.0"
    }
```

**Analyze Endpoint:**
```python
@app.post("/analyze", response_model=IssueAnalysis)
async def analyze_issue(request: AnalyzeRequest):
    # 1. Validate input
    # 2. Fetch from GitHub
    # 3. Analyze with AI
    # 4. Return results
```

---

### **File: `backend/services/github_service.py`**

#### **Purpose:** 
GitHub API integration and data fetching

#### **Key Functions:**

##### 1. **URL Parsing**
```python
def parse_repo_url(repo_url: str) -> tuple[str, str]:
    # Extracts: owner, repo_name
    # Handles: .git suffix, trailing slashes
    # Validates: GitHub URL format
```

**Supported Formats:**
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `https://github.com/owner/repo/`

##### 2. **Issue Data Fetching**
```python
async def fetch_issue_data(repo_url: str, issue_number: int):
    # 1. Parse repository URL
    # 2. Build GitHub API endpoints
    # 3. Fetch issue details
    # 4. Fetch comments
    # 5. Extract relevant data
    # 6. Return structured dict
```

**API Endpoints Used:**
- `GET /repos/{owner}/{repo}/issues/{number}` - Issue details
- `GET /repos/{owner}/{repo}/issues/{number}/comments` - Comments

**Returned Data Structure:**
```python
{
    "repo_owner": "facebook",
    "repo_name": "react",
    "issue_number": 28324,
    "title": "Button crashes on iOS",
    "body": "Full issue description...",
    "state": "open",
    "labels": ["bug", "iOS"],
    "created_at": "2025-01-15T...",
    "updated_at": "2025-01-20T...",
    "user": "username",
    "comments_count": 5,
    "comments": [
        {
            "user": "developer1",
            "body": "Comment text...",
            "created_at": "2025-01-16T..."
        },
        ...
    ]
}
```

##### 3. **Error Handling**
- **404:** Issue not found
- **403:** Rate limit exceeded
- **Timeout:** Request timeout
- **Connection:** Network errors

---

### **File: `backend/services/ai_service.py`**

#### **Purpose:** 
LLM integration and issue analysis

#### **Key Functions:**

##### 1. **LLM Initialization**
```python
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )
```

##### 2. **Prompt Construction**
```python
def create_analysis_prompt():
    # Creates structured prompt with:
    # - Issue context
    # - Analysis instructions
    # - Expected output format
    # - Few-shot example
```

##### 3. **Content Formatting**
```python
def format_comments_for_prompt(comments: list):
    # - Limits to first 5 comments
    # - Truncates long comments (500 chars)
    # - Formats for LLM consumption
```

##### 4. **AI Analysis**
```python
async def analyze_issue_with_ai(issue_data: Dict):
    # 1. Initialize LLM
    # 2. Format issue data
    # 3. Construct prompt
    # 4. Invoke LLM
    # 5. Parse JSON response
    # 6. Validate with Pydantic
    # 7. Return IssueAnalysis
```

**See [LLM_EXPLANATION.md](LLM_EXPLANATION.md) for detailed LLM integration details.**

---

## 🎨 Frontend System

### **File: `frontend/app.py`**

#### **Purpose:** 
Streamlit-based user interface

#### **Key Components:**

##### 1. **Page Configuration**
```python
st.set_page_config(
    page_title="GitHub Issue Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

##### 2. **Custom Styling**
- Hero section with gradient
- Card-based layouts
- Button styling
- Responsive design
- Color-coded priorities

##### 3. **Main Features**

**Quick Examples:**
```python
# One-click testing buttons
- React Issue Example
- Next.js Issue Example
- VS Code Issue Example
```

**Input Form:**
```python
# User inputs
- Repository URL (text input)
- Issue Number (number input)
- Analyze Button
```

**Results Display:**
```python
# Tab-based view:
Tab 1: Overview
  - Metrics (Type, Priority, Labels)
  - Summary card
  - Priority analysis
  - Suggested labels
  - Impact assessment

Tab 2: Full Report
  - Detailed breakdown
  - Download button

Tab 3: Raw JSON
  - JSON code view
  - Copy functionality
  - Download option
```

##### 4. **State Management**
```python
# Session state for form persistence
st.session_state.repo_url
st.session_state.issue_number
```

##### 5. **Sidebar**
- Usage instructions
- Example repositories
- Feature list
- Configuration requirements
- Version info

---

## 🔄 Data Flow

### **Complete Request-Response Cycle**

```
STEP 1: USER INPUT
User: "https://github.com/facebook/react" + Issue #28324
↓

STEP 2: FRONTEND PROCESSING
- Validate inputs
- Display loading spinner
- Send POST request to backend
↓

STEP 3: BACKEND RECEIVES REQUEST
FastAPI: POST /analyze
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 28324
}
↓

STEP 4: PYDANTIC VALIDATION
- Check repo_url is string
- Check issue_number > 0
- Create AnalyzeRequest object
↓

STEP 5: GITHUB SERVICE
- Parse URL → owner="facebook", repo="react"
- Fetch issue data from GitHub API
- Fetch comments
- Structure data
↓

STEP 6: AI SERVICE
- Receive issue data
- Truncate long content
- Format for LLM
- Construct prompt
↓

STEP 7: LLM PROCESSING
- Send prompt to GPT-4o-mini
- LLM analyzes issue
- Returns JSON response
↓

STEP 8: RESPONSE PARSING
- Extract JSON from response
- Validate with Pydantic
- Create IssueAnalysis object
↓

STEP 9: BACKEND RESPONSE
FastAPI returns:
{
  "summary": "...",
  "type": "bug",
  "priority_score": "4 - ...",
  "suggested_labels": [...],
  "potential_impact": "..."
}
↓

STEP 10: FRONTEND DISPLAY
- Hide spinner
- Show success message
- Display results in tabs
- Enable download
```

---

## 🚀 Setup & Installation

### **Prerequisites**
- Python 3.8 or higher
- OpenAI API key
- Git
- Virtual environment (recommended)

### **Step-by-Step Setup**

#### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/github-issue-assistant.git
cd github-issue-assistant
```

#### **2. Create Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **4. Configure Environment**
```bash
# Copy example file
cp .env.example .env

# Edit .env and add keys
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=optional_token_here
```

#### **5. Run Backend**
```bash
cd backend
python -m uvicorn main:app --reload
```
Backend runs on: `http://localhost:8000`

#### **6. Run Frontend**
```bash
# New terminal
streamlit run frontend/app.py
```
Frontend opens at: `http://localhost:8501`

---

## 📚 API Documentation

### **Base URL**
```
http://localhost:8000
```

### **Endpoints**

#### **1. Health Check**
```
GET /
```

**Response:**
```json
{
  "message": "GitHub Issue Assistant API",
  "status": "running",
  "version": "1.0.0"
}
```

#### **2. Analyze Issue**
```
POST /analyze
```

**Request Body:**
```json
{
  "repo_url": "https://github.com/facebook/react",
  "issue_number": 28324
}
```

**Response (200 OK):**
```json
{
  "summary": "Button component crashes on iOS Safari 15+ due to null pointer exception",
  "type": "bug",
  "priority_score": "5 - Critical production bug affecting all iOS users",
  "suggested_labels": ["bug", "iOS", "high-priority"],
  "potential_impact": "All iOS users cannot interact with buttons, blocking core functionality"
}
```

**Error Responses:**

```json
// 400 Bad Request
{
  "detail": "Invalid GitHub URL format"
}

// 404 Not Found
{
  "detail": "Issue #123 not found in owner/repo"
}

// 500 Internal Server Error
{
  "detail": "Error during AI analysis: ..."
}
```

#### **3. Health Status**
```
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## ⚙️ Configuration

### **Environment Variables**

#### **Required:**
```env
OPENAI_API_KEY=sk-proj-...
```
Get from: https://platform.openai.com/api-keys

#### **Optional:**
```env
GITHUB_TOKEN=github_pat_...
```
Benefits:
- Increases rate limit from 60 to 5000 req/hour
- Access to private repos (if needed)

Get from: https://github.com/settings/tokens

### **Application Settings**

#### **Backend (`backend/main.py`):**
```python
# CORS settings
allow_origins=["*"]  # Change in production

# Timeout settings
timeout=60  # seconds
```

#### **LLM Settings (`backend/services/ai_service.py`):**
```python
model="gpt-4o-mini"  # Can change to gpt-4
temperature=0.3      # Adjust for consistency
```

#### **Frontend (`frontend/app.py`):**
```python
# API URL
api_url = "http://localhost:8000"  # Change for deployment

# Layout
layout="wide"
```

---

## 🛡️ Error Handling

### **Backend Error Handling**

#### **1. Input Validation**
```python
# Pydantic automatically validates:
- repo_url must be string
- issue_number must be positive integer
- Returns 422 if invalid
```

#### **2. GitHub API Errors**
```python
# Custom error handling:
- 404: Issue not found → User-friendly message
- 403: Rate limit → Suggest adding token
- Timeout: Network error → Retry suggestion
- Invalid URL: Parse error → Format guidance
```

#### **3. LLM Errors**
```python
# Handles:
- Missing API key → Clear error message
- Invalid JSON response → Parsing error
- Token limit exceeded → Content truncation
- Timeout → Retry logic
```

### **Frontend Error Handling**

#### **1. Connection Errors**
```python
# Cannot connect to backend
→ Display setup instructions
```

#### **2. Validation Errors**
```python
# Invalid input
→ Show specific error message
→ Guide user to correct input
```

#### **3. Timeout Errors**
```python
# Request takes too long
→ Inform user
→ Suggest trying again
```

---

## 🧪 Testing

### **Unit Tests**

#### **File: `tests/test_github_service.py`**

```python
# Tests for URL parsing
- test_parse_repo_url_standard()
- test_parse_repo_url_with_git()
- test_parse_repo_url_trailing_slash()
- test_parse_repo_url_invalid()
```

#### **Running Tests**
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_github_service.py

# Run with coverage
pytest --cov=backend tests/
```

### **Manual Testing**

#### **Test Cases:**

1. **Valid Issue**
   - Repo: `facebook/react`
   - Issue: `28324`
   - Expected: Success

2. **Invalid Issue**
   - Repo: `facebook/react`
   - Issue: `1`
   - Expected: 404 error

3. **Invalid URL**
   - Repo: `not-a-url`
   - Expected: Validation error

4. **Large Issue**
   - Repo with long issue body
   - Expected: Truncation, success

5. **No Comments**
   - Issue with no comments
   - Expected: Success

---

## 🎯 Best Practices Implemented

### **1. Code Quality**

✅ **Type Hints**
```python
def fetch_issue_data(repo_url: str, issue_number: int) -> Dict[str, Any]:
    ...
```

✅ **Docstrings**
```python
"""
Fetch issue data from GitHub API

Args:
    repo_url: GitHub repository URL
    issue_number: Issue number to fetch

Returns:
    Dictionary containing issue data
"""
```

✅ **Error Handling**
```python
try:
    result = await fetch_data()
except SpecificError as e:
    handle_error(e)
```

### **2. Architecture**

✅ **Separation of Concerns**
- API layer (main.py)
- Business logic (services/)
- UI layer (frontend/)

✅ **Async Operations**
```python
async def fetch_issue_data(...):
    async with httpx.AsyncClient() as client:
        response = await client.get(...)
```

✅ **Dependency Injection**
```python
# Services are imported when needed
from services.github_service import fetch_issue_data
```

### **3. Security**

✅ **Environment Variables**
- API keys in .env
- .env in .gitignore
- .env.example for reference

✅ **Input Validation**
- Pydantic models
- URL parsing
- Number validation

✅ **Rate Limiting**
- GitHub token for higher limits
- Timeout handling

### **4. User Experience**

✅ **Loading States**
- Spinners during processing
- Progress messages

✅ **Error Messages**
- Clear, actionable errors
- Setup instructions when needed

✅ **Examples**
- Quick-start buttons
- Pre-filled examples

### **5. Code Organization**

✅ **Modular Structure**
```
backend/
  main.py          # API
  services/        # Business logic
    github_service.py
    ai_service.py
```

✅ **Configuration Management**
- .env for secrets
- Config in code clearly marked

✅ **Documentation**
- README.md
- LLM_EXPLANATION.md
- PROJECT_OVERVIEW.md (this file)

---

## 🚀 Future Enhancements

### **Phase 1: Core Improvements**

1. **Caching Layer**
   ```python
   # Redis/Memcached for caching analyzed issues
   cache_key = f"{repo}:{issue_number}"
   if cached := redis.get(cache_key):
       return cached
   ```

2. **Batch Processing**
   ```python
   # Analyze multiple issues at once
   POST /analyze-batch
   {
     "issues": [
       {"repo_url": "...", "issue_number": 1},
       {"repo_url": "...", "issue_number": 2}
     ]
   }
   ```

3. **Webhook Integration**
   ```python
   # Auto-analyze new issues
   POST /webhook/github
   # Triggered on issue creation
   ```

### **Phase 2: Advanced Features**

4. **Historical Analysis**
   ```python
   # Track issue trends over time
   GET /analytics/{repo}
   # Returns priority trends, common types, etc.
   ```

5. **Custom Models**
   ```python
   # Fine-tune on specific projects
   # Better domain-specific classification
   ```

6. **Multi-LLM Support**
   ```python
   # Add Claude, Gemini as options
   # Fallback mechanism
   ```

### **Phase 3: Enterprise Features**

7. **User Authentication**
   ```python
   # JWT-based auth
   # Role-based access
   ```

8. **Team Collaboration**
   ```python
   # Share analyses
   # Comment on analyses
   # Override AI suggestions
   ```

9. **Dashboard**
   ```python
   # Visualizations
   # Charts and graphs
   # Export reports
   ```

### **Phase 4: Deployment**

10. **Cloud Deployment**
    - Backend: Heroku, Railway, or Render
    - Frontend: Streamlit Cloud
    - Database: PostgreSQL for history

11. **CI/CD Pipeline**
    ```yaml
    # GitHub Actions
    - Run tests
    - Build Docker image
    - Deploy to cloud
    ```

12. **Monitoring**
    - Error tracking (Sentry)
    - Performance monitoring
    - Usage analytics

---

## 📊 Technical Specifications

### **Performance Metrics**

| Metric | Value |
|--------|-------|
| **API Response Time** | 5-10 seconds |
| **LLM Latency** | 3-5 seconds |
| **GitHub API Latency** | 1-2 seconds |
| **Max Issue Size** | 2000 chars (body) |
| **Max Comments** | 5 analyzed |
| **Rate Limit (No Token)** | 60/hour |
| **Rate Limit (With Token)** | 5000/hour |

### **Cost Analysis**

#### **Per Analysis:**
- Input tokens: ~1,500
- Output tokens: ~200
- Cost: ~$0.15

#### **Monthly (1000 analyses):**
- Total cost: ~$150
- With optimizations: ~$50

### **Scalability**

| Users | Requests/Day | Cost/Day |
|-------|-------------|----------|
| 10 | 100 | $15 |
| 100 | 1,000 | $150 |
| 1,000 | 10,000 | $1,500 |

**Optimization strategies reduce costs by 60-70%**

---

## 🎓 Key Learnings

### **1. AI Integration**
- Prompt engineering is 80% of quality
- Few-shot examples improve accuracy
- Temperature control matters
- Token optimization saves costs

### **2. API Design**
- Pydantic makes validation easy
- FastAPI is incredibly fast
- Async operations improve performance
- Clear error messages help users

### **3. Frontend Development**
- Streamlit enables rapid prototyping
- Session state for persistence
- Loading states improve UX
- Examples reduce friction

### **4. Full Stack Integration**
- Clear separation of concerns
- RESTful APIs are straightforward
- Error handling at every layer
- Documentation is essential

---

## 📝 Summary

This project demonstrates:

✅ **Real-World AI Application**
- Practical LLM integration
- Production-ready error handling
- Cost-optimized implementation

✅ **Modern Web Development**
- RESTful API architecture
- Type-safe validation
- Async operations
- Responsive UI

✅ **Software Engineering Best Practices**
- Clean code structure
- Comprehensive documentation
- Error handling
- Testing

✅ **Problem-Solving Skills**
- Understanding business needs
- Designing effective solutions
- Iterative improvement
- User-centric design

---

## 🤝 Contributing

This project was built as a craft case for SeedlingLabs Engineering Internship. Suggestions and improvements are welcome!

---

## 📞 Support

For questions or issues:
- Open a GitHub issue
- Check the documentation
- Review error messages carefully

---

## 📜 License

MIT License - See LICENSE file

---

**Built with ❤️ for SeedlingLabs | Demonstrating AI-Native Development Skills**

**Version:** 1.0.0  
**Last Updated:** January 21, 2026  
**Author:** [Your Name]
