#!/usr/bin/env python3
"""
Unit tests for the client module.

This file contains tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    # ⚠️ IMPORTANT: choose the correct one depending on client.py
    @patch("client.get_json")        # if: from utils import get_json
    # @patch("client.utils.get_json")  # if: import utils
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and
        calls get_json exactly once with the expected argument.
        """
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert the return value is the mocked payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
