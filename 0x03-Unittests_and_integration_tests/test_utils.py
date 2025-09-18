#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map and get_json."""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Ensure access_nested_map returns expected results for given inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Ensure KeyError is raised with the correct message when key is missing."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @patch('utils.requests.get')  # Patch 'requests.get' in the utils module
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns the expected result with mocked HTTP calls."""

        # Create a mock response object with a json method
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload
        
        # Configure the mock to return the mock_response
        mock_get.return_value = mock_response
        
        # Call the get_json function
        result = get_json(test_url)

        # Assert the mock was called once with the correct URL
        mock_get.assert_called_once_with(test_url)
        
        # Assert the returned result matches the test_payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
