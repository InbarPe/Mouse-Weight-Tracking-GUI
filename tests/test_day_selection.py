import tempfile
from pathlib import Path
from data_loader import find_day_folders, find_expdetails_file

def test_find_valid_day_folders():
    """Test finding valid date-formatted folders."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)
        
        # Create valid day folders
        (base / "20251201").mkdir()
        (base / "20251202").mkdir()
        (base / "20251203").mkdir()
        
        # Create an invalid folder (should be ignored)
        (base / "invalid_folder").mkdir()
        
        folders = find_day_folders(str(base))
        
        assert len(folders) == 3
        assert all(len(f.name) == 8 for f in folders)


def test_no_day_folders_raises():
    """Test that FileNotFoundError is raised when no valid day folders exist."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir)
        
        # Create only invalid folders
        (base / "invalid_folder").mkdir()
        
        try:
            find_day_folders(str(base))
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError as e:
            assert "No valid day folders found" in str(e)


def test_nonexistent_base_path_raises():
    """Test that FileNotFoundError is raised for nonexistent base path."""
    try:
        find_day_folders("/nonexistent/path/12345")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert "Base folder does not exist" in str(e)


def test_find_expdetails_file():
    """Test finding ExpDetails file in a day folder."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        day_folder = Path(tmp_dir)
        
        # Create an ExpDetails file
        exp_file = day_folder / "IP75_20251201_ExpDetails.txt"
        exp_file.write_text("BW: 83% 21.2g")
        
        found_file = find_expdetails_file(day_folder)
        assert found_file == exp_file


def test_missing_expdetails_file_raises():
    """Test that FileNotFoundError is raised when ExpDetails file is missing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        day_folder = Path(tmp_dir)
        
        # Create a non-ExpDetails file
        (day_folder / "other_file.txt").write_text("content")
        
        try:
            find_expdetails_file(day_folder)
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError as e:
            assert "Missing ExpDetails file" in str(e)
