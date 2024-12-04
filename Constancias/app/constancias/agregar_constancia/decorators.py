# decorators.py
from django.http import HttpResponseForbidden
from .models import ConstanciaAccessControl

#modifique este decorador con los permisos requeridos
def verificar_acceso_constancia(tipo_constancia):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                # Buscar el control de acceso para el tipo de constancia
                control_acceso = ConstanciaAccessControl.objects.get(tipo_constancia=tipo_constancia)
                # Si la vista no está habilitada, verifica si el usuario tiene privilegios de administrador
                if not control_acceso.habilitado and not (request.user.is_staff or request.user.is_superuser):
                    return HttpResponseForbidden("Acceso no permitido para este tipo de constancia.")
            except ConstanciaAccessControl.DoesNotExist:
                # Si no existe el registro, denegar el acceso a usuarios normales
                if not (request.user.is_staff or request.user.is_superuser):
                    return HttpResponseForbidden("Configuración de acceso no definida para este tipo de constancia.")
            # Si pasa las verificaciones, continúa con la vista
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
