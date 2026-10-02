document.addEventListener("DOMContentLoaded", function () {

    // Auto-hide Bootstrap flash messages
    const alerts = document.querySelectorAll(
        '[data-auto-dismiss="true"]'
    );

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const closeButton = alert.querySelector(
                ".btn-close"
            );

            if (closeButton) {
                closeButton.click();
            }

        }, 4000);

    });


    // Confirmation before deleting posts/comments
    const confirmationForms = document.querySelectorAll(
        "form[data-confirm]"
    );

    confirmationForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const message = form.dataset.confirm;

            if (!window.confirm(message)) {
                event.preventDefault();
            }

        });

    });

});
