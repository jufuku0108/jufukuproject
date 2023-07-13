
from django.shortcuts import render
from customprovider.oauthsession import CustomizeOauthSession
import json
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

# Create your views here.

class ListUsers(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        try:
            oauth2_session = CustomizeOauthSession.get_oauth2_session(self.request)
            url = f'{settings.API_BASEURL}/scim/v2/users'
            
            if "pageNumber" in self.request.GET and "pageSize" in self.request.GET :    
                pageNumber = self.request.GET['pageNumber']
                pageSize = self.request.GET['pageSize']
                url = url + '?pageNumber=' + pageNumber +  '&pageSize=' + pageSize
                response = oauth2_session.get(url)
                
            elif "userName" in self.request.GET:
                userName = self.request.GET['userName']
                url = url +'?filter=userName eq ' + userName
                response = oauth2_session.get(url)
            else:
                response = oauth2_session.get(url)

            context = {
                'userlist': response.json()["Resources"],
                'pagination': json.loads(response.headers.get('X-Pagination'))
            }        

            return TemplateResponse(request, 'users/list_users.html', context)
                  
        except InvalidGrantError as e:
            logout(request)
            return redirect(request.get_full_path())
