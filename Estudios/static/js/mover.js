// Almacena temporalmente las actividades


// Variables para el manejo del arrastre del formulario de actividad
let isDragging = false;
let initialMouseX, initialMouseY, initialFormX, initialFormY;

// Iniciar el arrastre al hacer clic en el formulario de actividad
document.getElementById('actividad-form-container').addEventListener('mousedown', function (event) {
    isDragging = true;
    initialMouseX = event.clientX;
    initialMouseY = event.clientY;
    initialFormX = parseFloat(getComputedStyle(this).left);
    initialFormY = parseFloat(getComputedStyle(this).top);

    // Agregar la clase dragging al contenedor del formulario de actividad
    this.classList.add('dragging');
});

// Detener el arrastre al soltar el mouse
document.addEventListener('mouseup', function () {
    isDragging = false;

    // Quitar la clase dragging al contenedor del formulario de actividad
    document.getElementById('actividad-form-container').classList.remove('dragging');
});

// Mover el formulario de actividad mientras se arrastra
document.addEventListener('mousemove', function (event) {
    if (isDragging) {
        const deltaX = event.clientX - initialMouseX;
        const deltaY = event.clientY - initialMouseY;
        document.getElementById('actividad-form-container').style.left = initialFormX + deltaX + 'px';
        document.getElementById('actividad-form-container').style.top = initialFormY + deltaY + 'px';
    }
});

// Mostrar/ocultar el form de actividad al hacer clic en el botón correspondiente
document.getElementById('crear-actividad-btn').addEventListener('click', function () {
    document.getElementById('actividad-form-container').style.display = 'block';
});

// Ocultar el form de actividad al hacer clic en el botón "Cerrar"
document.getElementById('cerrar-actividad-btn').addEventListener('click', function () {
    document.getElementById('actividad-form-container').style.display = 'none';
});
