from flask import Flask, render_template, request, jsonify, g
import mysql.connector

app = Flask(__name__)

# Параметры БД (замените на свои от преподавателя)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'chat_db'
}

def get_db():
    """Получение соединения с БД"""
    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Закрытие соединения"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """Страница регистрации"""
    return render_template('Registration.html')

@app.route('/login')
def login():
    """Страница авторизации"""
    return render_template('avtorization.html')

@app.route('/user_registration', methods=['POST'])
def user_registration():
    """Регистрация пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        db.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user_avtorization', methods=['POST'])
def user_avtorization():
    """Авторизация пользователя"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        if user:
            return jsonify({'success': True, 'message': 'Вход выполнен'})
        else:
            return jsonify({'success': False, 'message': 'Неверные данные'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat')
def chat():
    """Чат с приветствием"""
    nickname = request.args.get('nickname', 'Гость')
    return f'{nickname}, добро пожаловать в чат!'

if __name__ == '__main__':
    app.run(debug=True)