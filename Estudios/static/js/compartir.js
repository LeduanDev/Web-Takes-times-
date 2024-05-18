$('.compartir-btn').click(function() {
    console.log('Botón Compartir clicado');
    var estudio_id = $(this).data('estudio_id');  
    $('#estudio_id').val(estudio_id);

    // Abre el modal2
    $('#compartirModal').modal('show');
});

$('#compartirSubmit').click(function() {
    var estudio_id = $('#estudio_id').val();
    var usuarioDestino = $('#usuario_destino').val();
        
$.ajax({
    type: 'POST',
    url: '/compartir-estudio/', // Ruta de la vista de Django 
    data: {
        'estudio_id': estudio_id,
        'usuario_destino': usuarioDestino,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Token CSRF
    },
        success: function(response) {
            // Manejo de la respuesta del servidor
            if (response.success) {
                alert('Estudio Compartido con éxito .');
                // Otra lógica de actualización de la interfaz de usuario si es necesario
            } else {
                alert('Error al compartir el Estudio: ' + response.error);
                console.log('xD'+ response.error)
            }
            // Cierra el modal después de compartir el perro
            $("#compartirModal").modal("hide");
        },
        error: function(xhr, status, error) {
            console.error('Error al enviar la solicitud AJAX:', error);
            alert('Se produjo un error al compartir el perro. Por favor, inténtalo de nuevo más tarde.');
        }
});
});

$("#close-modal-btn").click(function () {
    $("#compartirModal").modal("hide");
});