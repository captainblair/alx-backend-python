#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize decorator"""

    def test_memoize(self):
        """Test that a_method is only called once when memoized"""

        class TestClass:
            """Simple class to test memoization"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method so we can track calls
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Assertions
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # Ensure a_method is only called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
