import os
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['UPLOAD_FOLDER'] = 'static/avatars'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Путь к базе данных SQLite
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Создаёт подключение к SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Чтобы работать как с dictionary
        conn.execute("PRAGMA journal_mode=WAL")  # Для производительности
        conn.execute("PRAGMA foreign_keys=ON")  # Включаем внешние ключи
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def init_db():
    """Создаёт таблицы, если их нет"""
    conn = get_db_connection()
    if conn is None:
        print("❌ Не удалось подключиться к БД!")
        return
    
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            nickname TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            avatar TEXT DEFAULT NULL,
            last_seen DATETIME DEFAULT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            recipient_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (recipient_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

# Инициализируем БД при запуске
init_db()

class User(UserMixin):
    def __init__(self, id, nickname, first_name, last_name, avatar=None):
        self.id = id
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.avatar = avatar

@login_manager.user_loader
def load_user(user_id):
    """Загружает пользователя из БД по ID"""
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(
            id=user_data['id'],
            nickname=user_data['nickname'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            avatar=user_data['avatar']
        )
    return None


# === АВТОРИЗАЦИЯ ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Заполните все поля'})

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE nickname = ?", (username,))
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data and check_password_hash(user_data['password'], password):
                user = User(
                    id=user_data['id'],
                    nickname=user_data['nickname'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    avatar=user_data['avatar']
                )
                
                login_user(user, remember=True)
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET last_seen = datetime('now') WHERE id = ?", (user.id,))
                conn.commit()
                conn.close()
                
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Неверный логин или пароль'})
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
            
    return render_template('avtorization.html')


# === РЕГИСТРАЦИЯ ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        nickname = request.form.get('username')
        password = request.form.get('password')
        
        print(f"📝 Регистрация: {first_name} {last_name}, ник: {nickname}")
        
        if not all([first_name, last_name, nickname, password]):
            return jsonify({'success': False, 'error': 'Заполните все поля'})
        
        hashed_password = generate_password_hash(password)
        
        # Обработка аватарки
        avatar_filename = None
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                avatar_filename = f"{nickname}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename)
                file.save(filepath)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (first_name, last_name, nickname, password, avatar) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(sql, (first_name, last_name, nickname, hashed_password, avatar_filename))
            conn.commit()
            
            conn.close()
            return jsonify({'success': True})
            
        except sqlite3.IntegrityError as err:
            print(f"❌ ОШИБКА: Ник уже занят: {err}")
            return jsonify({'success': False, 'error': 'Этот ник уже занят'})
        except Exception as e:
            print(f"❌ ОБЩАЯ ОШИБКА: {e}")
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('Registration.html')


# === СПИСОК ПОЛЬЗОВАТЕЛЕЙ ===
@app.route('/users')
@login_required
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nickname, first_name, last_name, last_seen, avatar 
        FROM users 
        WHERE id != ?
    """, (current_user.id,))
    all_users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', 
                          users=all_users, 
                          current_user=current_user,
                          now=datetime.now())


# === ЧАТ С ПОЛЬЗОВАТЕЛЕМ ===
@app.route('/chat/<recipient_nickname>')
@login_required
def chat(recipient_nickname):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE nickname = ?", (recipient_nickname,))
    recipient = cursor.fetchone()
    
    if not recipient:
        return "Пользователь не найден", 404
    
    recipient_id = recipient['id']

    cursor.execute("""
        SELECT m.*, u.nickname as sender_nickname, u.avatar as sender_avatar
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id = ? AND m.recipient_id = ?) 
           OR (m.sender_id = ? AND m.recipient_id = ?) 
        ORDER BY m.timestamp DESC
        LIMIT 50
    """, (current_user.id, recipient_id, recipient_id, current_user.id))
    
    messages = cursor.fetchall()
    messages.reverse()
    
    conn.close()

    return render_template('chat.html', 
                           current_user=current_user, 
                           recipient=recipient, 
                           messages=messages,
                           sender_nickname=current_user.nickname)


# === ОТПРАВКА СООБЩЕНИЯ (API) ===
@app.route('/api/send_message', methods=['POST'])
@login_required
def send_message_api():
    data = request.get_json()
    message_text = data.get('message')
    recipient_id = data.get('recipient_id')

    if not message_text or not recipient_id:
        return jsonify({'success': False, 'message': 'Ошибка данных'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (?, ?, ?)"
        cursor.execute(sql, (current_user.id, recipient_id, message_text))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# === ПОЛУЧЕНИЕ НОВЫХ СООБЩЕНИЙ (JSON API) ===
@app.route('/api/get_messages')
@login_required
def get_messages_api():
    recipient_id = request.args.get('recipient_id')
    last_id = request.args.get('last_id', 0, type=int)

    if not recipient_id:
        return jsonify([])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.message_text, m.sender_id, u.nickname as sender_nickname,
                   m.timestamp as time
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.id > ?
              AND ((m.sender_id = ? AND m.recipient_id = ?) 
                   OR (m.sender_id = ? AND m.recipient_id = ?))
            ORDER BY m.id ASC
        """, (last_id, current_user.id, recipient_id, recipient_id, current_user.id))
        
        messages = cursor.fetchall()
        conn.close()
        
        # Форматируем время
        result = []
        for msg in messages:
            result.append({
                'id': msg['id'],
                'message_text': msg['message_text'],
                'sender_id': msg['sender_id'],
                'sender_nickname': msg['sender_nickname'],
                'time': msg['time']
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Ошибка get_messages: {e}")
        return jsonify([]), 500


# === HEARTBEAT (статус онлайн) ===
@app.route('/api/heartbeat', methods=['POST'])
@login_required
def heartbeat():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_seen = datetime('now') WHERE id = ?", (current_user.id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})


# === ВЫХОД ===
@app.route('/logout')
@login_required
def logout():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_seen = datetime('now') WHERE id = ?", (current_user.id,))
    conn.commit()
    conn.close()
    
    logout_user()
    return redirect('/login')


# === СТРАНИЦА ДЛЯ ПРЕПОДАВАТЕЛЯ ===
@app.route('/teacher-check')
def teacher_check():
    """Страница для проверки работы преподавателем"""
    return render_template('teacher_check.html')


# === ГЛАВНАЯ СТРАНИЦА ===
@app.route('/')
def index():
    return redirect(url_for('register'))


# === ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == '__main__':
    app.run(debug=True)