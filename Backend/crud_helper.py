from Backend.models import RequestLog

def log_request(
    db,
    company_id,
    api_endpoint_id,
    input_payload,
    output_payload,
    status_code,
):
    log = RequestLog(
        company_id=company_id,
        api_endpoint_id=api_endpoint_id,
        input_payload=input_payload,
        output_payload=output_payload,
        status_code=status_code,
    )
    db.add(log)
    db.commit()
