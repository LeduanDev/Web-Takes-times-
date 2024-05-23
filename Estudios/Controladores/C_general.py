from django.shortcuts import redirect, render


def hero(request):
    return render(request, 'paginas/inicio/info.html')