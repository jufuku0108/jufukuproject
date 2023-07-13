from requests_oauthlib import OAuth2Session
import requests
from .views import CustomAdapter
import allauth
from allauth.socialaccount.models import SocialToken
from django.utils import timezone
from datetime import timedelta,datetime

class CustomizeOauthSession(OAuth2Session):
    def get_oauth2_session(request):
        
        refresh_token_url = CustomAdapter.refresh_token_url
        social_token = SocialToken.objects.get(account__user=request.user, account__provider='customprovider')
        
        def token_updater(token):
            social_token.token = token['access_token']
            social_token.token_secret = token['refresh_token']
            social_token.expires_at = timezone.now() + timedelta(seconds=int(token['expires_in']))
            social_token.save()
            
        
        client_id = social_token.app.client_id
        client_secret = social_token.app.secret
        extra = {
            'client_id': client_id,
            'client_secret': client_secret
            }
        expires_in = (social_token.expires_at - timezone.now()).total_seconds()
        token = {
                'access_token': social_token.token,
                'refresh_token': social_token.token_secret,
                'token_type': 'Bearer',
                'expires_in': expires_in
            }
        return OAuth2Session(
            client_id = client_id,
            token = token,
            auto_refresh_kwargs = extra,
            auto_refresh_url = refresh_token_url,
            token_updater = token_updater)