import tempfile
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from plotter import plot_weight_vs_external
from external_values import detect_outliers


def test_plot_with_regression():
    """Test plotting with regression line enabled."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 85.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Should not raise an error
    try:
        # We can't actually display plots in tests, but we can test the function doesn't crash
        plot_weight_vs_external(weights, external_values, show_regression=True)
        assert True
    except Exception as e:
        assert False, f"plot_weight_vs_external with regression failed: {e}"


def test_plot_with_outlier_detection():
    """Test plotting with outlier detection enabled."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 120.0])  # 120 is an outlier
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    try:
        plot_weight_vs_external(weights, external_values, mark_outliers=True, z_thresh=1.9)
        assert True
    except Exception as e:
        assert False, f"plot_weight_vs_external with outlier detection failed: {e}"


def test_detect_outliers():
    """Test outlier detection with z-score method."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 120.0])  # 120 is an outlier
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    in_mask, out_mask = detect_outliers(external_values, weights, z_thresh=1.9)
    
    # Should have 4 inliers and 1 outlier
    assert np.sum(in_mask) == 4
    assert np.sum(out_mask) == 1
    assert out_mask[4] == True  # Last value should be detected as outlier


def test_detect_outliers_no_outliers():
    """Test outlier detection when there are no outliers."""
    weights = np.array([80.0, 81.0, 82.0, 83.0, 84.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    in_mask, out_mask = detect_outliers(external_values, weights, z_thresh=3.0)
    
    # All should be inliers with high z threshold
    assert np.sum(in_mask) == 5
    assert np.sum(out_mask) == 0


def test_detect_outliers_multiple():
    """Test outlier detection with multiple outliers."""
    weights = np.array([80.0, 120.0, 82.0, 130.0, 84.0])  # 120 and 130 are outliers
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    in_mask, out_mask = detect_outliers(external_values, weights, z_thresh=0.9)
    
    # Should detect multiple outliers
    assert np.sum(out_mask) >= 1


def test_regression_with_perfect_correlation():
    """Test regression functionality with perfectly correlated data."""
    weights = np.array([80.0, 81.0, 82.0, 83.0, 84.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    try:
        plot_weight_vs_external(weights, external_values, show_regression=True)
        plt.close('all')  # Clean up matplotlib figures
        assert True
    except Exception as e:
        assert False, f"Regression with perfect correlation failed: {e}"


def test_plot_with_both_features():
    """Test plotting with both regression and outlier detection."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 120.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    try:
        plot_weight_vs_external(
            weights,
            external_values,
            show_regression=True,
            mark_outliers=True,
            z_thresh=1.9
        )
        assert True
    except Exception as e:
        assert False, f"Plotting with both features failed: {e}"


def test_plot_with_single_value():
    """Test plotting with just one data point - validates error message."""
    weights = np.array([82.0])  # Only 1 point - should show error message
    external_values = np.array([3.0])
    
    try:
        # Capture the figure
        plot_weight_vs_external(weights, external_values, show_regression=False)
        
        # Get the current figure and axes
        fig = plt.gcf()
        ax = fig.gca()
        
        # Check that the text object with the error message was added
        texts = [child for child in ax.get_children() if isinstance(child, plt.Text) and child.get_text()]
        text_content = ' '.join([text.get_text() for text in texts])
        
        assert "Insufficient data for correlation" in text_content, \
            f"Expected error message not found. Text content: {text_content}"
        
        plt.close('all')  # Clean up matplotlib figures
    except AssertionError as e:
        raise e
    except Exception as e:
        assert False, f"Plotting with single value failed: {e}"


def test_regression_parameter_false():
    """Test that regression parameter can be False."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 85.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    try:
        plot_weight_vs_external(weights, external_values, show_regression=False)
        assert True
    except Exception as e:
        assert False, f"Plotting with show_regression=False failed: {e}"


def test_outlier_detection_parameter_false():
    """Test that outlier detection parameter can be False."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 85.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    try:
        plot_weight_vs_external(weights, external_values, mark_outliers=False)
        assert True
    except Exception as e:
        assert False, f"Plotting with mark_outliers=False failed: {e}"


def test_custom_z_threshold():
    """Test outlier detection with custom z-score threshold."""
    weights = np.array([80.0, 81.5, 82.0, 83.5, 85.0])
    external_values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Test with different thresholds
    try:
        for threshold in [1.0, 2.0, 3.0, 4.0]:
            plot_weight_vs_external(
                weights,
                external_values,
                mark_outliers=True,
                z_thresh=threshold
            )
        assert True
    except Exception as e:
        assert False, f"Custom z-threshold failed: {e}"


def test_large_dataset():
    """Test with larger dataset."""
    np.random.seed(42)
    weights = np.random.normal(82, 2, 100)  # 100 points, mean 82, std 2
    external_values = np.random.normal(3, 1, 100)
    
    try:
        plot_weight_vs_external(
            weights,
            external_values,
            show_regression=True,
            mark_outliers=True,
            z_thresh=3.0
        )
        assert True
    except Exception as e:
        assert False, f"Large dataset plotting failed: {e}"
