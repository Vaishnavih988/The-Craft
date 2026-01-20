"""
Tests for GitHub Service
Run with: pytest tests/test_github_service.py
"""

import pytest
from backend.services.github_service import parse_repo_url


def test_parse_repo_url_standard():
    """Test parsing standard GitHub URL"""
    owner, repo = parse_repo_url("https://github.com/facebook/react")
    assert owner == "facebook"
    assert repo == "react"


def test_parse_repo_url_with_git():
    """Test parsing GitHub URL with .git extension"""
    owner, repo = parse_repo_url("https://github.com/facebook/react.git")
    assert owner == "facebook"
    assert repo == "react"


def test_parse_repo_url_trailing_slash():
    """Test parsing GitHub URL with trailing slash"""
    owner, repo = parse_repo_url("https://github.com/facebook/react/")
    assert owner == "facebook"
    assert repo == "react"


def test_parse_repo_url_invalid():
    """Test parsing invalid URL"""
    with pytest.raises(ValueError):
        parse_repo_url("https://gitlab.com/someuser/somerepo")


def test_parse_repo_url_incomplete():
    """Test parsing incomplete URL"""
    with pytest.raises(ValueError):
        parse_repo_url("https://github.com/facebook")
