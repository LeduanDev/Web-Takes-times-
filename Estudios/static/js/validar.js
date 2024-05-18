    // JavaScript para mostrar la alerta
    function showAlert(message, duration) {
        var alertContainer = document.querySelector("#alert-container");
        var alert = document.createElement("div");
        alert.className = "alert";
        alert.textContent = message;
        alertContainer.appendChild(alert);
        alert.style.display = "block";

        // Ocultar la alerta después de 'duration' milisegundos
        setTimeout(function() {
            alert.style.display = "none";
        }, duration);
    }

    // JavaScript para validar el formulario y mostrar la alerta
    document.querySelector("#hidea-form").addEventListener("submit", function(event) {
        var form = document.querySelector("#hidea-form");
        var hasErrors = false;

        // Validar cada campo del formulario
        var inputs = form.querySelectorAll("input, select, textarea");
        inputs.forEach(function(input) {
            if (!input.value.trim()) { // Verificar si el campo está vacío
                hasErrors = true; // Indicar que hay errores
            }
        });

        // Mostrar alerta si hay errores
        if (hasErrors) {
            showAlert("Por favor complete todos los campos obligatorios.", 4000); // Mostrar alerta por 5 segundos
            event.preventDefault(); // Evitar envío del formulario si hay errores
        }
    });