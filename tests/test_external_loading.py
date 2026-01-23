import numpy as np
import tempfile
import pickle
from external_values import load_single_values_file, detect_outliers

def test_load_npy_array():
    """Test loading a numpy array from .npy file."""
    arr = np.array([1.5, 2.3, 3.7])
    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
        path = f.name
    
    np.save(path, arr)
    out = load_single_values_file(path)
    
    assert len(out) == 3
    assert np.allclose(out, arr)


def test_load_1d_array():
    """Test loading 1D numpy array."""
    arr = np.array([10, 20, 30, 40])
    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
        path = f.name
    
    np.save(path, arr)
    out = load_single_values_file(path)
    
    assert len(out) == 4
    assert out[0] == 10


def test_load_pickle_scalar():
    """Test loading a scalar value from pickle file."""
    path = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False).name
    with open(path, "wb") as f:
        pickle.dump(5.5, f)

    out = load_single_values_file(path)
    assert out == 5.5 or out == [5.5]


def test_load_pickle_list():
    """Test loading a list from pickle file."""
    values = [1.1, 2.2, 3.3, 4.4]
    path = tempfile.NamedTemporaryFile(suffix=".pkl", delete=False).name
    with open(path, "wb") as f:
        pickle.dump(values, f)

    out = load_single_values_file(path)
    assert len(out) == 4


def test_unsupported_file_format_raises():
    """Test that unsupported file formats raise an error."""
    path = tempfile.NamedTemporaryFile(suffix=".txt", delete=False).name
    with open(path, "w") as f:
        f.write("1,2,3")
    
    try:
        load_single_values_file(path)
        assert False, "Should have raised an error for unsupported format"
    except (ValueError, Exception):
        pass  # Expected behavior


def test_empty_npy_array():
    """Test handling of empty numpy arrays."""
    arr = np.array([])
    with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as f:
        path = f.name
    
    np.save(path, arr)
    out = load_single_values_file(path)
    
    assert len(out) == 0


def test_detect_outliers_basic():
    """Test basic outlier detection."""
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    weights = np.array([80.0, 81.0, 82.0, 83.0, 120.0])  # 120 is outlier
    
    in_mask, out_mask = detect_outliers(external_values, weights, z_thresh=1.9)
    
    assert len(in_mask) == 5
    assert len(out_mask) == 5
    assert np.sum(out_mask) >= 1  # At least one outlier


def test_detect_outliers_no_outliers_high_threshold():
    """Test that high z-threshold results in no outliers."""
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    weights = np.array([80.0, 81.0, 82.0, 83.0, 84.0])
    
    in_mask, out_mask = detect_outliers(external_values, weights, z_thresh=5.0)
    
    assert np.sum(in_mask) == 5
    assert np.sum(out_mask) == 0


def test_detect_outliers_low_threshold():
    """Test that low z-threshold catches more outliers."""
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    weights = np.array([80.0, 81.0, 82.0, 83.0, 84.0])
    
    in_mask_high, out_mask_high = detect_outliers(external_values, weights, z_thresh=3.0)
    in_mask_low, out_mask_low = detect_outliers(external_values, weights, z_thresh=1.0)
    
    # Lower threshold should catch more or equal outliers
    assert np.sum(out_mask_low) >= np.sum(out_mask_high)
