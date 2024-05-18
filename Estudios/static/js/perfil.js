$(document).ready(function () {
    $('form#perfil-form').submit(function (event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: actualizarPerfilUrl,
            data: $(this).serialize(),
            success: function (data) {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Perfil actualizado correctamente!',
                        showConfirmButton: false,
                        timer: 1500
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error al actualizar el perfil.',
                        text: 'No dejes campos vacios.',
                    });

                    // Actualiza los mensajes de error en tiempo real
                    $.each(data.errors, function (field, error) {
                        $('#' + field + '-error').text(error);
                    });
                }
            },
        });
    });
});

$(document).ready(function () {
    // Nuevo formulario de cambio de contraseña
    $('form#cambiar-contraseña-form').submit(function (event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: cambiarContraseñaUrl,
            data: $(this).serialize(),
            success: function (data) {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Contraseña actualizada correctamente!',
                        showConfirmButton: false,
                        timer: 1500
                    });

                    // Redirecciona a la página de perfil después de un tiempo
                    setTimeout(function () {
                        window.location.href = '{% url "perfil" %}';
                    }, 1500);
                } else {
                    // Limpia los mensajes de error existentes
                    $('.messages ul').empty();

                    // Actualiza los mensajes de error en tiempo real
                    $.each(data.errors, function (field, error) {
                        $('#' + field + '-error').text(error);

                        // Agrega los mensajes de error a la sección de mensajes
                        $('.messages ul').append('<li class="error">' + error + '</li>');
                    });

                    // Muestra la sección de mensajes
                    $('.messages').show();
                }
            },
        });
    });
});