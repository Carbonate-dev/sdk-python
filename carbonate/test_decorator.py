import unittest
import functools

from carbonate.exceptions import TestException

def test_decorator(sdk_attribute_name: str = "carbonate_sdk"):
    def inner_decorator(func):
        @functools.wraps(func)
        def decorator(self, *args, **kwargs):
            if not hasattr(self, sdk_attribute_name):
                raise ValueError(f"Class {self.__class__.__name__} does not have a {sdk_attribute_name} attribute, please specify the attribute that holds your SDK instance in your @carbonate.test() decorator.")

            sdk = getattr(self, sdk_attribute_name)
            sdk.start_test(func.__module__, func.__name__)
            try:
                func(self, *args, **kwargs)
            except unittest.SkipTest:
                raise
            except Exception as e:  # pylint: disable=broad-except
                sdk.end_test()

                sdk.handle_test_failure(e)

            sdk.end_test()

        return decorator
    return inner_decorator