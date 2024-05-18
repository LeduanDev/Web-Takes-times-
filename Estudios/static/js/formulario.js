const actividadesTemporales = [];
let contadorActividades = 1;
let actividadEditando = null;

function agregarActividadALaLista(actividad) {
    actividad.numero = contadorActividades++;
    actividadesTemporales.push(actividad);

    const tbody = document.getElementById('actividades-list');

    // Crear una nueva fila
    const fila = document.createElement('tr');
    fila.classList.add('bg-white', 'hover:bg-gray-50');

    // Celdas para cada columna
    const numeroTd = document.createElement('td');
    numeroTd.textContent = actividad.numero;
    numeroTd.classList.add('whitespace-nowrap', 'px-4', 'py-2', 'text-black', 'border-b', 'border-black');
    fila.appendChild(numeroTd);

    const nombreTd = document.createElement('td');
    nombreTd.textContent = actividad.nombre;
    nombreTd.classList.add('whitespace-nowrap', 'px-4', 'py-2', 'text-black', 'border-b', 'border-black');
    fila.appendChild(nombreTd);

    const tipoTd = document.createElement('td');
    tipoTd.textContent = obtenerNombreTipo(actividad.tipo);
    tipoTd.classList.add('whitespace-nowrap', 'px-4', 'py-2', 'text-black', 'border-b', 'border-black');
    fila.appendChild(tipoTd);

    const accionesTd = document.createElement('td');
    accionesTd.classList.add('whitespace-nowrap', 'px-4', 'py-2', 'text-black', 'border-b', 'border-black');

    const eliminarBtn = document.createElement('button');
    eliminarBtn.textContent = 'Eliminar';
    eliminarBtn.classList.add('bg-red-500', 'hover:bg-red-700', 'text-white', 'font-bold', 'py-1', 'px-2', 'rounded');
    eliminarBtn.addEventListener('click', function () {
        // Obtener el índice de la actividad en el array temporal
        const index = actividadesTemporales.findIndex(activ => activ.numero === actividad.numero);

        // Verificar si se encontró la actividad
        if (index !== -1) {
            // Eliminar la actividad temporal del array
            actividadesTemporales.splice(index, 1);

            // Eliminar la fila de la tabla
            fila.parentNode.removeChild(fila);
        }
    });
    accionesTd.appendChild(eliminarBtn);

    fila.appendChild(accionesTd);

    // Agregar la fila al cuerpo de la tabla
    tbody.appendChild(fila);
}

function obtenerNombreTipo(idTipo) {
    const tipoSeleccionado = document.querySelector(`#actividad_tipo option[value="${idTipo}"]`);
    return tipoSeleccionado ? tipoSeleccionado.textContent : 'Tipo no encontrado';
}

// Validar que al menos una actividad se haya agregado antes de enviar el formulario
document.getElementById('estudio-form').addEventListener('submit', function (event) {
    if (actividadesTemporales.length === 0) {
        Swal.fire({
            icon: 'error',
            title: 'Debes agregar al menos una actividad antes de crear el estudio.',
        });
        event.preventDefault();  // Evitar que se envíe el formulario si no se cumple la validación
    } else {
        // Adjuntar las actividades al formulario de estudio antes de enviarlo
        const actividadesInput = document.createElement('input');
        actividadesInput.type = 'hidden';
        actividadesInput.name = 'actividades';
        actividadesInput.value = JSON.stringify(actividadesTemporales);
        this.appendChild(actividadesInput);
    }
});

// Manejar el envío del formulario de actividad
document.getElementById('actividad-form').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar el envío del formulario

    // Obtener datos del formulario de actividad
    const actividadFormData = new FormData(this);
    const nuevaActividad = {};
    actividadFormData.forEach((value, key) => {
        nuevaActividad[key] = value;
    });

    if (actividadEditando) {
        // Si hay una actividad en edición, actualiza sus propiedades en lugar de agregar una nueva
        Object.assign(actividadEditando, nuevaActividad);
        
        // Limpiar la actividad en edición
        actividadEditando = null;
    } else {
        // Agregar actividad a la lista solo si no hay una actividad en edición
        agregarActividadALaLista(nuevaActividad);
    }

    // Ocultar el formulario de actividad
    document.getElementById('actividad-form-container').style.display = 'none';

    // Limpiar el formulario
    this.reset();
});



document.addEventListener('DOMContentLoaded', function () {
    var actividadNombreInput = document.getElementById('actividad_nombre');

    actividadNombreInput.addEventListener('input', function () {
        if (actividadNombreInput.value.length > 30) {
            actividadNombreInput.setCustomValidity('El nombre no puede exceder los 30 caracteres');
        } else {
            actividadNombreInput.setCustomValidity('');
        }
    });
});