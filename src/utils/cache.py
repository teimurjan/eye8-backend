from src.constants.status_codes import OK_CODE


def response_filter(res):
    return res[1] == OK_CODE
