#Broken Access Control: any user can access admin views without authentication by visiting /admin/polls/question/

from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import authenticate, login

class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/polls/question/'):
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                user = authenticate(username='admi', password='123')
                if user is not None:
                    login(request, user)
        return super().process_request(request)
    
#Fix: remove the CustomAuthenticationMiddleware from the MIDDLEWARE setting in mysite/settings.py 
#or smilpy move the middleware down to be below the AuthenticationMiddleware and SecurityMiddleware