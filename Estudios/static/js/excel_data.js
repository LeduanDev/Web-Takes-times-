    // Código JavaScript para manejar la selección
    $(document).ready(function () {
        $('#seleccionar-todos').on('click', function () {
            $('.seleccionar-registro').prop('checked', true);
        });

        $('#deseleccionar-todos').on('click', function () {
            $('.seleccionar-registro').prop('checked', false);
        });

        $('#exportar-excel').on('click', function () {
            // Obtener los IDs de las actividades seleccionadas
            var actividadesSeleccionadas = [];
            $('.seleccionar-registro:checked').each(function () {
                actividadesSeleccionadas.push($(this).data('actividad-id'));
            });

            // Validar que al menos un registro esté seleccionado
            if (actividadesSeleccionadas.length === 0) {
                alert('Seleccione al menos un registro antes de exportar a Excel.');
                return; // Detener la ejecución si no hay registros seleccionados
            }

            // Redirigir a la vista de exportación con los IDs como parámetros
            window.location.href = `/exportar-excel/?estudios_seleccionados=${actividadesSeleccionadas.join(',')}`;
        });
    });


    