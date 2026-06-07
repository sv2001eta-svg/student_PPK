import pymysql

db_config = {
    'host': 'vh464.timeweb.ru',
    'user': 'cc086496_maga2',
    'password': 'tEX22kha',
    'database': 'cc086496_maga2',
    'port': 3306,
    'connect_timeout': 15
}

print("🔍 Пытаюсь подключиться к базе данных...")
print(f"📋 Хост: {db_config['host']}")
print(f"📋 Пользователь: {db_config['user']}")
print(f"📋 База: {db_config['database']}")
print("=" * 50)

try:
    conn = pymysql.connect(**db_config)
    print("✅ УСПЕШНО! Подключение установлено!")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📊 Версия MySQL: {version[0]}")
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Таблицы в базе: {tables}")
    
    conn.close()
    print("✅ Подключение закрыто")
    
except Exception as e:
    print(f"❌ ОШИБКА ПОДКЛЮЧЕНИЯ:")
    print(f"   {e}")
    print(f"   Тип: {type(e).__name__}")