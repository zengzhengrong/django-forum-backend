def jwt_encode(user):
    try:
        from rest_framework_jwt.settings import api_settings
    except ImportError:
        raise ImportError("djangorestframework_jwt needs to be installed")

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def jwt_decode(token):
    try:
        from rest_framework_jwt.settings import api_settings
        from rest_framework_jwt.serializers import jwt
    except ImportError:
        raise ImportError("djangorestframework_jwt needs to be installed")
    
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
    # decode jwt 
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = 'token expired'
        return (msg,403)
    except jwt.DecodeError:
        msg = 'token decode error'
        return (msg,403)
    
    username = jwt_get_username_from_payload(payload) # return username
    return (username,200)