import os

from django.contrib.gis.geoip2 import GeoIP2
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        g = GeoIP2
        print(g('127.0.0.1'))
        # print(request.session.get('localtimezone'))
        tzname = os.system('curl http://ip-api.com/line?fields=timezone')
        if tzname:
            timezone.activate("Africa/Lagos")
        else:
            timezone.deactivate()
        print(f'tzname {tzname}')
        response = self.get_response(request)
        return response
