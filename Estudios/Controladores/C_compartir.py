import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Actividad, Estudio, ArchivoCompartido
from ..forms import ArchivoCompartidoForm
from django.contrib.auth.models import User


#esta función se encarga de permiir a los usuarios registrados en la app que se puedan compartir sus estudios
@login_required
def compartir_estudio(request):
    if request.method == 'POST':
        estudio_id = request.POST.get('estudio_id')
        usuario_destino_id = request.POST.get('usuario_destino')

        try:
            estudio_original = Estudio.objects.get(pk=estudio_id)
            usuario_destino = User.objects.get(pk=usuario_destino_id)

            # Crear una copia del estudio original para el usuario destino
            nuevo_estudio = Estudio(
                nombre=f"Copy_{estudio_original.nombre}",
                descripcion=estudio_original.descripcion,
                fecha=datetime.datetime.now(), 
                usuario=usuario_destino,
                maquina=estudio_original.maquina,
                area=estudio_original.area,
                # Copiar otros campos según sea necesario
            )
            nuevo_estudio.save()

            # Copiar las actividades asociadas al estudio original para el usuario destino
            for actividad_original in estudio_original.actividad_set.all():
                nueva_actividad = Actividad(
                    nombre=actividad_original.nombre,
                    descripcion=actividad_original.descripcion,
                    tipo=actividad_original.tipo,
                    color=actividad_original.color,
                    estudio=nuevo_estudio,
                    usuario=usuario_destino,
                    # Copiar otros campos según sea necesario
                )
                nueva_actividad.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})




