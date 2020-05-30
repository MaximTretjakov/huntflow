from cli import parser_init
from resume_file import get_resume_file, path_to
from transport import upload_file, get_ids, candidate_to_db, candidate_to_vacancy, base_url
from pipeline import open_base, parser, separator, person_to_db_payload_prepare, person_to_vacancy_payload_prepare

if __name__ == '__main__':
    data = 0
    args = parser_init()
    if args.token:
        try:
            data = open_base(args.base_path)
        except FileNotFoundError as er:
            print(f'Error! {er.args}')

        parsed_data = parser(data)
        person_to_db, person_to_vacancy = separator(parsed_data)
        payload_to_db = person_to_db_payload_prepare(person_to_db)
        payload_to_vacancy = person_to_vacancy_payload_prepare(person_to_vacancy)

        for payload_db, payload_vacancy in zip(payload_to_db, payload_to_vacancy):
            resume_file = get_resume_file(payload_db['last_name'], path_to)
            upload_res = upload_file(resume_file, base_url, args.token).json()
            photo_id, file_id = get_ids(upload_res)
            candidate_to_db_res = candidate_to_db(base_url, photo_id, file_id, args.token, payload_db).json()
            candidate_to_vacancy_res = candidate_to_vacancy(base_url, file_id, candidate_to_db_res['id'], args.token, payload_vacancy).json()
    else:
        print('Use -h/--help to get help')
