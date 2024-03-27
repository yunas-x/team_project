from pathlib import Path


def get_full_path(relative_path: str):
    """Resolves relative path and returns full path

    Args:
        relative_path (str): Relative path
    """
    
    return (Path(relative_path)).resolve()