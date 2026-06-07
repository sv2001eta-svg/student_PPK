from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions' # Ключ для сессий

# 🔧 НАСТРОЙКИ БАЗЫ ДАННЫХ
db_config = {
    'host': 'vh464.timeweb.ru',  # Если база на удаленном сервере, тут будет IP
    'user': 'cc086496_maga2',
'password': 'tEX22kha',
'database': 'cc086496_maga2'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# === ГЛАВНАЯ СТРАНИЦА ===
@app.route('/')
def index():
    return redirect(url_for('login'))

# === АВТОРИЗАЦИЯ ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE nickname = %s", (username,))
        user = cursor.fetchone()
        
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['nickname'] = user['nickname']
            return redirect(url_for('users_list')) # Переход к списку юзеров
        else:
            flash('Неверный логин или пароль!')
            
    return render_template('avtorization.html')

# === РЕГИСТРАЦИЯ ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['username']  # ← Исправлено!
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
try:
    print(f"🔍 Пытаюсь подключиться к БД...")
    conn = get_db_connection()
    print(f"✅ Подключение успешно!")
    
    cursor = conn.cursor()
    sql = "INSERT INTO users (first_name, last_name, nickname, password) VALUES (%s, %s, %s, %s)"
    print(f"📝 Выполняю запрос: {sql}")
    
    cursor.execute(sql, (first_name, last_name, nickname, hashed_password))
    conn.commit()
    print(f"✅ Пользователь {nickname} зарегистрирован!")
    
    return redirect(url_for('login'))
    
except mysql.connector.Error as err:
    print(f"❌ ОШИБКА БАЗЫ ДАННЫХ: {err}")
    flash(f"Ошибка: {err}")
    
except Exception as e:
    print(f"❌ ОБЩАЯ ОШИБКА: {e}")
    flash(f"Ошибка регистрации")
    
finally:
    # ← ЭТО ВАЖНО! Закрываем соединение в любом случае
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("✅ Соединение закрыто")
    
return render_template('Registration.html')

# === СПИСОК ПОЛЬЗОВАТЕЛЕЙ (ТВОЯ НОВАЯ ЗАДАЧА) ===
@app.route('/users')
def users_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Берем всех, кроме себя
    cursor.execute("SELECT id, nickname, first_name, last_name FROM users WHERE id != %s", (session['user_id'],))
    users = cursor.fetchall()
    conn.close()
    
    return render_template('users.html', users=users, current_user=session['nickname'])

# === ВЫХОД ===
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)