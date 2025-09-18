#!/usr/bin/env python3
"""
Client module for the Github API.
"""

# Try relative import first (works when used as a package).
# Fallback to absolute import (works when run as a script).
try:
    from .utils import get_json
except Exception:
    from utils import get_json


class GithubOrgClient:
    """A client to interact with GitHub organizations."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        """Initialize with organization name."""
        self._org_name = org_name

    @property
    def org(self):
        """Return organization data from GitHub API."""
        return get_json(self.ORG_URL.format(self._org_name))

    @property
    def _public_repos_url(self):
        """Return public repos URL from the org payload."""
        return self.org.get("repos_url")

    def public_repos(self):
        """Return a list with names of public repositories."""
        repos = get_json(self._public_repos_url)
        return [repo.get("name") for repo in repos]
