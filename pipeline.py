import openpyxl
from pathlib import Path
from itertools import tee, zip_longest


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def open_base(db_path):
    # file = Path(db_path, name)
    # print(f'file {file}')
    wb_obj = openpyxl.load_workbook(db_path)
    sheet_data = wb_obj.active
    return sheet_data


def normalize_data(fio_data):
    fio_items = fio_data.pop(1).split(' ')
    fio_data += [i for i in fio_items if len(i) != 0]
    return fio_data


def parser(sheet):
    person_data = []
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if i == 0:
            continue
        raw_data = [i for i in row]
        person_data.append(normalize_data(raw_data))
    return person_data


def person_to_db_payload_prepare(person_data):
    payload_list = []
    key_list = ['position', 'money', 'last_name', 'first_name', 'middle_name']
    for i in range(len(person_data)):
        payload_list.append(dict(zip(key_list, person_data[i])))
    return payload_list


def person_to_vacancy_payload_prepare(person_data):
    payload_list = []

    def get_payload(comment, status=44, id_file=0, rejection_reason=0, vacancy=9):
        return {
            "vacancy": vacancy,
            "status": status,
            "comment": comment,
            "files": [
                {
                    "id": id_file
                }
            ],
            "rejection_reason": rejection_reason
        }

    for vac_type_, status_, comment_ in grouper(person_data, 3):
        payload = get_payload(vacancy=vac_type_, comment=status_ + ' - ' + comment_)
        payload_list.append(payload)
    return payload_list


def separator(separate_data):
    to_vacancy = []
    vacancy_type = (
        ('Frontend-разработчик', 9),
        ('Менеджер по продажам', 2)
    )
    for i in separate_data:
        if i[0] == vacancy_type[0][0]:
            to_vacancy.append(vacancy_type[0][1])
            to_vacancy.append(i.pop(2))
            to_vacancy.append(i.pop(2))
        else:
            to_vacancy.append(vacancy_type[1][1])
            to_vacancy.append(i.pop(2))
            to_vacancy.append(i.pop(2))
    return separate_data, to_vacancy
