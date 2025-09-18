#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.public_repos."""

import unittest
from unittest.mock import patch, MagicMock
from client import GithubOrgClient  # Adjust the import if necessary


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @patch('client.get_json')  # Mock get_json globally in the client module
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct repos list."""
        
        # Define the payload for get_json mock
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        
        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url', return_value="https://api.github.com/orgs/test_org/repos"):
            # Create an instance of GithubOrgClient
            client = GithubOrgClient("test_org")

            # Call the public_repos method
            repos = client.public_repos()

            # Debugging: Print the returned list of repos
            print(f"Returned repos: {repos}")

            # Test that the returned list of repos matches the mocked payload
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Assert that the mocked _public_repos_url property was called once
            client._public_repos_url.assert_called_once()

            # Assert that the mocked get_json was called once with the expected URL
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")


if __name__ == "__main__":
    unittest.main()
