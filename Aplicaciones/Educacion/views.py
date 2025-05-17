from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})
