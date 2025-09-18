#!/usr/bin/env python3
"""
Integration tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient class"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get before all tests"""
        # Patch 'requests.get' so it returns TEST_PAYLOAD data
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        # Configure side_effect to return payloads in the right order
        mock_get.return_value.json.side_effect = [
            TEST_PAYLOAD["org"],
            TEST_PAYLOAD["repos"]
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        expected_repos = [repo["name"] for repo in TEST_PAYLOAD["repos"]]
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license"""
        client = GithubOrgClient("google")
        apache_repos = [
            repo["name"] for repo in TEST_PAYLOAD["repos"]
            if repo["license"]["key"] == "apache-2.0"
        ]
        self.assertEqual(client.public_repos(license="apache-2.0"), apache_repos)


if __name__ == "__main__":
    unittest.main()
