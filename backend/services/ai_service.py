"""
AI Service - Analyze GitHub issues using LLM
"""

import os
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


# Define IssueAnalysis model here to avoid circular imports
class IssueAnalysis(BaseModel):
    """Response model for issue analysis"""
    summary: str = Field(..., description="One-sentence summary of the issue")
    type: str = Field(..., description="Issue type: bug, feature_request, documentation, question, or other")
    priority_score: str = Field(..., description="Priority score from 1-5 with justification")
    suggested_labels: list[str] = Field(..., description="2-3 relevant labels")
    potential_impact: str = Field(..., description="Potential impact on users")


# Initialize LLM
def get_llm():
    """Initialize and return OpenAI LLM"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables. "
            "Please add it to your .env file."
        )
    
    return ChatOpenAI(
        model="gpt-4o-mini",  # Using GPT-4 for best results
        temperature=0.3,  # Lower temperature for more consistent outputs
        api_key=api_key
    )


def create_analysis_prompt() -> ChatPromptTemplate:
    """
    Create a comprehensive prompt for issue analysis
    Uses few-shot prompting for better results
    """
    
    prompt_template = """You are an expert software engineer and project manager analyzing GitHub issues. Your task is to provide a structured analysis of the given issue.

**Issue Information:**
Repository: {repo_owner}/{repo_name}
Issue #{issue_number}: {title}

**Issue Description:**
{body}

**Comments ({comments_count} total):**
{comments}

---

**Your Task:**
Analyze the above GitHub issue and provide a structured JSON response with the following fields:

1. **summary**: A clear, one-sentence summary of the user's problem or request
2. **type**: Classify as ONE of: bug, feature_request, documentation, question, or other
3. **priority_score**: A score from 1 (low) to 5 (critical) with a brief justification (format: "3 - Justification here")
4. **suggested_labels**: An array of 2-3 relevant GitHub labels (e.g., ["bug", "UI", "high-priority"])
5. **potential_impact**: A brief sentence on the potential impact on users (especially important for bugs)

**Guidelines:**
- Be concise but informative
- Base priority on urgency, user impact, and severity
- Consider edge cases mentioned in comments
- If it's clearly a bug, rate priority higher
- For feature requests, consider user demand and alignment with project goals

**Example Output Format:**
{{
  "summary": "User unable to login due to OAuth redirect failure in production",
  "type": "bug",
  "priority_score": "4 - Critical login functionality broken, affects all OAuth users",
  "suggested_labels": ["bug", "authentication", "high-priority"],
  "potential_impact": "All users using OAuth authentication cannot login, blocking access to the application"
}}

Now analyze the issue and provide your response in valid JSON format:"""

    return ChatPromptTemplate.from_template(prompt_template)


def format_comments_for_prompt(comments: list) -> str:
    """Format comments for LLM prompt"""
    if not comments:
        return "No comments yet."
    
    # Limit to first 5 comments to avoid token limits
    comments_to_include = comments[:5]
    formatted = []
    
    for i, comment in enumerate(comments_to_include, 1):
        user = comment.get("user", "Unknown")
        body = comment.get("body", "")
        # Truncate very long comments
        if len(body) > 500:
            body = body[:500] + "... [truncated]"
        formatted.append(f"Comment {i} by @{user}:\n{body}")
    
    if len(comments) > 5:
        formatted.append(f"\n... and {len(comments) - 5} more comments")
    
    return "\n\n".join(formatted)


async def analyze_issue_with_ai(issue_data: Dict[str, Any]) -> IssueAnalysis:
    """
    Analyze GitHub issue using LLM
    
    Args:
        issue_data: Dictionary containing issue information from GitHub
        
    Returns:
        IssueAnalysis: Structured analysis result
    """
    try:
        # Initialize LLM
        llm = get_llm()
        
        # Create prompt
        prompt = create_analysis_prompt()
        
        # Format issue body (handle None and truncate if too long)
        body = issue_data.get("body", "") or "No description provided."
        if len(body) > 2000:
            body = body[:2000] + "... [truncated for length]"
        
        # Format comments
        comments_text = format_comments_for_prompt(issue_data.get("comments", []))
        
        # Prepare prompt variables
        prompt_vars = {
            "repo_owner": issue_data.get("repo_owner", ""),
            "repo_name": issue_data.get("repo_name", ""),
            "issue_number": issue_data.get("issue_number", ""),
            "title": issue_data.get("title", ""),
            "body": body,
            "comments_count": issue_data.get("comments_count", 0),
            "comments": comments_text
        }
        
        # Create the full prompt
        messages = prompt.format_messages(**prompt_vars)
        
        # Get LLM response
        response = llm.invoke(messages)
        response_text = response.content
        
        # Parse JSON response
        # Try to extract JSON if it's wrapped in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parse the JSON
        analysis_dict = json.loads(response_text)
        
        # Validate and create IssueAnalysis object
        analysis = IssueAnalysis(**analysis_dict)
        
        return analysis
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {response_text}")
    except Exception as e:
        raise ValueError(f"Error during AI analysis: {str(e)}")
