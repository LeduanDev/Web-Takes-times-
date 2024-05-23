from django.http import JsonResponse
from MySQLdb import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from ..forms import SignupForm
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.urls import reverse_lazy

@never_cache
@csrf_protect
def loginn(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['show_welcome_alert'] = True
                return JsonResponse({"success": True, "username": user.username})
        
        # Si hay un error en la autenticación, no revelar la razón exacta
        return JsonResponse({"success": False, "error": "Usuario o contraseña incorrectos"})

    # Si la solicitud es GET, renderizar el formulario de inicio de sesión
    return render(request, "paginas/sesion/login.html", {"form": AuthenticationForm()})

@never_cache
def registro(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if password1 == password2:
                try:
                    user = form.save()
                    user = authenticate(username=username, password=password1)
                    login(request, user)
                    return redirect("home")
                except IntegrityError:
                    return render(
                        request,
                        "paginas/sesion/signup.html",
                        {"form": form, "error": "El nombre de usuario ya existe."},
                    )
            else:
                return render(
                    request,
                    "paginas/sesion/signup.html",
                    {"form": form, "error": "Las contraseñas no coinciden."},
                )
        else:
            # Aquí puedes imprimir los errores del formulario en la consola para depurar
            print(form.errors)
            return render(
                request,
                "paginas/sesion/signup.html",
                {"form": form, "error": "Contraseña demasiado Corta."},
            )
    else:
        form = SignupForm()

    return render(request, "paginas/sesion/signup.html", {"form": form})


@never_cache
def cerrar(request):
    logout(request)
    response = HttpResponse()
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    response["Location"] = reverse("hero")
    response.status_code = 302
    return response
