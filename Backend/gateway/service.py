import requests
from Backend.translit import transliterate_payload
from Backend.crud_helper import log_request

def process_request(db, company, api, payload):
    transliterated = transliterate_payload(
        payload,
        api.fields_to_transliterate,
        api.normalization_enabled
    )

    response = requests.post(api.target_url, json=transliterated)

    log_request(
        db=db,
        company_id=company.id,
        api_endpoint_id=api.id,
        input_payload=payload,
        output_payload=transliterated,
        status_code=response.status_code
    )

    return response.json()

