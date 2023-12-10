from argparse import ArgumentParser, Namespace
from pathlib import Path
from loader import load
from plan_types import PlanType


def get_args() -> Namespace:
    argparser = ArgumentParser(prog = 'file_loader')
    
    default_path = Path.home() / 'Desktop' / 'pdfs'
    argparser.add_argument('-d', '--dest', default=str(default_path))
    argparser.add_argument('-m', '--mode', default=PlanType.HSE_BASIC_PLAN, choices=[tp.value for tp in PlanType])
    argparser.add_argument('--headless', default=False, action='store_true')
    
    return argparser.parse_args()


if __name__ == '__main__':
    args = get_args()
    load(PlanType(args.mode), args.dest, args.headless)
    
    