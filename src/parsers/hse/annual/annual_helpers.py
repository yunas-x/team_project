import re


def get_programme_name(text_list: list[str]) -> str:
    programme_name = ''

    for i in range(0, len(text_list)):
        row = text_list[i]

        if 'программа' in row and '"' in row:
            start_ind = row.index('"') + 1
            potential_name = row[start_ind:]

            # if both quotes are in the row then programme name should be between them
            if '"' in potential_name:
                end_ind = potential_name.index('"')

                programme_name = potential_name[:end_ind]
                break

            # if just one quote is in the row then find next row with end quote
            else:
                if '  ' in potential_name:
                    gap_ind = potential_name.index('  ')

                    programme_name = potential_name[:gap_ind]

                for j in range(i + 1, len(text_list)):
                    row = text_list[j]

                    if '"' in row:
                        quote_ind = row.index('"')

                        programme_name += ' ' + row[:quote_ind]
                        break

                    elif '  ' in row:
                        gap_ind = row.index('  ')

                        programme_name += ' ' + row[:gap_ind]
                break

    return programme_name


def get_year_and_enrolled_in(text_list) -> (int, int):
    for row in text_list:
        match = re.search(r'\d ?курс, ?\d{4}/\d{4} ?учебный ?год', row)

        if match:
            res_string = match.group(0)
            slash_ind = res_string.index('/')

            year = int(res_string[0])
            enrolled_in = int(res_string[slash_ind - 4:slash_ind]) + 1 - year
            break

    return year, enrolled_in


def get_hours(val) -> int:
    if type(val) is str:
        match = re.search(r'\d+', val)
        if match:
            return int(match.group(0))
        else:
            return 0
    else:
        return int(val)