from parsers.hse.annual.AnnualParser import AnnualParser
from parsers.hse.basic.BasicParser import BasicParser
from parsers.itmo.ItmoParser import ItmoParser
from parsers.parsing import parse, validate
import pandas as pd


if __name__ == "__main__":
    #pd.set_option('display.max_columns', None)
    parse('media/curricula_examples/itmo', 'media/output/itmo', ItmoParser(), 1)
    #parse('media/plans/itmo', 'media/output/itmo', ItmoParser(), 12)
    validate('media/plans/itmo', 'media/output/itmo', 'media/json_schemes/itmo_schema.json', 1)