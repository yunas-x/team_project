from pathlib import Path
from parsers.hse.basic.BasicParser import BasicParser
from parsers.hse.annual.AnnualParser import AnnualParser
from tests.parsers.hse.basic.tests import start_stress_testing


def __start_hse_basic_parser_testing():
    start_stress_testing(str(Path(__file__).parents[2] / "curricula_examples" / "hse" / "basic"),
                         str(Path(__file__).parents[1] / "parsers" / "hse" / "temp_files"),
                         str(Path(__file__).parents[1] / "parsers" / "hse" / "schemes" / "base_hse_schema.json"),
                         BasicParser())
    

def start_hse_annual_parser_testing():
    start_stress_testing(str(Path(__file__).parents[2] / "curricula_examples" / "hse" / "annual"),
                         str(Path(__file__).parents[1] / "parsers" / "hse" / "temp_files"),
                         str(Path(__file__).parents[1] / "parsers" / "hse" / "schemes" / "annual_hse_schema.json"),
                         AnnualParser())


if __name__ == "__main__":
    start_hse_annual_parser_testing()
    #__start_hse_basic_parser_testing()
    #parser = BasicParser()
    #print(parser.parse(r"C:\Users\shisha\Desktop\pdfs\2017 Б 01.03.01 Мат 2017 очная Совместный бакалавриат НИУ ВШЭ и ЦПМ.pdf"))

