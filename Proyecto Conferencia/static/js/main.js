// Funcionalidad para mensajes de alerta
document.addEventListener('DOMContentLoaded', function() {
    // Auto ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Inicializar todos los tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Inicializar todos los popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Funcionalidad para contador de caracteres en textareas
    const textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(function(textarea) {
        const maxLength = textarea.getAttribute('data-max-length');
        const counterElement = document.createElement('small');
        counterElement.classList.add('form-text', 'text-muted', 'character-counter');
        counterElement.textContent = `0/${maxLength} caracteres`;
        
        textarea.parentNode.insertBefore(counterElement, textarea.nextSibling);
        
        textarea.addEventListener('input', function() {
            const currentLength = textarea.value.length;
            counterElement.textContent = `${currentLength}/${maxLength} caracteres`;
            
            if (currentLength > maxLength) {
                counterElement.classList.add('text-danger');
            } else {
                counterElement.classList.remove('text-danger');
            }
        });
    });
    
    // Funcionalidad para confirmación de acciones
    const confirmForms = document.querySelectorAll('form[data-confirm]');
    confirmForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const confirmMessage = form.getAttribute('data-confirm');
            if (!confirm(confirmMessage)) {
                event.preventDefault();
            }
        });
    });
    
    // Funcionalidad para copiar al portapapeles
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const textToCopy = button.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(function() {
                // Cambiar temporalmente el texto del botón
                const originalText = button.textContent;
                button.textContent = '¡Copiado!';
                setTimeout(function() {
                    button.textContent = originalText;
                }, 2000);
            });
        });
    });
    
    // Inicializar contador para elementos con fecha límite
    const countdownElements = document.querySelectorAll('[data-countdown]');
    countdownElements.forEach(function(element) {
        const targetDate = new Date(element.getAttribute('data-countdown')).getTime();
        
        // Actualizar cada segundo
        const interval = setInterval(function() {
            const now = new Date().getTime();
            const distance = targetDate - now;
            
            // Cálculos de tiempo
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            // Mostrar resultado
            element.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
            
            // Si la cuenta regresiva termina
            if (distance < 0) {
                clearInterval(interval);
                element.innerHTML = "¡Evento iniciado!";
                element.classList.add('text-danger');
            }
        }, 1000);
    });
});