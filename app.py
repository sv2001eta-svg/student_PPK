from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Замени на случайную строку!

# Настройки подключения к базе данных
db_config = {
    'host': 'vh464.timeweb.ru',
    'user': 'cc086496_maga2',
    'password': 'tEX22kha',
    'database': 'cc086496_maga2'
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
        nickname = request.form['username']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE nickname = %s", (nickname,))
            user = cursor.fetchone()
            conn.close()
            
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['nickname'] = user['nickname']
                return redirect(url_for('users_list'))
            else:
                flash('Неверный логин или пароль!')
        except Exception as e:
            print(f"Ошибка: {e}")
            flash('Ошибка авторизации')
    
    return render_template('avtorization.html')

# === РЕГИСТРАЦИЯ ===
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        try:
            print("🔍 Пытаюсь подключиться к БД...")
            conn = get_db_connection()
            print("✅ Подключение успешно!")
            
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
            flash("Ошибка регистрации")
        
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

# === ВЫХОД ===
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# === ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == '__main__':
    app.run(debug=True)