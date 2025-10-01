import os
import sys
import django
from django.conf import settings

def run_tests():
    # Configure Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging.settings')
    django.setup()
    
    # Run the tests
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(['messaging.tests_threaded_conversations_fixed'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    run_tests()
