"""
GitHub Issue Assistant - Backend API
FastAPI application for analyzing GitHub issues using AI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="GitHub Issue Assistant API",
    description="AI-powered GitHub issue analysis",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request model for issue analysis"""
    repo_url: str = Field(..., description="GitHub repository URL", json_schema_extra={"example": "https://github.com/facebook/react"})
    issue_number: int = Field(..., description="Issue number", gt=0, json_schema_extra={"example": 123})


class IssueAnalysis(BaseModel):
    """Response model for issue analysis"""
    summary: str = Field(..., description="One-sentence summary of the issue")
    type: str = Field(..., description="Issue type: bug, feature_request, documentation, question, or other")
    priority_score: str = Field(..., description="Priority score from 1-5 with justification")
    suggested_labels: List[str] = Field(..., description="2-3 relevant labels")
    potential_impact: str = Field(..., description="Potential impact on users")
    

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "GitHub Issue Assistant API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=IssueAnalysis)
async def analyze_issue(request: AnalyzeRequest):
    """
    Analyze a GitHub issue using AI
    
    Args:
        request: AnalyzeRequest containing repo URL and issue number
        
    Returns:
        IssueAnalysis: Structured analysis of the issue
    """
    try:
        # Import services
        from services.github_service import fetch_issue_data
        from services.ai_service import analyze_issue_with_ai
        
        # Fetch issue data from GitHub
        issue_data = await fetch_issue_data(request.repo_url, request.issue_number)
        
        # Analyze with AI
        analysis = await analyze_issue_with_ai(issue_data)
        
        return analysis
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
