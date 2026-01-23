import tempfile
from pathlib import Path
import numpy as np
import tkinter as tk
from unittest.mock import patch, MagicMock
from scipy.io import loadmat
import pytest

# Import after path is set up in conftest
from gui import MouseWeightGUI


class TestSaveWeights:
    """Test suite for weight saving functionality."""
    
    @pytest.fixture
    def gui_app(self):
        """Create a test GUI app."""
        root = tk.Tk()
        app = MouseWeightGUI(root)
        yield app
        root.destroy()
    
    @pytest.fixture
    def sample_days(self):
        """Create sample day folders with date names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            days = []
            for date in ["20250101", "20250102", "20250103"]:
                day_folder = tmpdir / date
                day_folder.mkdir()
                days.append(day_folder)
            yield days
    
    @pytest.fixture
    def sample_weights(self):
        """Sample weight data."""
        return np.array([80.0, 81.5, 82.0])
    
    def test_save_mat_format(self, gui_app, sample_days, sample_weights):
        """Test saving weights in MATLAB format."""
        gui_app.selected_days = sample_days
        gui_app.save_format.set("mat")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.mat"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(sample_weights, sample_days)
            
            # Verify file was created and contains correct data
            assert output_file.exists(), "MAT file was not created"
            
            loaded_data = loadmat(str(output_file))
            assert "weights" in loaded_data
            assert "dates" in loaded_data
            assert np.allclose(loaded_data["weights"].flatten(), sample_weights)
            # MAT files may wrap dates in extra dimensions, so flatten and check length
            dates_array = np.asarray(loaded_data["dates"]).flatten()
            assert len(dates_array) == 3
    
    def test_save_npy_format(self, gui_app, sample_days, sample_weights):
        """Test saving weights in NumPy format."""
        gui_app.selected_days = sample_days
        gui_app.save_format.set("npy")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.npy"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(sample_weights, sample_days)
            
            # Verify file was created and contains correct data
            assert output_file.exists(), "NPY file was not created"
            
            loaded_data = np.load(str(output_file), allow_pickle=True).item()
            assert "weights" in loaded_data
            assert "dates" in loaded_data
            assert np.allclose(loaded_data["weights"], sample_weights)
            assert len(loaded_data["dates"]) == 3
    
    def test_save_cancelled(self, gui_app):
        """Test when user cancels the file save dialog."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_days = [Path(tmpdir) / "20250101"]
            sample_days[0].mkdir()
            sample_weights = np.array([80.0])
            
            gui_app.save_format.set("mat")
            
            # filedialog returns empty string when cancelled
            with patch('gui.filedialog.asksaveasfilename', return_value=""):
                with patch('gui.messagebox.showinfo') as mock_info:
                    gui_app.save_extracted_weights(sample_weights, sample_days)
            
            # Should not show success message when cancelled
            mock_info.assert_not_called()
    
    def test_save_selected_weights_no_days(self, gui_app):
        """Test save_selected_weights when no days are selected."""
        gui_app.selected_days = []
        
        with patch('gui.messagebox.showerror') as mock_error:
            gui_app.save_selected_weights()
        
        mock_error.assert_called_once()
        assert "Please load and select days first" in str(mock_error.call_args)
    
    def test_save_selected_weights_with_days(self, gui_app, sample_days, sample_weights):
        """Test save_selected_weights with days selected."""
        gui_app.selected_days = sample_days
        gui_app.save_format.set("mat")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.mat"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    with patch('gui.load_weights_for_selected_days', return_value=sample_weights):
                        gui_app.save_selected_weights()
            
            # Should have saved the file
            assert output_file.exists()
    
    def test_save_with_different_weight_values(self, gui_app, sample_days):
        """Test saving with various weight values."""
        weights = np.array([75.5, 80.0, 85.5, 90.0, 78.3])
        gui_app.selected_days = sample_days + [Path(tempfile.mkdtemp()) / "20250104", 
                                                 Path(tempfile.mkdtemp()) / "20250105"]
        gui_app.save_format.set("mat")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.mat"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(weights, gui_app.selected_days)
            
            loaded_data = loadmat(str(output_file))
            assert np.allclose(loaded_data["weights"].flatten(), weights)
    
    def test_save_empty_weights(self, gui_app, sample_days):
        """Test saving empty weight array."""
        weights = np.array([])
        gui_app.save_format.set("mat")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.mat"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(weights, [])
            
            # Should still create file with empty data
            assert output_file.exists()
    
    def test_save_with_single_weight(self, gui_app):
        """Test saving with a single weight value."""
        day = Path(tempfile.mkdtemp()) / "20250101"
        day.mkdir(exist_ok=True)
        gui_app.selected_days = [day]
        gui_app.save_format.set("npy")
        weights = np.array([82.0])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "weights.npy"
            
            with patch('gui.filedialog.asksaveasfilename', return_value=str(output_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(weights, gui_app.selected_days)
            
            loaded_data = np.load(str(output_file), allow_pickle=True).item()
            assert loaded_data["weights"][0] == 82.0
    
    def test_mat_and_npy_consistency(self, gui_app, sample_days, sample_weights):
        """Test that MAT and NPY formats store the same data."""
        gui_app.selected_days = sample_days
        
        with tempfile.TemporaryDirectory() as tmpdir:
            mat_file = Path(tmpdir) / "weights.mat"
            npy_file = Path(tmpdir) / "weights.npy"
            
            # Save as MAT
            gui_app.save_format.set("mat")
            with patch('gui.filedialog.asksaveasfilename', return_value=str(mat_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(sample_weights, sample_days)
            
            # Save as NPY
            gui_app.save_format.set("npy")
            with patch('gui.filedialog.asksaveasfilename', return_value=str(npy_file)):
                with patch('gui.messagebox.showinfo'):
                    gui_app.save_extracted_weights(sample_weights, sample_days)
            
            # Load both and compare
            mat_data = loadmat(str(mat_file))
            npy_data = np.load(str(npy_file), allow_pickle=True).item()
            
            assert np.allclose(mat_data["weights"].flatten(), npy_data["weights"])
    
    def test_save_error_handling(self, gui_app, sample_days, sample_weights):
        """Test error handling during save."""
        gui_app.selected_days = sample_days
        gui_app.save_format.set("mat")
        
        # Mock savemat to raise an exception
        with patch('gui.savemat', side_effect=Exception("Disk full")):
            with patch('gui.filedialog.asksaveasfilename', return_value="/tmp/weights.mat"):
                with patch('gui.messagebox.showerror') as mock_error:
                    gui_app.save_extracted_weights(sample_weights, sample_days)
        
        mock_error.assert_called_once()
        assert "Save Error" in str(mock_error.call_args)
        assert "Disk full" in str(mock_error.call_args)


class TestSaveIntegration:
    """Integration tests for save functionality with actual file I/O."""
    
    def test_save_and_load_workflow(self):
        """Test complete workflow: save weights and load them back."""
        weights = np.array([80.0, 81.5, 82.0])
        dates = ["20250101", "20250102", "20250103"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_weights.mat"
            
            # Save
            data = {"weights": weights, "dates": np.array(dates, dtype=object)}
            from scipy.io import savemat
            savemat(str(output_file), data)
            
            # Load and verify
            loaded = loadmat(str(output_file))
            assert np.allclose(loaded["weights"].flatten(), weights)
            assert list(loaded["dates"].flatten()) == dates
    
    def test_npy_save_and_load_workflow(self):
        """Test complete workflow for NPY format."""
        weights = np.array([80.0, 81.5, 82.0])
        dates = ["20250101", "20250102", "20250103"]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_weights.npy"
            
            # Save
            data = {"weights": weights, "dates": np.array(dates, dtype=object)}
            np.save(str(output_file), data)
            
            # Load and verify
            loaded = np.load(str(output_file), allow_pickle=True).item()
            assert np.allclose(loaded["weights"], weights)
            assert len(loaded["dates"]) == 3
