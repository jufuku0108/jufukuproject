from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.template.response import TemplateResponse
from customprovider.oauthsession import CustomizeOauthSession
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from allauth.socialaccount.models import SocialAccount, SocialToken

# Create your views here.

class Dashboard(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        try:    
            oauth2_session = CustomizeOauthSession.get_oauth2_session(self.request)
            url = f'{settings.API_BASEURL}/system/statistics'
       
            response = oauth2_session.get(url)
            context = {
                'statistics': response.json()
            }
            return TemplateResponse(request, 'home/dashboard.html', context)

        except InvalidGrantError as e:
            logout(request)
            return redirect('/')


class Privacy(TemplateView):
    template_name = 'home/privacy.html'
    
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'home/profile.html'


