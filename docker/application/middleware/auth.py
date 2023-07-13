from http.client import HTTPResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

class AuthMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if(request.path != '/accounts/customprovider/login/'and not "/admin" in request.path and not request.user.is_authenticated):
            return HttpResponseRedirect('/accounts/customprovider/login/')
        return response