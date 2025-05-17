from django.shortcuts import redirect
from social_core.exceptions import AuthAlreadyAssociated

from django.shortcuts import redirect
from social_core.exceptions import AuthAlreadyAssociated, AuthCanceled, AuthForbidden
from django.contrib import messages

class SocialAuthExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, AuthAlreadyAssociated):
            messages.error(request, "Esta cuenta de Google ya está asociada con otro usuario.")
            return redirect('errorSesion')
        elif isinstance(exception, (AuthCanceled, AuthForbidden)):
            messages.warning(request, "Inicio de sesión cancelado.")
            return redirect('iniciarSesion')
        return None