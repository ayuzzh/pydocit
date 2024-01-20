"""
Author: Ayush K M
Date: 16.01.2024

This is the example docstring of the file example_documentation.
"""

"""
This will get ignored.
"""
from typing import List, Optional, Dict, Tuple, Union, Set


class ExampleClass:
    """This is documentation of class Example class"""

    def __init__(self):
        """This is docstring of __init__ method"""

        """This will get ignored too."""
        pass

    def example_method(self):
        """This is docstring of example_method method"""
        pass

    def method_with_all_explanations(
        self, a, b: int, c: float = 1.0, d="d", *args, **kwargs
    ):
        """This is docstring of method_with_all_explanations method

        This method takes parameters self, a, b, c, d, args and kwargs

        a is regular parameter
        b is typing hinted as int
        c is type hinted as float with default value 1.0
        d is regular parameter with default value "d"
        args takes n number of arguments
        kwargs takes n number of keyword arguments
        """
        pass


class ExampleClass2:
    """This is docstring of ExampleClass2 class"""

    pass


class ClassInheritsOtherClass(ExampleClass):
    """This is docstring of ClassInheritsOtherClass class which inherits
    class ExampleClass"""

    def example_method(self):
        """This is docstring of example_method method"""
        pass


class ClassInheritsTwoClasses(ExampleClass, ExampleClass2):
    """This is docstring of ClassInheritsTwoClasses class which inherits
    two classes ExampleClass and ExampleClass2"""

    def example_method(self):
        """This is docstring of example_method method"""
        pass


def example_function():
    """This is docstring of example_function function"""

    """This will get ignored too."""
    pass


def function_with_parameters(a, b, c):
    """This is docstring of example_function2 function
    with parameters a, b and c"""
    pass


def function_with_parameters_having_default_values(a, b="blabla", c="lala"):
    """This is docstring of function_with_parameters_having_default_values function
    with parameters a, b and c.
    b and c have default values "bla" and "lala" respectively"""
    pass


def function_with_annotations(a: int, b: str):
    """This is docstring of function_with_annotations function
    with parameters a and b.
    a and b have type hinting as int and str respectively"""
    pass


def function_with_vargs_and_vkw(a, *args, **kwargs):
    """This is docstring of function_with_vargs_and_vkw function
    with *args and **kwargs."""
    pass


def function_with_vargs_and_vkw_with_annotations(*args: int, **kwargs: float):
    """This is docstring of function_with_vargs_and_vkw_with_annotations function
    with *args and **kwargs.
    Here args and kwargs are type hinted as int and str respectively"""
    pass


def function_with_child_function():
    """This is docstring of function_with_child_function function
    with another function inside it."""

    def function_inside_a_function():
        """This function gets ignored during documentation generation"""
        pass


def function_with_annotations_derived_from_typing(a: List[int], b: Optional[str]):
    """This is docstring of function_with_child_function function
    with annotations derived from typing."""
    pass


def functions_with_return_annotations() -> str:
    """This is docstring of functions_with_return_annotations function
    with return annotations."""
    pass
