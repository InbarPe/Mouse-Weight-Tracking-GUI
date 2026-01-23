from pathlib import Path
import re

DATE_PATTERN = re.compile(r"\d{8}")

def find_day_folders(base_path):
    base = Path(base_path)
    if not base.exists():
        raise FileNotFoundError("Base folder does not exist")

    folders = [
        p for p in base.iterdir()
        if p.is_dir() and DATE_PATTERN.fullmatch(p.name)
    ]

    if not folders:
        raise FileNotFoundError("No valid day folders found")

    return sorted(folders)

def find_expdetails_file(day_folder):
    files = list(day_folder.glob("*ExpDetails*.txt"))
    if not files:
        raise FileNotFoundError(
            f"Missing ExpDetails file in folder: {day_folder.name}"
        )
    return files[0]

def load_weights_for_selected_days(selected_days):
    """Load weights from all selected days.
    
    Args:
        selected_days: List of Path objects representing day folders
        
    Returns:
        List of weight values extracted from ExpDetails files
    """
    from weight_parser import extract_weight
    
    weights = []
    for day in selected_days:
        txt_file = find_expdetails_file(day)
        weights.append(extract_weight(txt_file))
    return weights
