import requests
import json
from requests_toolbelt.multipart import encoder

# base url
base_url = 'https://dev-100-api.huntflow.ru/'


def set_post_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": "App/1.0 (incaseoffire@example.com)",
        "Content-Type": "application/json"
    }


def get_ids(data_set):
    photo_ = data_set['photo']['id']
    file_ = data_set['id']
    return photo_, file_


def get_externals(f_id):
    return {
        "externals": [
            {
                "data": {
                    "body": "Тестовый текст резюме"
                },
                "auth_type": "NATIVE",
                "files": [
                    {
                        "id": f_id
                    }
                ]
            }
        ]
    }


def get_vacancy_data(id_file, comment, vacancy_id=9, reason=None, status=44):
    return {
        "vacancy": vacancy_id,
        "status": status,
        "comment": comment,
        "files": [
            {
                "id": id_file
            }
        ],
        "rejection_reason": reason
    }


def upload_file(file_name, base, token):
    session = requests.Session()
    with open(file_name, 'rb') as f:
        form = encoder.MultipartEncoder({
            'file': (file_name, f, 'application/octet-stream')
        })
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'App/1.0 (incaseoffire@example.com)',
            'Content-Type': form.content_type,
            'X-File-Parse': 'true',
            'Prefer': 'respond-async'
        }
        resp = session.post(base + 'account/6/upload', headers=headers, data=form)
    session.close()
    assert resp.status_code == requests.codes.ok, f'error : {resp.text}'
    return resp


def candidate_to_db(base, p_id, f_id, token, payload):
    payload['photo'] = p_id
    externals = get_externals(f_id)
    candidate_payload = {**payload, **externals}
    resp = requests.post(base + 'account/6/applicants', headers=set_post_headers(token), json=candidate_payload)
    assert resp.status_code == requests.codes.ok, f'error : {resp.text}'
    return resp


def candidate_to_vacancy(base, f_id, candidate_id, token, payload):
    payload['files'][0]['id'] = f_id
    resp = requests.post(base + f'account/6/applicants/{candidate_id}/vacancy', headers=set_post_headers(token), json=payload)
    assert resp.status_code == requests.codes.ok, f'error : {resp.text}'
    return resp
