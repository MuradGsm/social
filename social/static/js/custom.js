// custom.js
document.addEventListener('DOMContentLoaded', function() {
    // Пример: добавление обработчика событий для уведомлений
    const notificationDropdown = document.getElementById('navbarDropdown');
    notificationDropdown.addEventListener('click', function() {
        // Логика для загрузки уведомлений
        console.log('Уведомления загружены');
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.connected-buttons .btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            buttons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});
