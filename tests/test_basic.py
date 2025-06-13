"""
Basic test to verify test setup works
"""
import pytest


def test_basic_math():
    """Test basic math to verify pytest works"""
    assert 1 + 1 == 2


def test_basic_string():
    """Test basic string operations"""
    assert "hello" + " world" == "hello world"


class TestBasicClass:
    """Test class structure"""
    
    def test_class_method(self):
        """Test method in class"""
        assert True is True