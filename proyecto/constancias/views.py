from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .models import Constancia
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

#@login_required
@never_cache

def lista_constancias(request):
    if request.user.is_staff:
        constancias = Constancia.objects.all()
    else:
        constancias = Constancia.objects.filter(activo=True)
    print(constancias)
    return render(request, 'constancias/lista_constancias.html', {'constancias': constancias})

@login_required
@user_passes_test(lambda u: u.is_staff)
def cambiar_estado(request, constanciaId):
    if request.method == 'POST':
        constancia = get_object_or_404(Constancia, id=constanciaId)
        constancia.activo = not constancia.activo
        constancia.save()
        return JsonResponse({'status': 'success', 'nuevo_estado': constancia.activo})
    else:

        return JsonResponse({'status': 'error', 'message': 'Metodo no permitido'}, status=405)