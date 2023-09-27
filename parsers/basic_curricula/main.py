import pandas as pd


def parse(excel_file_name):
    df = pd.read_excel(excel_file_name, sheet_name='Sheet1', skiprows=2)

    ep = df.iloc[0, 2]
    educational_program = ep.replace('"', '').replace('Образовательная программа ', '')

    sd = df.iloc[1, 2]
    study_direction = sd.replace('Направление ', '')

    sm = df.iloc[2, 2]
    study_mode = consts.PART_TIME
    if 'Очная' in sm:
        study_mode = consts.FULL_TIME
    elif 'очно' in sm.lower():
        study_mode = consts.FULL_PART_TIME

    ct = df.iloc[3, 2]
    competition_type = consts.TARGETED
    if 'бюджетное' in ct:
        competition_type = consts.BUDGET
    elif 'по договору' in ct:
        competition_type = consts.COMMERCIAL

    dt = df.iloc[6, 2]
    dt = dt.replace('Время формирования: ', '')
    date_time = utils.parse_date_string(dt)

    subject_names = self.__get_subject_names(df)

    applicant_list = []
    for i in range(7, df.shape[0]):
        insurance_number = get_insurance_number(str(df.iloc[i, 2]))
        if insurance_number == BAD_RESULT:
            continue

        agreement = self.__convert_yes_no_to_bool(df.iloc[i, 4])
        if agreement == BAD_RESULT:
            continue

        brought_original = self.__convert_yes_no_to_bool(df.iloc[i, 6])
        if brought_original == BAD_RESULT:
            continue

        subject_scores = self.__get_subject_scores(df, i)
        if subject_scores == BAD_RESULT:
            continue

        index_after_subjects = df.shape[1] - 5

        es = df.iloc[i, index_after_subjects]
        # noinspection PyBroadException
        try:
            extra_score = int(es)
        except Exception:
            extra_score = 0

        special_right = self.__convert_yes_no_to_bool(df.iloc[i, index_after_subjects + 4])
        if special_right == BAD_RESULT:
            continue

        # noinspection PyBroadException
        try:
            applicant_list.append(
                ApplicationEntry(int(df.iloc[i, 0]), insurance_number, agreement, brought_original,
                                 subject_scores, extra_score, special_right))
        except Exception:
            continue

    application_info = ApplicationInfo("НИУ ВШЭ", study_direction, educational_program, 4, 5, 6, study_mode,
                                       competition_type, self._url, date_time, subject_names)

    return [application_info, applicant_list]


if __name__ == '__main__':
    print_hi('PyCharm')
