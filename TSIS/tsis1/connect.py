import psycopg2
from config import load_config

def get_connection():
    """
    Создает и возвращает соединение с базой данных PostgreSQL,
    используя параметры из конфигурационного файла.
    """
    params = load_config()
    # Устанавливаем соединение
    conn = psycopg2.connect(**params)
    return conn

if __name__ == '__main__':
    # Проверка подключения
    try:
        connection = get_connection()
        print("✅ Подключение к базе данных установлено успешно!")
        connection.close()
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")