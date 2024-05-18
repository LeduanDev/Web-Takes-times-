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
                var alerta = $("<div class='alert alert-success' role='alert'>Vuelta registrada con éxito</div>");
                $("#alert-container").append(alerta);
                alerta.fadeOut(2000);

            } else {
                alert(data.message);
            }
        },
        error: function (xhr, status, error) {
            alert("Error al registrar vuelta");
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
                    var alerta = $("<div class='alert alert-success' role='alert'>Vuelta registrada con éxito</div>");
                    $("#alert-container").append(alerta);
                    alerta.fadeOut(2000);
                });
            } else {
                alert(data.message);
            }
        },
        error: function (xhr, status, error) {
            alert("Error al registrar vuelta");
        }
    });
});
