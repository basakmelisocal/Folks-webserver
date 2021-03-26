from flask import jsonify


def base_resp(response, code, error_message=None):
    result = dict()
    result.update(response)
    result.update({"code": code})
    if error_message:
        result.update({"debug": error_message})
    return jsonify(result)
