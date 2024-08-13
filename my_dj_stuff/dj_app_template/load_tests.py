"""This script replaces python manage.py test
"""

import sys
from unittest import TestSuite
from my_dj_stuff.dj_app_template.boot_django import boot_django

boot_django()

default_labels = ["dj_app1.tests", ]

def get_suite(labels=default_labels):
    """takes a list of test labels and directly calls the DiscoverRunner on them

    Args:
        labels (str, optional): Test label. Defaults to default_labels.

    Returns:
        TestSuite: TestSuite to run the tests - needed for external test tools
    """
    from django.test.runner import DiscoverRunner
    runner = DiscoverRunner(verbosity=1)
    # here the tests will be started
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)

    # In case this is called from setuptools, return a test suite
    return TestSuite()

if __name__ == "__main__":
    command_line_labels = sys.argv[1:]
    labels = command_line_labels if command_line_labels else default_labels
    get_suite(labels)