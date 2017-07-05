import pytest
import lightningtrace


def test_seq_positive_integers():
    """
    Test to make sure that the sequence works with positive integers
    """
    res = lightningtrace.utils.seq(0, 6, 1)
    assert res == [0, 1, 2, 3, 4, 5, 6]


def test_seq_posititve_floats():
    """
    Test to make sure that the sequence works with positive floats
    """
    res = lightningtrace.utils.seq(0.0, 2.5, 0.5)
    assert res == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]


def test_seq_integers():
    """
    Test to make sure that the sequence works with positive and negative integers
    """
    res = lightningtrace.utils.seq(-2, 2, 1)
    assert res == [-2, -1, 0, 1, 2]


def test_seq_floats():
    """
    Test to make sure that the sequence works with positive and negative floats
    """
    res = lightningtrace.utils.seq(-0.5, 0.5, 0.5)
    assert res == [-0.5, 0.0, 0.5]
