from pathlib import Path
from common import parse_hse_basic_curricula


base_dir_path = Path(__file__).resolve().parent.parent.parent.parent.parent
default_files_path = base_dir_path.joinpath("curricula_examples").joinpath("basic")


if __name__ == '__main__':
    parse_hse_basic_curricula(default_files_path)
