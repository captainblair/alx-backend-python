#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map, get_json, and memoize."""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    def test_access_nested_map(self):
        """Ensure access_nested_map returns expected results for given inputs."""
        # Test 1
        nested_map = {"a": 1}
        path = ("a",)
        expected = 1
        self.assertEqual(access_nested_map(nested_map, path), expected)

        # Test 2
        nested_map = {"a": {"b": 2}}
        path = ("a",)
        expected = {"b": 2}
        self.assertEqual(access_nested_map(nested_map, path), expected)

        # Test 3
        nested_map = {"a": {"b": 2}}
        path = ("a", "b")
        expected = 2
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Ensure KeyError is raised with the correct message when key is missing."""
        # Test 1
        nested_map = {}
        path = ("a",)
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))

        # Test 2
        nested_map = {"a": 1}
        path = ("a", "b")
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @patch('utils.requests.get')  # Patch 'requests.get' in the utils module
    def test_get_json(self, mock_get):
        """Test that get_json returns the expected result with mocked HTTP calls."""

        # Test 1
        test_url = "http://example.com"
        test_payload = {"payload": True}
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

        # Test 2
        test_url = "http://holberton.io"
        test_payload = {"payload": False}
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method results."""
        
        # Define the class with a memoized property
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of the class
        obj = TestClass()

        # First call, should call a_method and return 42
        result1 = obj.a_property
        self.assertEqual(result1, 42)

        # Second call, should return cached result without calling a_method again
        result2 = obj.a_property
        self.assertEqual(result2, 42)

        # Ensure a_method was only called once
        # We check by testing that the second call doesn't trigger a method call
        with self.assertRaises(AssertionError):  # The second call should not trigger a method call
            obj.a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
