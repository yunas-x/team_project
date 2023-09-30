from pathlib import Path
from converters import convert_pdf_to_data_frame


if __name__ == '__main__':
    base_dir_path = Path(__file__).resolve().parent.parent.parent
    basic_example_files_path = base_dir_path.joinpath("curricula_examples").joinpath("basic")

    df = convert_pdf_to_data_frame(basic_example_files_path.joinpath("1.pdf"))

    print(df.iloc[0, 0])
