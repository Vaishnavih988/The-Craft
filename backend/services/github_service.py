"""
GitHub Service - Fetch issue data from GitHub API
"""

import os
import re
import httpx
from typing import Dict, Any, Optional


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""
    pass


def parse_repo_url(repo_url: str) -> tuple[str, str]:
    """
    Parse GitHub repository URL to extract owner and repo name
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Tuple of (owner, repo_name)
        
    Raises:
        ValueError: If URL format is invalid
    """
    # Support various GitHub URL formats
    patterns = [
        r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
        r"github\.com/([^/]+)/([^/]+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, repo_url)
        if match:
            owner, repo = match.groups()
            # Remove .git suffix if present
            repo = repo.rstrip('.git')
            return owner, repo
    
    raise ValueError(
        f"Invalid GitHub URL format: {repo_url}. "
        "Expected format: https://github.com/owner/repo"
    )


async def fetch_issue_data(repo_url: str, issue_number: int) -> Dict[str, Any]:
    """
    Fetch issue data from GitHub API
    
    Args:
        repo_url: GitHub repository URL
        issue_number: Issue number to fetch
        
    Returns:
        Dictionary containing issue data (title, body, comments)
        
    Raises:
        ValueError: If URL is invalid
        GitHubAPIError: If GitHub API request fails
    """
    # Parse repository URL
    owner, repo = parse_repo_url(repo_url)
    
    # GitHub API endpoints
    issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    # Prepare headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Issue-Assistant"
    }
    
    # Add authentication token if available (for higher rate limits)
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    async with httpx.AsyncClient() as client:
        try:
            # Fetch issue details
            issue_response = await client.get(issue_url, headers=headers, timeout=10.0)
            
            if issue_response.status_code == 404:
                raise GitHubAPIError(
                    f"Issue #{issue_number} not found in {owner}/{repo}. "
                    "Please check the repository URL and issue number."
                )
            elif issue_response.status_code == 403:
                raise GitHubAPIError(
                    "GitHub API rate limit exceeded. Please add a GITHUB_TOKEN to your .env file."
                )
            elif issue_response.status_code != 200:
                raise GitHubAPIError(
                    f"GitHub API error: {issue_response.status_code} - {issue_response.text}"
                )
            
            issue_data = issue_response.json()
            
            # Fetch comments
            comments_response = await client.get(comments_url, headers=headers, timeout=10.0)
            comments_data = []
            
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
            
            # Extract relevant information
            result = {
                "repo_owner": owner,
                "repo_name": repo,
                "issue_number": issue_number,
                "title": issue_data.get("title", ""),
                "body": issue_data.get("body", "") or "",  # Handle None body
                "state": issue_data.get("state", ""),
                "labels": [label["name"] for label in issue_data.get("labels", [])],
                "created_at": issue_data.get("created_at", ""),
                "updated_at": issue_data.get("updated_at", ""),
                "user": issue_data.get("user", {}).get("login", ""),
                "comments_count": issue_data.get("comments", 0),
                "comments": [
                    {
                        "user": comment.get("user", {}).get("login", ""),
                        "body": comment.get("body", ""),
                        "created_at": comment.get("created_at", "")
                    }
                    for comment in comments_data
                ]
            }
            
            return result
            
        except httpx.TimeoutException:
            raise GitHubAPIError("Request to GitHub API timed out. Please try again.")
        except httpx.RequestError as e:
            raise GitHubAPIError(f"Error connecting to GitHub API: {str(e)}")
