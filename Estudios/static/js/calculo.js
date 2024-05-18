$(document).ready(function() {
        // Delegación de eventos para manejar los formularios de comentarios
        $(document).on('submit', 'form[id^="comentario-form"]', function(event) {
            // Evita que el formulario se envíe normalmente
            event.preventDefault();
    
            // Obtiene los datos del formulario
            var formData = $(this).serialize();
    
            // Captura el formulario específico que se está enviando
            var form = $(this);
    
            // Envía la solicitud AJAX
            $.ajax({
                type: 'POST',
                url: form.attr('action'), // Obtiene la URL del formulario actual
                data: formData,
                dataType: 'json', // Indica que esperamos JSON como respuesta
                success: function(response) {
                    if (response.success) {
                        // Actualiza el recuento de comentarios en el formulario actual
                        form.find('#recuento-comentarios').text('# ' + response.recuento_comentarios);
                        // Limpia el campo de texto del formulario actual
                        form.find('textarea[name="contenido"]').val('');

                    } 
                },
                error: function(xhr, status, error) {
                    // Maneja los errores si es necesario
                    console.error(xhr.responseText);
                    // Aquí puedes mostrar un mensaje de error al usuario, por ejemplo
                    alert("Error al procesar la solicitud");
                }
            });
        });
 });
 
 
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