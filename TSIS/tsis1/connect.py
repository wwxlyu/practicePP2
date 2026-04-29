import psycopg2
from config import load_config

def get_connection():
    params = load_config()
    conn = psycopg2.connect(**params)
    return conn

if __name__ == '__main__':
    try:
        connection = get_connection()
        print(" Succesful!")
        connection.close()
    except Exception as e:
        print(f"Error: {e}")