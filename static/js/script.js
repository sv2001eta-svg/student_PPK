$(document).ready(function() {
    
    // Обработка формы регистрации
    $('#registrationForm').on('submit', function(e) {
        e.preventDefault(); // Предотвращаем стандартную отправку
        
        const formData = {
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            username: $('#username').val(),
            password: $('#password').val()
        };
        
        $.ajax({
    url: '/register',
    method: 'POST',
    data: formData,  // ← Убрано JSON.stringify
    success: function(response) {
                alert('Регистрация успешна! Теперь войдите.');
                window.location.href = '/login'; // Перенаправление на вход
            },
            error: function(xhr) {
                const error = xhr.responseJSON ? xhr.responseJSON.error : 'Ошибка регистрации';
                alert('Ошибка: ' + error);
            }
        });
    });
    
    // Обработка формы авторизации
    $('#authorizationForm').on('submit', function(e) {
        e.preventDefault(); // Предотвращаем стандартную отправку
        
        const formData = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        
        $.ajax({
            url: '/user_avtorization',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                if (response.success) {
                    // Перенаправление на чат с никнеймом
                    window.location.href = '/chat?nickname=' + formData.username;
                } else {
                    alert('Ошибка: ' + response.message);
                }
            },
            error: function(xhr) {
                const error = xhr.responseJSON ? xhr.responseJSON.error : 'Ошибка авторизации';
                alert('Ошибка: ' + error);
            }
        });
    });
    
});