import numpy as np
import pickle
from scipy.io import loadmat
from pathlib import Path

def load_single_values_file(file_path):
    if not file_path:
        raise ValueError("No values file selected")

    return _load_values(Path(file_path))

def load_daily_values_files(day_folders, filename):
    values = []
    for folder in day_folders:
        path = folder / filename
        if not path.exists():
            raise FileNotFoundError(
                f"Missing values file '{filename}' in folder: {folder.name}"
            )
        vals = _load_values(path)
        if len(vals) != 1:
            raise ValueError(
                f"Expected exactly one value in {path.name}, got {len(vals)}"
            )
        values.append(vals[0])
    return values

def _load_values(path: Path):
    suffix = path.suffix.lower()

    if suffix == ".npy":
        data = np.load(path, allow_pickle=True)
        return _to_list(data)

    elif suffix == ".pkl":
        with open(path, "rb") as f:
            data = pickle.load(f)
        return _to_list(data)

    elif suffix == ".mat":
        data = loadmat(path)
        return _extract_from_mat(data)

    else:
        raise ValueError(f"Unsupported file type: {suffix}")

def _to_list(data):
    if isinstance(data, (int, float)):
        return [data]

    if isinstance(data, (list, tuple)):
        return list(data)

    if hasattr(data, "shape") and data.shape == ():
        return [data.item()]

    if hasattr(data, "tolist"):
        out = data.tolist()
        if isinstance(out, (int, float)):
            return [out]
        return out

    raise ValueError("Loaded data is not numeric or array-like")


def _extract_from_mat(mat_dict):
    for key, val in mat_dict.items():
        if key.startswith("__"):
            continue
        if hasattr(val, "tolist"):
            flat = val.flatten().tolist()
            return flat
    raise ValueError("No numeric array found in .mat file")


def detect_outliers(x, y, z_thresh=3.0):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    zx = np.abs((x - x.mean()) / x.std())
    zy = np.abs((y - y.mean()) / y.std())

    inlier_mask = (zx < z_thresh) & (zy < z_thresh)
    outlier_mask = ~inlier_mask

    return inlier_mask, outlier_mask
