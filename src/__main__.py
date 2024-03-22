from parsers.itmo.ItmoParser import ItmoParser
from parsers import parse, validate
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(name)s - %(levelname)s]: %(message)s')
    parse('media/plans/itmo', 'media/output/itmo', ItmoParser(), 1)
    validate('media/plans/itmo', 'media/output/itmo', 'media/json_schemes/itmo_schema.json', 1)