#!/usr/bin/env python3
"""
Unit and integration tests for the client module.

Tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
import client as client_module
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @patch.object(client_module, "get_json")
    def test_org_google(self, mock_get_json):
        """Test org returns expected value for 'google'."""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("google")
        result = client.org

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google"
        )
        self.assertEqual(result, test_payload)

    @patch.object(client_module, "get_json")
    def test_org_abc(self, mock_get_json):
        """Test org returns expected value for 'abc'."""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("abc")
        result = client.org

        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/abc"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url."""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("google")

            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch.object(client_module, "get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repo names."""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )

    def test_has_license_true(self):
        """Test has_license returns True when license matches."""
        repo = {"license": {"key": "my_license"}}
        self.assertTrue(GithubOrgClient.has_license(repo, "my_license"))

    def test_has_license_false(self):
        """Test has_license returns False when license does not match."""
        repo = {"license": {"key": "other_license"}}
        self.assertFalse(GithubOrgClient.has_license(repo, "my_license"))


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos)
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and configure side_effects for integration."""
        cls.get_patcher = patch("requests.get")
        cls.get_patcher_started = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["url"]:
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.repos_payload["url"]:
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload["repos"]
                return mock_resp
            else:
                raise ValueError(f"Unexpected URL: {url}")

        cls.get_patcher_started.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repo names."""
        client = GithubOrgClient(self.org_payload["login"])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)


if __name__ == "__main__":
    unittest.main()
