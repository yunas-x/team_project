import csv
from pathlib import Path

def iterfile(file: Path):
    with open(file, mode="rb") as f:
        yield from f
        
def write_report(program_id: int) -> Path:
    """Creates report file of programm learning plan if does not exist

    Args:
        program_id (int): program_id for which report should be assembled

    Returns:
        Path: path to report created
    """
    
    file = Path(f'report_{program_id}.csv')
    
    if not file.is_file():
        with open(file, 'w+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
            
    return file