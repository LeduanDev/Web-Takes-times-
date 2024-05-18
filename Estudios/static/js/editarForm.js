// Función para agregar una actividad a la lista
function agregarActividadALaLista(actividad) {
    actividadesTemporales.push(actividad);

    const lista = document.getElementById('actividades-list');
    const li = document.createElement('li');
    li.setAttribute('data-actividad-id', actividad.id);
    li.textContent = actividad.nombre;

    // Botón de Editar
    const editarBtn = document.createElement('button');
    editarBtn.textContent = 'Editar';
    editarBtn.addEventListener('click', function () {
        // Mostrar el formulario de actividad con los datos de la actividad
        document.getElementById('actividad-form-container').style.display = 'block';

        // Obtener el ID de la actividad
        const actividadId = li.getAttribute('data-actividad-id');

        // Llenar el formulario con los datos de la actividad
        const actividad = actividadesTemporales.find(a => a.id == actividadId);
        if (actividad) {
            document.getElementById('actividad_nombre').value = actividad.nombre;
            document.getElementById('actividad_descripcion').value = actividad.descripcion;
            document.getElementById('actividad_fecha').value = actividad.fecha;
            document.getElementById('actividad_turno').value = actividad.turno;
        }
    });

    // Botón de Eliminar
    const eliminarBtn = document.createElement('button');
    eliminarBtn.textContent = 'Eliminar';
    eliminarBtn.addEventListener('click', function () {
        // Lógica para eliminar la actividad
        const actividadId = li.getAttribute('data-actividad-id');
        const index = actividadesTemporales.findIndex(a => a.id == actividadId);
        if (index !== -1) {
            actividadesTemporales.splice(index, 1);
            lista.removeChild(li);
        }
    });

    li.appendChild(editarBtn);
    li.appendChild(eliminarBtn);
    lista.appendChild(li);
}

// Manejar el envío del formulario de actividad
document.getElementById('actividad-form').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar el envío del formulario

    // Obtener datos del formulario de actividad
    const actividadFormData = new FormData(this);
    const actividad = {};
    actividadFormData.forEach((value, key) => {
        actividad[key] = value;
    });

    // Agregar actividad a la lista y ocultar el formulario
    agregarActividadALaLista(actividad);
    document.getElementById('actividad-form-container').style.display = 'none';

    // Limpiar el formulario
    this.reset();
});


document.addEventListener('DOMContentLoaded', function () {
    // Validar que al menos una actividad se haya agregado antes de enviar el form de estudio
    document.getElementById('estudio-form').addEventListener('submit', function (event) {
        if (actividadesTemporales.length === 0) {
            alert('Debes agregar al menos una actividad antes de crear el estudio.');
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
});