from argparse import ArgumentParser, Namespace
from pathlib import Path
from loader import load
from plan_types import PlanType


def get_args() -> Namespace:
    arg_parser = ArgumentParser(prog='file_loader')
    
    default_path = Path.home() / 'Desktop' / 'pdfs'
    arg_parser.add_argument('-d', '--dest', default=str(default_path))
    arg_parser.add_argument('-m', '--mode', default=PlanType.HSE_BASIC_PLAN, choices=[tp.value for tp in PlanType])
    arg_parser.add_argument('--headless', default=False, action='store_true')
    
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    load(PlanType(args.mode), args.dest, args.headless)
    
    