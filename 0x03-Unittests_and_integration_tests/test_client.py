#!/usr/bin/env python3
"""Unit tests for GithubOrgClient._public_repos_url."""

import unittest
from unittest.mock import patch, MagicMock
from client import GithubOrgClient  # Adjust the import if necessary


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @patch.object(GithubOrgClient, 'org', return_value={"repos_url": "https://api.github.com/orgs/test_org/repos"})
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct URL."""
        
        # Create an instance of the GithubOrgClient with a mock org name
        client = GithubOrgClient("test_org")

        # Assert that _public_repos_url returns the mocked URL
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test_org/repos")
        
        # Assert that the mock org method was called once
        mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
