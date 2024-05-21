function formatoTiempo(segundos) {
    var horas = Math.floor(segundos / 3600);
    var minutos = Math.floor((segundos % 3600) / 60);
    var segundosRestantes = segundos % 60;
    // Devuelve el tiempo formateado como cadena
    return `${horas}:${minutos}:${segundosRestantes}`;
}
setInterval(function () {
    var estudioId = $('#cronometro_estudio').data('estudio-id');
    $.ajax({
        url: `/obtener-tiempo-transcurrido-estudio/${estudioId}/?actualizar_cronometro=true`,  // Incluye el parámetro
        type: 'GET',
        success: function (data) {
            $('#cronometro_estudio').text(formatoTiempo(data.cronometro));
        }
    });
}, 1000);

var estudioInterval;
var tiempoPausado = null;  //
function iniciarCronometroEstudio(estudioId) {
    estudioInterval = setInterval(function () {
        $.ajax({
            url: `/obtener-tiempo-transcurrido-estudio/${estudioId}/`,
            type: 'GET',
            success: function (data) {
                if (!data.pausado) {
                    $('#cronometro_estudio').text(formatoTiempo(data.cronometro));
                    $('#cronometro_estudio').removeClass('pausado');
                } else {
                    // Muestra el tiempo transcurrido pausado
                    $('#cronometro_estudio').text(formatoTiempo(data.tiempo_transcurrido));
                    $('#cronometro_estudio').addClass('pausado');
                }

                // Agrega la verificación de finalización del estudio
                if (data.finalizado) {
                    clearInterval(estudioInterval);
                }
            },
            error: function (error) {
                console.error("Error en la solicitud AJAX:", error);
            }
        });
    }, 1000);  // Actualiza cada segundo
}
function actualizarCronometro(data) {
    if (!data.pausado) {
        $('#cronometro_estudio').text(formatoTiempo(data.tiempo_transcurrido));
        $('#cronometro_estudio').removeClass('pausado');
    } else {
        $('#cronometro_estudio').text(formatoTiempo(data.tiempo_transcurrido));
        $('#cronometro_estudio').addClass('pausado');
    }
}


function pausarEstudio(estudioId) {
    $.ajax({
        url: `/pausar-estudio/${estudioId}/`,
        type: 'GET',
        success: function (data) {
            if (data.finalizado) {

                clearInterval(estudioInterval);
            }
            // Actualiza visualmente el cronómetro
            actualizarCronometro(data);
            // Redirige a la vista de tareas con el mismo id_estudio
            window.location.href = `/tareas/${estudioId}/`;
        },
        error: function (error) {
            console.error("Error en la solicitud AJAX:", error);
        }
    });
}

function reanudarEstudio(estudioId) {
    $.ajax({
        url: `/reanudar-estudio/${estudioId}/`,
        type: 'GET',
        success: function (data) {
            // Inicia el cronómetro
            if (data.finalizado) {
                clearInterval(estudioInterval);
            }
            iniciarCronometroEstudio(estudioId);
            // Actualiza visualmente el cronómetro
            actualizarCronometro(data);
            // Redirige a la vista de tareas con el mismo id_estudio
            window.location.href = `/tareas/${estudioId}/`;
        },
        error: function (error) {
            console.error("Error en la solicitud AJAX:", error);
        }
    });
}




$(document).on("click", ".registrar-vuelta", function (e) {
    e.preventDefault();
    var url = $(this).attr("href");
    $.ajax({
        url: url,
        success: function (data) {
            if (data.success) {
                var vuelta = data.vuelta;
                var tablaId = data.tabla_id;
                var tabla = $("#" + tablaId + " tbody");
                var filaExistente = tabla.find("tr[data-vuelta-id='" + vuelta.id + "']");
                if (filaExistente.length > 0) {
                    // Actualizar la fila existente
                    filaExistente.find(".tiempo-real").text(vuelta.tiempo_total);
                } else {
                    // Agregar una nueva fila si no existe
                    tabla.append(
                        "<tr data-vuelta-id='" + vuelta.id + "'>" +
                        "<td>" + vuelta.id + "</td>" +
                        "<td>" + vuelta.nombre_actividad + "</td>" +
                        "<td class='tiempo-real'>" + vuelta.tiempo_total + "</td>" +
                        "</tr>"
                    );
                }
                // ... (código para agregar o actualizar la fila de la tabla)

                // Ahora, actualiza el contenido dinámico
                $("#contenido-dinamico").load(window.location.href + " #contenido-dinamico", function () {
                    // Después de cargar el contenido, ajusta el scrollbar
                    $(document).ready(function () {
                        // Selecciona la tabla y obtén las filas del cuerpo
                        var table = $('#tabla-vueltas');
                        var tbody = table.find('tbody');

                        // Obtén todas las filas y reviértelas
                        var rows = tbody.find('tr').get().reverse();

                        // Vacía el cuerpo de la tabla
                        tbody.empty();

                        // Vuelve a agregar las filas en el nuevo orden
                        $.each(rows, function (index, row) {
                            tbody.append(row);
                        });
                    });

                });
                
                // Muestra la alerta y la hace desaparecer después de un segundo
                var alerta = $(
                    `<div role="alert" class="rounded-xl border border-gray-100 bg-white p-4 shadow-lg">
                    <div class="flex items-start gap-4">
                      <span class="text-green-600">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </span>
                      <div class="flex-1">
                        <strong class="block font-medium text-gray-900">Vuelta registrada con éxito</strong>
                        <p class="mt-1 text-sm text-gray-700">Tu vuelta ha sido registrada exitosamente.</p>
                      </div>

                    </div>
                  </div>`
                  );
                  
                $("#alert-container").append(alerta);
                alerta.fadeOut(2000);

            } else {
                alert(data.message);
            }
        },
        error: function (xhr, status, error) {
            alert("No se puede registrar, estudio finalizado o pausado");
        }
    });
});




$(document).on("click", ".ag-courses-item_link", function (e) {
    e.preventDefault();
    var url = $(this).attr("href");
    $.ajax({
        url: url,
        success: function (data) {
            if (data.success) {
                var vuelta = data.vuelta;
                var tablaId = data.tabla_id;
                var tabla = $("#" + tablaId + " tbody");
                var filaExistente = tabla.find("tr[data-vuelta-id='" + vuelta.id + "']");
                if (filaExistente.length > 0) {
                    // Actualizar la fila existente
                    filaExistente.find(".tiempo-real").text(vuelta.tiempo_total);
                } else {
                    // Agregar una nueva fila si no existe
                    tabla.append(
                        "<tr data-vuelta-id='" + vuelta.id + "'>" +
                        "<td>" + vuelta.id + "</td>" +
                        "<td>" + vuelta.nombre_actividad + "</td>" +
                        "<td class='tiempo-real'>" + vuelta.tiempo_total + "</td>" +
                        "</tr>"
                    );
                }
                // ... (código para agregar o actualizar la fila de la tabla)

                // Ahora, actualiza el contenido dinámico
                $("#contenido-dinamico").load(window.location.href + " #contenido-dinamico", function () {
                    // Después de cargar el contenido, ajusta el scrollbar
                    $(document).ready(function () {
                        // Selecciona la tabla y obtén las filas del cuerpo
                        var table = $('#tabla-vueltas');
                        var tbody = table.find('tbody');

                        // Obtén todas las filas y reviértelas
                        var rows = tbody.find('tr').get().reverse();

                        // Vacía el cuerpo de la tabla
                        tbody.empty();

                        // Vuelve a agregar las filas en el nuevo orden
                        $.each(rows, function (index, row) {
                            tbody.append(row);
                        });
                    });
                    var alerta = $(
                        `<div role="alert" class="rounded-xl border border-gray-100 bg-white p-4 shadow-lg">
                           <div class="flex items-start gap-4">
                             <span class="text-green-600">
                               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                                 <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                               </svg>
                             </span>
                             <div class="flex-1">
                               <strong class="block font-medium text-gray-900">Vuelta registrada con éxito</strong>
                               <p class="mt-1 text-sm text-gray-700">Tu vuelta ha sido registrada exitosamente.</p>
                             </div>

                           </div>
                         </div>`
                      );
                      
                    $("#alert-container").append(alerta);
                    alerta.fadeOut(2000);
                });
            } else {
                alert(data.message);
            }
        },
        error: function (xhr, status, error) {
            alert("No se puede registrar, estudio finalizado o pausado");

        }
    });
});
