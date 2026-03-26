document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds to provide better UX
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        alerts.forEach(alert => {
            setTimeout(() => {
                if(typeof bootstrap !== 'undefined') {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } else {
                    alert.style.display = 'none';
                }
            }, 5000);
        });
    }
});
