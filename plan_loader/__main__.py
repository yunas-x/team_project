from argparse import ArgumentParser, Namespace
from pathlib import Path
from enums import PlanType
from loaders import get_loader
import logging
from config import DEFAULT_DOWNLOAD_PATH


def get_args() -> Namespace:
    arg_parser = ArgumentParser(prog='file_loader')
    
    arg_parser.add_argument('-d', '--dest', default=DEFAULT_DOWNLOAD_PATH)
    arg_parser.add_argument('-m', '--mode', default=PlanType.HSE_ANNUAL_PLAN, choices=[tp.value for tp in PlanType])
    
    return arg_parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s - %(levelname)s]: %(message)s')
    args = get_args()
    get_loader(args.mode).load(args.dest)