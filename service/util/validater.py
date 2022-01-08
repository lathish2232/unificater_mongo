from service.util.json_utils import is_not_null_or_empty


def do_instance_validation(req_body):
    val_status = None
    if is_not_null_or_empty(req_body):
        msg = []
        params = req_body.get('connectionParameters')
        for param in params:
            if param.get('isRequired'):
                if not is_not_null_or_empty(param.get('userValue')):
                    msg.append(f'{param.get("displayName")} should not be Null or Empty')
        if msg:
            val_status = msg
    else:
        val_status = "Payload should not be Null or Empty"

    return val_status
