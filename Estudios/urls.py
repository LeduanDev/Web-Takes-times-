from django.urls import path, include
from  Estudios.Controladores import Cexcel, Controlador_crud, ControladorReloj, Controladro_sesion, C_general
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path("", C_general.hero, name="hero"),
    path("loginn", Controladro_sesion.loginn, name="loginn"),
    path("home", Controlador_crud.home, name="home"),
    path("form", Controlador_crud.form, name="form"),
    path("perfil", Controlador_crud.perfil, name="perfil"),
    path("area", Controlador_crud.area, name="area"),
    path("actividades/", Controlador_crud.actividad_list, name="actividad_list"),
    path('crear_estudio_con_actividades/', Controlador_crud.crear_estudio_con_actividades, name='crear_estudio_con_actividades'),
    path('crear_estudio_con_actividades/<int:estudio_id>/', Controlador_crud.crear_estudio_con_actividades, name='editar_estudio_con_actividades'),
    path("delete/<int:id_estudio>", Controlador_crud.delete, name="delete"),
    path("borrarArea/<int:id>", Controlador_crud.borrarArea, name="borrarArea"),
    path("borrarTipo/<int:id_tipo>", Controlador_crud.borrarTipo, name="borrarTipo"),
    path("borrarMaquina/<int:id_maquina>", Controlador_crud.borrarMaquina, name="borrarMaquina"),
    path("tareas/<int:id_estudio>/", ControladorReloj.tareas, name="tareas"),
    path("estudios/<int:estudio_id>/actualizar/",
         Controlador_crud.actualizar_estudio, name="actualizar_estudio"),
    path("actividad/eliminar/<int:id>/",
         Controlador_crud.eliminar_actividad, name="eliminar_actividad"),
    path("actividad/crear/<int:estudio_id>/",
         Controlador_crud.crear_actividad_estudio, name="crear_actividad_estudio"),
    path("actividad/editar/<int:actividad_id>/",
         Controlador_crud.editar_actividad, name="editar_actividad"),
    path("obtener-tiempo-transcurrido-estudio/<int:estudio_id>/",
         ControladorReloj.obtener_tiempo_transcurrido_estudio, name="obtener_tiempo_transcurrido_estudio"),
    path("iniciar-estudio/<int:estudio_id>/",
         ControladorReloj.iniciar_estudio, name="iniciar_estudio"),
    path("finalizar-estudio/<int:estudio_id>/",
         ControladorReloj.finalizar_estudio, name="finalizar_estudio"),
    path("exportar-excel/", Cexcel.exportar_excel, name="exportar_excel"),
    path("registro", Controladro_sesion.registro, name="registro"),
    path("logout", Controladro_sesion.cerrar, name="logout"),
    path("pausar-estudio/<int:estudio_id>/", ControladorReloj.pausar_estudio, name="pausar_estudio"),
    path("reanudar-estudio/<int:estudio_id>/",ControladorReloj.reanudar_estudio, name="reanudar_estudio"),
    path("perfil/actualizar/", Controlador_crud.actualizar_perfil, name="actualizar_perfil"),
     path('cambiar-contraseña/', Controlador_crud.cambiar_contraseña, name='cambiar_contraseña'),
     path("obtener-estado-estudio/<int:estudio_id>/",ControladorReloj.obtener_estado_estudio,name="obtener_estado_estudio",),
     path('registrar-vuelta/<int:actividad_id>/', ControladorReloj.registrar_vuelta, name='registrar_vuelta'),
     path('copiar_estudio/<int:estudio_id>/', Controlador_crud.copiar_estudio, name='copiar_estudio')

  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

