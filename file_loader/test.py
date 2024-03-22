from pathlib import Path
import requests
import time

path = str(Path.home() / 'Desktop' / 'itmo')

programs_response = requests.get('https://abitlk.itmo.ru/api/v1/programs/short?limit=300')
programs = programs_response.json()['result']['groups']

total = len(programs)
current = 1
skipped = 0

for program in programs:
    
    if program_slug := program['slug']:
        start_time = time.time()
        name = program['name'].replace('\\', '-').replace('/', '-').replace(':', '')
        degree = program['degree']
        file_name = str(Path(path) / ('%s (%s, %s).pdf' % (name, program['year'], degree)))
        
        print("Downloading: %s" % (file_name))
        
        response = requests.get('https://abit.itmo.ru/_next/data/PyEfeC8TAzZTl_mT-rjFm/ru/program/%s/%s.json' % (degree, program_slug))
        
        academic_plan = response.json()['pageProps']['apiProgram']['academic_plan']

        if academic_plan is not None:
            if not Path(file_name).exists():
                file_response = requests.get(academic_plan)
                with open(file_name, 'wb') as file:
                    file.write(file_response.content)
        else:
            print('SKIPPED')
            skipped += 1
        
    print("--- %s seconds (%s/%s) [Skipped: %s] ---" % (time.time() - start_time, current, total, skipped))
    current += 1

