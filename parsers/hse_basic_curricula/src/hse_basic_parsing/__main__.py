from pathlib import Path
import common
from file_loader.plan_types import PlanType
from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_args() -> Namespace:
    argparser = ArgumentParser(prog = 'file_loader')
    
    base_dir_path = Path(__file__).resolve().parents[4]
    default_files_path = base_dir_path.joinpath("curricula_examples").joinpath("working")
    
    argparser.add_argument('-s', '--src', default=str(default_files_path))
    argparser.add_argument('-d', '--dest', default=str(default_files_path))
    argparser.add_argument('-m', '--mode', default=PlanType.HSE_BASIC_PLAN, choices=[tp.value for tp in PlanType])
    argparser.add_argument('--headless', default=False, action='store_true')
    
    return argparser.parse_args()


if __name__ == '__main__':
    args = get_args()
    
    common.parse_hse_curricula(Path(args.src), Path(args.dest))
