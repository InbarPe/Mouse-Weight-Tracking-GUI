import tempfile
from weight_parser import extract_weight

def write_tmp(content):
    f = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
    f.write(content)
    f.close()
    return f.name


def test_integer_weight():
    path = write_tmp("BW: 83% 21.2g")
    assert extract_weight(path) == 83.0


def test_decimal_weight():
    path = write_tmp("Some text BW: 81.5% more text")
    assert extract_weight(path) == 81.5


def test_weight_with_leading_whitespace():
    """Test extraction with extra whitespace around the BW value."""
    path = write_tmp("BW:  75.3%  some text")
    assert extract_weight(path) == 75.3


def test_weight_case_insensitive():
    """Test that BW extraction is case-insensitive."""
    path = write_tmp("bw: 80%")
    result = extract_weight(path)
    assert result == 80.0


def test_weight_multiple_lines():
    """Test extraction from multi-line file."""
    content = """
    Date: 2025-12-01
    Mouse ID: IP75
    BW: 82.1%
    Notes: Healthy
    """
    path = write_tmp(content)
    assert extract_weight(path) == 82.1


def test_missing_weight_raises():
    path = write_tmp("No weight here")
    try:
        extract_weight(path)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "BW" in str(e) or "weight" in str(e).lower()


def test_zero_weight():
    """Test that zero is a valid weight value."""
    path = write_tmp("BW: 0%")
    assert extract_weight(path) == 0.0


def test_large_weight_value():
    """Test extraction of weights greater than 100."""
    path = write_tmp("BW: 125.8%")
    assert extract_weight(path) == 125.8
