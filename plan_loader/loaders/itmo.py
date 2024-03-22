from pathlib import Path
import requests
import time
from loaders.base import BaseLoader
import logging
from config import ITMO_PLANS_URL, ITMO_PROGRAM_URL


class ItmoLoader(BaseLoader):
    """Class for loading study plans for ITMO"""
    
    def load(self, path: str) -> None:
        # Get list of all programs
        programs_response = requests.get(ITMO_PLANS_URL)
        programs = programs_response.json()['result']['groups']

        total = len(programs)
        current = 1
        skipped = 0
        new = 0

        for program in programs:
            # Slug is used to reference programs when requesting them by API
            # It is None for postgraduate programs
            if program_slug := program['slug']:
                start_time = time.perf_counter()
                # Replacing chars that are prohibited in filenames
                name = program['name'].replace('\\', '-').replace('/', '-').replace(':', '')
                degree = program['degree']
                file_name = str(Path(path) / ('%s (%s, %s).pdf' % (name, program['year'], degree)))
                
                logging.info('')
                logging.info('--- %s/%s ---' % (current, total))
                logging.info("Checking: %s" % (name))
                
                # Get info about a specific program
                response = requests.get(ITMO_PROGRAM_URL % (degree, program_slug))
                # Get link to download academic_plan
                academic_plan = response.json()['pageProps']['apiProgram']['academic_plan']
                # Check if file is already downloaded and download if not
                if academic_plan is not None:
                    if not Path(file_name).exists():
                        logging.info('NEW - Started downloading')
                        file_response = requests.get(academic_plan)
                        with open(file_name, 'wb') as file:
                            file.write(file_response.content)
                        logging.info('Finished')
                    else:
                        logging.info('EXISTS')
                        new += 1
                else:
                    logging.info('SKIPPED - Postgraduate')
                    skipped += 1
                
            logging.info("--- %s seconds [Skipped: %s, New: %s] ---" % (time.perf_counter() - start_time, skipped, new))
            current += 1

