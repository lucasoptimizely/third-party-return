from django.http import HttpResponse
import json
import random
import string
from datetime import datetime

DOMAIN = '.third-party-return.appspot.com'
COOKIENAME = 'otid'

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                response = HttpResponse(data, "text/javascript")
                return response
        except:
            data = json.dumps(str(objects))
        response = HttpResponse(data, "application/json")
        return response
    return decorator

def pixel(request):
    response = HttpResponse({}, "image/png")
    add_id_if_not_set(request, response)
    return response
    
def add_id_if_not_set(request, response):
    if COOKIENAME not in request.COOKIES:
        N = 10
        expires = datetime.now().replace(year=datetime.now().year + 10)
        ran = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
        response.set_cookie(COOKIENAME, ran, domain=DOMAIN, expires=expires)
    return response

@json_response
def home(request):
    return request.COOKIES
