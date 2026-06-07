$(document).ready(function() {
    
    // Обработка формы регистрации
    $('#registrationForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            username: $('#username').val(),
            password: $('#password').val()
        };
        
        $.ajax({
            url: '/register',
            method: 'POST',
            data: formData,
            success: function(response) {
                alert('Регистрация успешна! Теперь войдите.');
                window.location.href = '/login';
            },
            error: function(xhr) {
                const error = xhr.responseJSON ? xhr.responseJSON.error : 'Ошибка регистрации';
                alert('Ошибка: ' + error);
            }
        });
    });
    
        // Обработка формы авторизации
    $('#authorizationForm').on('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        
        $.ajax({
            url: '/login',
            method: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    window.location.href = '/users';
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