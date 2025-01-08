document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert.fade.show');
    messages.forEach(message => {
        message.classList.add('fade-out');
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(message);
            bsAlert.close();
        }, 3000);
    });
});