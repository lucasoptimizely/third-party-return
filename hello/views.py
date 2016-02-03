from django import http
from django.http import HttpResponse
import json
import random
import string
from datetime import datetime

domain = '.third-party-return.appspot.com'

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        # N = 10
        # expires = datetime.now().replace(year=datetime.now().year + 10)
        # print request.COOKIES
        # request.COOKIES['otid'] = (request.COOKIES['otid'] if 'otid' in request.COOKIES else ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N)))
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            # objects.set_cookie('otid', request.COOKIES['otid'], domain=domain, expires=expires)
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                response = HttpResponse(data, "text/javascript")
                # response.set_cookie('otid', request.COOKIES['otid'], domain=domain, expires=expires)
                return response
        except:
            data = json.dumps(str(objects))
        response = HttpResponse(data, "application/json")
        # response.set_cookie('otid', request.COOKIES['otid'], domain=domain, expires=expires)
        return response
    return decorator

def pixel(func):
    response = HttpResponse({}, "image/png")
    N = 10
    expires = datetime.now().replace(year=datetime.now().year + 10)
    ran = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
    response.set_cookie('otid', ran, domain=domain, expires=expires)
    return response
    

@json_response
def home(request):
    return request.COOKIES
