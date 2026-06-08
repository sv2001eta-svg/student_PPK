from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

db_config = {
    'host': 'vh464.timeweb.ru',
    'user': 'cc086496_maga2',
    'password': 'tEX22kha',
    'database': 'cc086496_maga2',
    'use_pure': True  # <--- ДОБАВЬ ЭТУ СТРОКУ!
}


def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

# === АВТОРИЗАЦИЯ ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Заполните все поля'})

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            # Ищем пользователя по нику
            cursor.execute("SELECT * FROM users WHERE nickname = %s", (username,))
            user = cursor.fetchone()
            conn.close()
            
            # Проверяем пароль
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['nickname'] = user['nickname']
                # Возвращаем успешный ответ для JS
                return jsonify({'success': True})
            else:
                # Возвращаем ошибку с текстом
                return jsonify({'success': False, 'message': 'Неверный логин или пароль'})
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
            
    # Если запрос GET, просто показываем страницу входа
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
        print(f"🔐 Хеш пароля: {hashed_password[:20]}...")
        
        try:
            print("🔍 Подключаюсь к БД...")
            conn = get_db_connection()
            
            if not conn:
                print("❌ Не удалось подключиться к БД")
                return jsonify({'success': False, 'error': 'Ошибка подключения к базе данных'})
            
            print("✅ Подключение к БД успешно")
            cursor = conn.cursor()
            
            sql = "INSERT INTO users (first_name, last_name, nickname, password) VALUES (%s, %s, %s, %s)"
            print(f"📝 Выполняю запрос: {sql}")
            print(f"   Данные: ({first_name}, {last_name}, {nickname}, {hashed_password})")
            
            cursor.execute(sql, (first_name, last_name, nickname, hashed_password))
            conn.commit()
            print(f"✅ Пользователь {nickname} зарегистрирован! ID: {cursor.lastrowid}")
            
            conn.close()
            return jsonify({'success': True})
            
        except mysql.connector.Error as err:
            print(f"❌ ОШИБКА MySQL: {err}")
            print(f"   Код ошибки: {err.errno}")
            return jsonify({'success': False, 'error': f'Ошибка БД: {err}'})
        except Exception as e:
            print(f"❌ ОБЩАЯ ОШИБКА: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)})
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()
                print("✅ Соединение закрыто")
    
    return render_template('Registration.html')

# === СПИСОК ПОЛЬЗОВАТЕЛЕЙ ===
@app.route('/users')
def users_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nickname, first_name, last_name FROM users WHERE id != %s", (session['user_id'],))
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users, current_user=session['nickname'])

# === ЧАТ С ПОЛЬЗОВАТЕЛЕМ ===  ← ВСТАВЬ СЮДА
@app.route('/chat/<recipient_nickname>')
def chat(recipient_nickname):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE nickname = %s", (recipient_nickname,))
    recipient = cursor.fetchone()
    
    if not recipient:
        return "Пользователь не найден", 404
    
    recipient_id = recipient['id']

    cursor.execute("""
        SELECT m.*, u.nickname as sender_nickname 
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id = %s AND m.recipient_id = %s) 
           OR (m.sender_id = %s AND m.recipient_id = %s) 
        ORDER BY m.timestamp ASC
    """, (current_user_id, recipient_id, recipient_id, current_user_id))
    
    messages = cursor.fetchall()
    conn.close()

    return render_template('chat.html', 
                           current_user=session['nickname'], 
                           recipient=recipient, 
                           messages=messages)

# === ОТПРАВКА СООБЩЕНИЯ (API) ===
@app.route('/api/send_message', methods=['POST'])
def send_message_api():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Не авторизован'}), 401

    data = request.get_json()
    message_text = data.get('message')
    recipient_id = data.get('recipient_id')
    sender_id = session['user_id']

    if not message_text or not recipient_id:
        return jsonify({'success': False, 'message': 'Ошибка данных'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO messages (sender_id, recipient_id, message_text) VALUES (%s, %s, %s)"
        cursor.execute(sql, (sender_id, recipient_id, message_text))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# === ВЫХОД ===
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# === ГЛАВНАЯ СТРАНИЦА ===
@app.route('/')
def index():
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)