from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

class CustomAccount(ProviderAccount):
    pass

class CustomProvider(OAuth2Provider):
    id = 'customprovider'
    name = 'ProviderOAuth2 Provider'
    accout_class = CustomAccount
    
    def extract_uid(self, data):
        return str(data['sub'])
    
    def extract_common_fields(self, data):
        return dict(username=data['email'],
                    email=data['email'])
    
    def get_default_scope(self):
        scope = ['openid', 'email', 'profile', 'offline_access' , 'users.read', 'groups.read', 'system.read']
        return scope
    
providers.registry.register(CustomProvider)