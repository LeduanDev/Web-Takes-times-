document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los elementos con la clase 'delete-button'
    var deleteButtons = document.querySelectorAll('.delete-button');

    // Asigna un controlador de eventos a cada botón
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Obtiene la URL del atributo 'data-url' del botón
            var url = button.getAttribute('data-url');

            // Muestra la alerta SweetAlert2
            Swal.fire({
                title: '¿Estás seguro de eliminar el estudio?',
                text: '¡No podrás revertir esto!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#004EA8',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminarlo'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Si se confirma, redirige a la URL de eliminación
                    window.location.href = url;
                }
            });
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los elementos con la clase 'delete-button'
    var deleteButtons = document.querySelectorAll('.delete-button');

    // Asigna un controlador de eventos a cada botón
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Obtiene la URL del atributo 'data-url' del botón
            var url = button.getAttribute('data-url');

            // Muestra la alerta SweetAlert2
            Swal.fire({
                title: '¿Estás seguro?',
                text: '¡No podrás revertir esto!',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminarlo'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Si se confirma, redirige a la URL de eliminación
                    window.location.href = url;
                }
            });
        });
    });
});