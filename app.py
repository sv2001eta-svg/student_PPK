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
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO users (first_name, last_name, nickname, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (first_name, last_name, nickname, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({'success': True}) # Ответ для JS
        except Error as err:
            return jsonify({'success': False, 'error': str(err)})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
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

if __name__ == '__main__':
    app.run(debug=True)