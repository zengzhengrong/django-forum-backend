from django.conf import settings
from ipware import get_client_ip


def get_ip_address_from_request(request):
    """
    返回request里的IP地址
    """
    ip, is_routable = get_client_ip(request)
    if settings.DEBUG:
        return ip
    else:
        if ip is not None and is_routable:
            return ip
    return None