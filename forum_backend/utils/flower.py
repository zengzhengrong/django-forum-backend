from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.conf import settings
import logging

logger = logging.Logger('django')
def flower_view(request):
    '''passes the request back up to nginx for internal routing'''
    is_debug = getattr(settings,'DEBUG',False)
    if is_debug:
        return JsonResponse({'messgae':'You turn on DEBUG model'})
    response = HttpResponse()
    path = request.get_full_path()
    path = path.replace('flower', 'flower-internal', 1)
    response['X-Accel-Redirect'] = path
    return response