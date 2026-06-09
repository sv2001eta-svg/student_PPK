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
    
});
// ============================================
// УВЕДОМЛЕНИЯ О НОВЫХ СООБЩЕНИЯХ
// ============================================

// Звук уведомления (короткий "динь")
const notificationSound = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBTGH0fPTgjMGHm7A7+OZSA0PVqXh8bllHAU2jNn1unEiBC13yO/eizEIHWq+8+OZURE');

let lastMessageCount = 0;
let isTabActive = true;
let originalTitle = document.title;

// Отслеживание активности вкладки
document.addEventListener('visibilitychange', function() {
    isTabActive = !document.hidden;
    if (isTabActive) {
        document.title = originalTitle;
        // Сбросить favicon
        document.querySelector("link[rel*='icon']").href = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>";
    }
});

// Функция показа уведомления
function showNotification(message) {
    // Звук
    try {
        notificationSound.play();
    } catch(e) {
        console.log('Звук не воспроизведён');
    }
    
    // Всплывающее уведомление браузера
    if (Notification.permission === 'granted' && !isTabActive) {
        new Notification('Новое сообщение', {
            body: message,
            icon: '💬'
        });
    }
    
    // Мигание вкладки
    if (!isTabActive) {
        let blinkCount = 0;
        let blinkInterval = setInterval(() => {
            document.title = blinkCount % 2 === 0 ? '🔔 Новое сообщение!' : originalTitle;
            blinkCount++;
            if (blinkCount > 6) {
                clearInterval(blinkInterval);
                document.title = originalTitle;
            }
        }, 1000);
    }
}

// Запрос разрешения на уведомления
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Модифицируем функцию загрузки сообщений (добавь это в существующую функцию loadMessages)
// Найди функцию loadMessages и добавь проверку новых сообщений

const originalLoadMessages = loadMessages;
loadMessages = function() {
    fetch(`/api/get_messages/${otherUserId}`)
        .then(response => response.json())
        .then(data => {
            const messagesContainer = document.getElementById('messages');
            const currentCount = data.messages.length;
            
            // Если есть новые сообщения и это не первая загрузка
            if (currentCount > lastMessageCount && lastMessageCount > 0) {
                const newMessage = data.messages[data.messages.length - 1];
                if (newMessage.sender_id !== currentUserId) {
                    showNotification(`${newMessage.sender_name}: ${newMessage.message}`);
                }
            }
            
            lastMessageCount = currentCount;
            
            // Обновляем отображение сообщений
            messagesContainer.innerHTML = '';
            data.messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = msg.sender_id === currentUserId ? 'message sent' : 'message received';
                messageDiv.innerHTML = `
                    <div class="message-content">${msg.message}</div>
                    <div class="message-time">${msg.created_at}</div>
                `;
                messagesContainer.appendChild(messageDiv);
            });
            
            // Прокрутка вниз
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
};
// ============================================
// СТАТУС ОНЛАЙН (Heartbeat)
// ============================================

// Обновляем статус каждые 30 секунд
setInterval(() => {
    fetch('/api/heartbeat', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Статус обновлён:', data.status);
        })
        .catch(error => {
            console.log('Ошибка обновления статуса:', error);
        });
}, 30000); // 30 секунд

// Обновить сразу при загрузке страницы
fetch('/api/heartbeat', { method: 'POST' });