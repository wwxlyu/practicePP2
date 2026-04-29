import psycopg2
from config import load_config

def get_connection():
    params = load_config()
    conn = psycopg2.connect(**params)
    return conn

if __name__ == '__main__':
    try:
        connection = get_connection()
        print(" Подключение к базе данных установлено успешно!")
        connection.close()
    except Exception as e:
        print(f"Ошибка подключения: {e}")