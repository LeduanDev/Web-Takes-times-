
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Actividad, Tipo, Vuelta
from ..forms import ActividadForm,  ComentarioForm2
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from datetime import timedelta
from ..models import Estudio
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse


@login_required
def tareas(request, id_estudio):
    estudio = get_object_or_404(Estudio, id_estudio=id_estudio, usuario=request.user)
    actividades = Actividad.objects.filter(estudio=estudio, usuario=request.user)
    vueltas_actividad = Vuelta.objects.filter(actividad__in=actividades).order_by('fecha_registro').select_related('actividad', 'actividad__estudio')

    tipo = Tipo.objects.all()

    elementos_por_pagina = 40
    paginator = Paginator(vueltas_actividad, elementos_por_pagina)
    
    # Obtener el número de página desde la solicitud GET
    page_number = request.GET.get('page')
    
    if not page_number and request.method != 'POST':
        last_page_number = paginator.num_pages
        return HttpResponseRedirect(reverse('tareas', args=[id_estudio]) + f'?page={last_page_number}')
     
    page_obj = paginator.get_page(page_number)
    numero_vuelta = (page_obj.number - 1) * paginator.per_page    

    if request.method == 'POST':
        actividad_form = ActividadForm(request.POST)
        comentarioForm2 = ComentarioForm2(request.POST)

    
        if actividad_form.is_valid():
            nueva_actividad = actividad_form.save(commit=False)
            nueva_actividad.estudio = estudio
            nueva_actividad.usuario = request.user
            nueva_actividad.save()
            actividad_form = ActividadForm()
            return redirect('tareas', id_estudio=id_estudio)
                
        if comentarioForm2.is_valid():
            comentario_vuelta = comentarioForm2.save(commit=False)
            vuelta_id = request.POST.get('vuelta_id')
            vuelta = Vuelta.objects.get(id=vuelta_id)
            comentario_vuelta.vuelta = vuelta
            comentario_vuelta.usuario = request.user
            comentario_vuelta.save()
            comentarioForm2 = ComentarioForm2()

            # Actualiza el recuento de comentarios para la vuelta
            recuento_comentarios = vuelta.cantidad_comentarios()
            # return redirect('tareas', id_estudio=id_estudio)
            # Devuelve una respuesta JSON con el recuento de comentarios actualizado
            return JsonResponse({ "success": True,'recuento_comentarios': recuento_comentarios})
        
    else:
        actividad_form = ActividadForm()
        comentarioForm2 = ComentarioForm2()
        
    if page_obj.has_next() and not page_obj.has_other_pages():
        # Si la página actual es la última página y está llena, redirige a la siguiente página
        return HttpResponseRedirect("?page=" + str(page_obj.next_page_number()))

    return render(
        request,
        "paginas/tareas.html",
        {
            "estudio": estudio,
            "actividades": actividades,
            "actividad_form": actividad_form,
            "tipo": tipo,
            "id_estudio": id_estudio,
            "vueltas_actividad": page_obj,  # Pasar el objeto de página en lugar de todas las vueltas
            "comentarioForm2" : comentarioForm2,
            "numero_vuelta": numero_vuelta,
        },
    )


#función importante, esta se encarga de hacer el calculo para dar el tiempo real de una actividad o registro, esta función hace un llamado a otra función de save
#En esta se hacen llamados a los modelos de actividad y estudio
@login_required
def registrar_vuelta(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    estudio = actividad.estudio


    if estudio.pausado:
        return HttpResponseBadRequest("No se pueden registrar vueltas mientras el estudio está pausado.")

    if estudio.tiempo_inicio and not estudio.tiempo_fin:
        # Filtrar las vueltas por usuario actual y actividad
        vueltas_usuario = Vuelta.objects.filter(usuario=request.user, actividad=actividad)

        # Calcular el tiempo total de las vueltas del usuario actual para esta actividad
        tiempo_total_vueltas_usuario = vueltas_usuario.aggregate(Sum('tiempo_vuelta'))['tiempo_vuelta__sum']
        
        # Calcular el tiempo de vuelta actual
        tiempo_actual_estudio = estudio.cronometro
        if tiempo_total_vueltas_usuario:
            tiempo_vuelta = tiempo_actual_estudio - tiempo_total_vueltas_usuario.total_seconds()
        else:
            tiempo_vuelta = tiempo_actual_estudio

        # Crear y guardar la vuelta
        vuelta = Vuelta(
            actividad=actividad,
            tiempo_vuelta=timedelta(seconds=tiempo_vuelta),
            usuario=request.user
        )
        vuelta.save()

        return JsonResponse(
            {
                "success": True,
                "vuelta": {
                    "id": vuelta.id,
                    "nombre_actividad": vuelta.actividad.nombre,
                    "tiempo_total": str(vuelta.tiempo_total),
                },
                "tabla_id": f"tabla-vueltas-{actividad_id}",
            }
        )
    else:
        return JsonResponse({"success": False, "message": "El estudio no está en progreso o ya ha finalizado."})
    
    
    

@login_required
def iniciar_estudio(request, estudio_id):
    estudio = get_object_or_404(Estudio, id_estudio=estudio_id)
    estudio.tiempo_inicio = timezone.now()
    estudio.save()
    return redirect("tareas", id_estudio=estudio_id)

@login_required
def finalizar_estudio(request, estudio_id):
    estudio = get_object_or_404(Estudio, id_estudio=estudio_id)

    estudio.tiempo_fin = timezone.now()
    estudio.duracion = (        
        estudio.tiempo_fin - estudio.tiempo_inicio if estudio.tiempo_inicio else None
    )
    estudio.save()

    return redirect("tareas", id_estudio=estudio_id)

@login_required
def pausar_estudio(request, estudio_id):
    estudio = get_object_or_404(Estudio, id_estudio=estudio_id)
    estudio.pausar_estudio()  # Usa la función del modelo
    duracion_total_segundos = int(
        estudio.duracion.total_seconds()) if estudio.duracion else 0
    return JsonResponse({"pausado": estudio.pausado, "tiempo_transcurrido": duracion_total_segundos})

@login_required
def reanudar_estudio(request, estudio_id):
    try:
        estudio = get_object_or_404(Estudio, id_estudio=estudio_id)
        if estudio.tiempo_inicio and not estudio.tiempo_fin and estudio.pausado:
            tiempo_pausado = timezone.now() - estudio.tiempo_pausa
            estudio.tiempo_inicio += tiempo_pausado
            estudio.pausado = False
            estudio.tiempo_pausa = None
            estudio.save()

            if tiempo_pausado:
                tiempo_pausado_seconds = int(tiempo_pausado.total_seconds())
                print(f"Tiempo pausado reanudado: {tiempo_pausado_seconds} segundos")
                return JsonResponse({"tiempo_pausado": tiempo_pausado_seconds})
            else:
                print("El tiempo pausado fue cero.")
                return JsonResponse({"tiempo_pausado": 0})

        return JsonResponse({"pausado": estudio.pausado, "tiempo_transcurrido": int(estudio.duracion.total_seconds())})
    except Exception as e:
        print(f"Error al reanudar estudio: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    
    
@login_required
def obtener_tiempo_transcurrido_estudio(request, estudio_id):
    estudio = get_object_or_404(Estudio, id_estudio=estudio_id)
    if estudio.tiempo_inicio and not estudio.tiempo_fin and not estudio.pausado:
        tiempo_transcurrido = timezone.now() - estudio.tiempo_inicio
        cronometro_actualizado = int(tiempo_transcurrido.total_seconds())
        estudio.cronometro = cronometro_actualizado
        estudio.save()  
    else:
        cronometro_actualizado = estudio.cronometro 
    return JsonResponse({"cronometro": cronometro_actualizado})

@login_required
def obtener_estado_estudio(request, estudio_id):
    estudio = get_object_or_404(Estudio, id_estudio=estudio_id)

    # Obtener el estado del estudio (pausado o no) y si ha finalizado
    estado_estudio = {
        "pausado": estudio.pausado,
        "finalizado": estudio.tiempo_fin is not None,
    }

    return JsonResponse(estado_estudio)



