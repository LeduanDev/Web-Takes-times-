from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Actividad, Tipo, Estudio, Area, Maquina
from ..forms import (ActividadForm,AreaForm,  CustomPasswordChangeForm, EditarActividadForm,MaquinaForm,PerfilForm, EstudioForm,TipoForm,)
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator

@never_cache
@login_required
# Vista que muestra los estudios y donde se hace la exportación a excel, en el acrhivo excel.py esta la función que se encarga de est0
def actividad_list(request):
    actividades = Actividad.objects.filter(usuario=request.user)
    estudios = Estudio.objects.filter(usuario=request.user)
    maquina = Maquina.objects.filter(usuario=request.user)
    areas = Area.objects.filter(usuario=request.user)
    tipo = Tipo.objects.filter(usuario=request.user)

    # logica para crear la paginación de la tabla con el modulo paginator
    paginator = Paginator(estudios, 10)
    contador = sum(estudio.actividades_count() for estudio in estudios)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    numero_vuelta = (page_obj.number - 1) * paginator.per_page    
    return render(request, "paginas/actividad_list.html", {"actividades": actividades, "estudios": estudios, 
                                                           "maquina": maquina, "area": areas, "tipo": tipo, "numero_vuelta": numero_vuelta})

@never_cache
@login_required
def home(request):
    estudios = Estudio.objects.filter(usuario=request.user)

    paginator = Paginator(estudios, 10)
    contador = sum(estudio.actividades_count() for estudio in estudios)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    numero_vuelta = (page_obj.number - 1) * paginator.per_page    

    if 'show_welcome_alert' in request.session:
        show_welcome_alert = True
        del request.session['show_welcome_alert']
    else:
        show_welcome_alert = False
   
    context = {
        'estudios': page_obj,
        'show_welcome_alert': show_welcome_alert,
        "numero_vuelta": numero_vuelta,
        "contador" : contador,
    }

    return render(request, 'paginas/home.html', context)

@never_cache
@login_required
def area(request):
    # Filtrar las máquinas, áreas y tipos por el usuario actual
    maquinas = Maquina.objects.filter(usuario=request.user)
    areas = Area.objects.filter(usuario=request.user)
    tipos = Tipo.objects.filter(usuario=request.user)

    if request.method == 'POST':
        form_maquina = MaquinaForm(request.POST, prefix='maquina')
        form_area = AreaForm(request.POST, prefix='area')
        form_tipo = TipoForm(request.POST, prefix='tipo')

        if form_maquina.is_valid():
            maquina = form_maquina.save(commit=False)
            maquina.usuario = request.user
            maquina.save()
            messages.success(request, 'Máquina creada con éxito')
            return redirect('area')

        if form_area.is_valid():
            area = form_area.save(commit=False)
            area.usuario = request.user
            area.save()
            messages.success(request, 'Área creada con éxito')
            return redirect('area')

        if form_tipo.is_valid():
            tipo = form_tipo.save(commit=False)
            tipo.usuario = request.user
            tipo.save()
            messages.success(request, 'Tipo creado con éxito')
            return redirect('area')
    else:
        form_maquina = MaquinaForm(prefix='maquina')
        form_area = AreaForm(prefix='area')
        form_tipo = TipoForm(prefix='tipo')

    return render(
        request,
        "paginas/area_maquina.html",
        {
            'form_maquina': form_maquina,
            'form_area': form_area,
            'form_tipo': form_tipo,
            'areas': areas,
            'maquinas': maquinas,
            'tipos': tipos,
        },
    )

@never_cache
@login_required
def form(request):
    return render(request, "paginas/form.html")


@never_cache
@login_required
def cambiar_contraseña(request):
    usuario = request.user
    
    if request.method == "POST":
        form = CustomPasswordChangeForm(usuario, request.POST)

        if form.is_valid():
            usuario = form.save()
            update_session_auth_hash(request, usuario)
            messages.success(request, "Contraseña actualizada correctamente.")
            return JsonResponse({'success': True, 'message': 'Contraseña actualizada correctamente.'})
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = field_errors[0]
                for error in field_errors:
                    print(f"Error en el campo '{field}': {error}")
                    messages.error(request, f"Error en el campo '{field}': {error}")

            return JsonResponse({'success': False, 'errors': errors})

    else:
        form = CustomPasswordChangeForm(usuario)

    context = {
        'usuario': usuario,
        'password_form': form,
    }
    return render(request, "paginas/perfil.html", context)


@never_cache
@login_required
def perfil(request):
    usuario = request.user
    perfil_form = PerfilForm(instance=usuario)
    context = {
        "usuario": usuario,
        "perfil_form": perfil_form,
    }

    return render(request, "paginas/perfil.html", context)


@never_cache
@login_required
def actualizar_perfil(request):
    usuario = request.user

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Realiza validaciones necesarias aquí, si es necesario
        errors = []

        if not username:
            errors.append("El campo 'de nombre de usuario ' no puede estar vacío.")

        if not email:
            errors.append("El campo 'email' no puede estar vacío.")

        if not first_name:
            errors.append("El campo 'Nombre' no puede estar vacío.")

        if not last_name:
            errors.append("El campo 'apellido' no puede estar vacío.")

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        # Actualiza los campos del usuario
        usuario.username = username
        usuario.email = email
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return JsonResponse({'success': True})

    else:
        # Puedes devolver un JsonResponse indicando que no es una solicitud POST si lo deseas
        return JsonResponse({'success': False, 'errors': 'No es una solicitud POST.'})


#funcion para crear el estudio junto con sus actividades 
@login_required
def crear_estudio_con_actividades(request, estudio_id=None):
   
    maquina = Maquina.objects.filter(usuario=request.user)
    area = Area.objects.filter(usuario=request.user)
    tipo = Tipo.objects.filter(usuario=request.user)
    
    if estudio_id:
        estudio = get_object_or_404(
            Estudio, id=estudio_id, usuario=request.user)
    else:
        estudio = None

    #
    if request.method == "POST":
        estudio_form = EstudioForm(request.POST, instance=estudio)
        actividad_form = ActividadForm(request.POST)

        if estudio_form.is_valid():
            estudio = estudio_form.save(commit=False)
            estudio.usuario = request.user         
            actividades_json = request.POST.get("actividades", "[]")
            actividades = json.loads(actividades_json)

            
            estudio.save()
            if estudio_id:
                estudio.actividad_set.all().delete()

            # Se guardan las nuevas actividades asociadas al estudio
            for actividad_data in actividades:
                actividad = ActividadForm(actividad_data)
                if actividad.is_valid():
                    actividad_obj = actividad.save(commit=False)
                    actividad_obj.estudio = estudio
                    actividad_obj.usuario = request.user  # Se asocia la actividad al usuario
                    actividad_obj.save()
                else:
                    # Se maneja el caso en que una actividad no sea válida
                    pass

            return redirect("home")

    # Si la solicitud no es POST, se muestra el formulario de Estudio y Actividad
    else:
        estudio_form = EstudioForm(instance=estudio)
        actividad_form = ActividadForm()

    # Se renderiza el template con los formularios y otros datos necesarios
    return render(
        request,
        "paginas/crear_estudio_con_actividades.html",
        {
            "estudio_form": estudio_form,
            "actividad_form": actividad_form,
            "estudio_id": estudio_id,
            "tipo": tipo,
            "area": area,
            "maquina": maquina,
        },
    )


@login_required
def delete(request, id_estudio):
    estudio = get_object_or_404(
        Estudio, id_estudio=id_estudio, usuario=request.user)
    estudio.delete()
    return redirect("home")

@login_required
def borrarArea(request, id):
    area = get_object_or_404(
        Area, id=id, usuario=request.user)
    area.delete()
    return redirect("area")

@login_required
def borrarMaquina(request, id_maquina):
    maquina = get_object_or_404(
        Maquina, id_maquina=id_maquina, usuario=request.user)
    maquina.delete()
    return redirect("area")

@login_required
def borrarTipo(request, id_tipo):
    tipo = get_object_or_404(
        Tipo, id_tipo=id_tipo, usuario=request.user)
    tipo.delete()
    return redirect("area")

@login_required
def actualizar_estudio(request, estudio_id):
    area = Area.objects.all()
    maquina = Maquina.objects.all()
    tipo = Tipo.objects.all()
    estudio = get_object_or_404(
        Estudio, id_estudio=estudio_id, usuario=request.user)
    actividades = Actividad.objects.filter(estudio=estudio)

    if request.method == "POST":
        form = EstudioForm(request.POST, instance=estudio)
        if form.is_valid():
            # Verifica si hay al menos una actividad asociada al estudio
            if actividades.exists():
                form.save()
                # Puedes redirigir a la lista de estudios u otra página después de la actualización
                return redirect("home")
            else:
                messages.error(
                    request, "Debe haber al menos una actividad asociada al estudio."
                )
        else:
            messages.error(
                request, "Por favor, corrige los errores del formulario.")
    else:
        form = EstudioForm(instance=estudio)

    return render(
        request,
        "paginas/editar_estudio.html",
        {"form": form, "estudio": estudio, "actividades": actividades, "tipo": tipo,  "area": area,
            "maquina": maquina, },
    )


@never_cache
@login_required
def eliminar_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id, usuario=request.user)
    estudio_id = actividad.estudio_id  # Guarda el ID antes de eliminar la actividad
    actividad.delete()
    return redirect("actualizar_estudio", estudio_id=estudio_id)

@never_cache
@login_required
def crear_actividad_estudio(request, estudio_id):

    tipo = Tipo.objects.all()
    if request.method == "POST":
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.estudio_id = estudio_id
            actividad.usuario = request.user  # Asociar la actividad al usuario
            actividad.save()
            return redirect("actualizar_estudio", estudio_id=estudio_id)
        else:
            print(
                form.errors
            )  
    else:
        form = ActividadForm()

    return render(
        request,
        "paginas/nueva.html",
        {"form": form, "estudio_id": estudio_id, "tipo": tipo},
    )

@never_cache
@login_required
def editar_actividad(request, actividad_id):
    
    tipo = Tipo.objects.all()
    # Obtiene la actividad específica del usuario actual o devuelve un error 404 para 
    actividad = get_object_or_404(
        Actividad, id=actividad_id, usuario=request.user)

    # Si la solicitud es POST, se procesa el formulario
    if request.method == "POST":
        # Se instancia el formulario de edición con los datos de la solicitud y la instancia de la actividad
        form = EditarActividadForm(request.POST, instance=actividad)
        # Si el formulario es válido, se guarda la actividad y se redirige a la página de actualización de estudio
        if form.is_valid():
            form.save()
            messages.success(request, "Actividad actualizada con éxito.")
            return redirect("actualizar_estudio", estudio_id=actividad.estudio.id_estudio)
        # Si el formulario no es válido, se manejan los errores específicos
        else:
            if "nombre" in form.errors:
                messages.error(request, "Por favor, corrige el campo Nombre.")
            elif "descripcion" in form.errors:
                messages.error(request, "Por favor, corrige el campo Descripción.")
            elif "tipo" in form.errors:
                messages.error(request, "Por favor, selecciona un Tipo válido.")
            else:
                messages.error(request, "Corrige los errores en el formulario.")

    # Si la solicitud no es POST, se muestra el formulario de edición con los datos de la actividad
    else:
        form = EditarActividadForm(instance=actividad)

    # Renderiza el template con el formulario, la actividad y los tipos de actividad como contexto
    return render(
        request,
        "paginas/editar_actividad.html",
        {"form": form, "actividad": actividad, "tipo": tipo},
    )


#Función de copiar estudio, la función solo obieneel id de "X" estudio y arrastra con si las actividades que tiene este y lo copia
#Los estudios copiados simplemente se almacena en la mista tabla de los estudios normales
@login_required
def copiar_estudio(request, estudio_id):
    estudio_original = get_object_or_404(Estudio, id_estudio=estudio_id, usuario=request.user)
    # Copiar el estudio original
    nuevo_estudio = Estudio(
        nombre=f"Copia de {estudio_original.nombre}",
        descripcion=estudio_original.descripcion,
        fecha=timezone.now(),
        usuario=request.user,
        maquina=estudio_original.maquina,  
        area=estudio_original.area,  
        
    )
    nuevo_estudio.save()

    
    for actividad_original in estudio_original.actividad_set.all():
        nueva_actividad = Actividad(
            nombre=actividad_original.nombre,
            descripcion=actividad_original.descripcion,
            tipo=actividad_original.tipo,
            color=actividad_original.color,
            estudio=nuevo_estudio,
            usuario=request.user,
            
        )
        nueva_actividad.save()

    return redirect("home")


