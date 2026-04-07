import psycopg2
import csv
from config import load_config

class PhoneBookApp:
    def __init__(self):
        self.config = load_config()
        self.prepare_database()

    def prepare_database(self):
        #Создаем таблицу, если её нет
        create_table = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(20) NOT NULL
        );
        """
        
        #Читаем SQL из внешних файлов
        with open('functions.sql', 'r') as f:
            functions_script = f.read()
        with open('procedures.sql', 'r') as f:
            procedures_script = f.read()

        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(create_table)
                cur.execute(functions_script)
                cur.execute(procedures_script)
            conn.commit()
        print("База данных и функции обновлены из SQL файлов.")

    def upsert(self, name, phone):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
        print(f"Контакт {name} добавлен/обновлен.")

    def bulk_insert(self, names, phones):
        print("\n--- Массовая вставка с валидацией ---")
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                #Вызываем функцию валидации
                cur.execute("SELECT * FROM insert_many_with_validation(%s, %s)", (names, phones))
                errors = cur.fetchall()
                if errors:
                    print("Ошибки в следующих данных:")
                    for err in errors:
                        print(f"Имя: {err[0]}, Телефон: {err[1]} (Неверный формат)")
                else:
                    print("Все данные успешно добавлены.")
            conn.commit()

    def search(self, text):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (text,))
                rows = cur.fetchall()
                for row in rows: print(row)

    def delete(self, identifier):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact_proc(%s)", (identifier,))
            conn.commit()
        print(f"Контакт {identifier} удален.")

if __name__ == "__main__":
    app = PhoneBookApp()
    
    while True:
        print("\n1. Ввод из консоли\n2. Массовая вставка (тест валидации)\n3. Поиск\n4. Удаление\n5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            app.upsert(input("Имя: "), input("Телефон: "))
        elif choice == '2':
            #Пример данных: Тест1 - ок, Тест2 - ошибка (буквы в телефоне)
            names = ["ValidUser", "InvalidUser"]
            phones = ["87071112233", "8707ERROR"]
            app.bulk_insert(names, phones)
        elif choice == '3':
            app.search(input("Что ищем: "))
        elif choice == '4':
            app.delete(input("Имя или телефон для удаления: "))
        elif choice == '5':
            break