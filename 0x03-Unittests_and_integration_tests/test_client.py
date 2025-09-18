#!/usr/bin/env python3
"""Integration tests for GithubOrgClient"""
import unittest
from unittest.mock import patch
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        """Start patcher"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = [
            TEST_PAYLOAD["org"], TEST_PAYLOAD["repos"]
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test all repos"""
        client = GithubOrgClient("google")
        expected = [repo["name"] for repo in TEST_PAYLOAD["repos"]]
        self.assertEqual(client.public_repos(), expected)

    def test_public_repos_with_license(self):
        """Test repos filtered by license"""
        client = GithubOrgClient("google")
        expected = [
            repo["name"] for repo in TEST_PAYLOAD["repos"]
            if repo["license"]["key"] == "apache-2.0"
        ]
        self.assertEqual(client.public_repos(license="apache-2.0"), expected)


if __name__ == "__main__":
    unittest.main()
