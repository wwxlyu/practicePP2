import psycopg2
import csv
import os
from config import load_config

class PhoneBookApp:
    def __init__(self):
        self.config = load_config()
        self.prepare_database()

    def prepare_database(self):
        commands = [
            #Таблица
            """
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20) NOT NULL
            );
            """,
            #Поиск
            """
            CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
            RETURNS TABLE (id INT, username VARCHAR, phone_number VARCHAR) AS $$
            BEGIN
                RETURN QUERY 
                SELECT * FROM phonebook 
                WHERE phonebook.username ILIKE '%' || pattern || '%' 
                   OR phonebook.phone_number LIKE '%' || pattern || '%';
            END;
            $$ LANGUAGE plpgsql;
            """,
            #Пагинация
            """
            CREATE OR REPLACE FUNCTION get_paginated_contacts(p_limit INT, p_offset INT)
            RETURNS TABLE (id INT, username VARCHAR, phone_number VARCHAR) AS $$
            BEGIN
                RETURN QUERY 
                SELECT * FROM phonebook 
                ORDER BY id 
                LIMIT p_limit OFFSET p_offset;
            END;
            $$ LANGUAGE plpgsql;
            """,
            #Upsert (Вставка или обновление по имени)
            """
            CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
            AS $$
            BEGIN
                INSERT INTO phonebook (username, phone_number)
                VALUES (p_name, p_phone)
                ON CONFLICT (username) 
                DO UPDATE SET phone_number = EXCLUDED.phone_number;
            END;
            $$ LANGUAGE plpgsql;
            """,
            #Удаление
            """
            CREATE OR REPLACE PROCEDURE delete_contact_proc(p_ident VARCHAR)
            AS $$
            BEGIN
                DELETE FROM phonebook WHERE username = p_ident OR phone_number = p_ident;
            END;
            $$ LANGUAGE plpgsql;
            """,
            #Процедура обновления (Update)
            """
            CREATE OR REPLACE PROCEDURE update_contact(p_target VARCHAR, p_new_value VARCHAR, p_mode INT)
            AS $$
            BEGIN
                -- mode 1: Обновить телефон по имени пользователя
                IF p_mode = 1 THEN
                    UPDATE phonebook SET phone_number = p_new_value WHERE username = p_target;
                -- mode 2: Обновить имя пользователя по номеру телефона
                ELSIF p_mode = 2 THEN
                    UPDATE phonebook SET username = p_new_value WHERE phone_number = p_target;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
            """
        ]
        
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                for cmd in commands:
                    cur.execute(cmd)
            conn.commit()
        print("Database is ready with all procedures.")

    def import_from_csv(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, filename)
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader) 
                for name, phone in reader:
                    self.upsert(name, phone)
            print("CSV imported successfully.")
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")

    def console_insert(self):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        self.upsert(name, phone)

    def upsert(self, name, phone):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
        print(f"Contact {name} processed.")

    #обновление
    def update(self, target, new_value, mode):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL update_contact(%s, %s, %s)", (target, new_value, mode))
            conn.commit()
        print(f"Update for {target} completed.")

    def search(self, text):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (text,))
                for row in cur.fetchall():
                    print(row)

    def delete(self, identifier):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact_proc(%s)", (identifier,))
            conn.commit()
        print(f"Contact {identifier} deleted.")

if __name__ == "__main__":
    app = PhoneBookApp()
    while True:
        print("\n1. Insert from Console\n2. Import from CSV\n3. Search\n4. Delete\n5. Update\n6. Exit")
        choice = input("Choose: ")
        
        if choice == '1':
            app.console_insert()
        elif choice == '2':
            app.import_from_csv('contacts.csv')
        elif choice == '3':
            s = input("Search for: ")
            app.search(s)
        elif choice == '4':
            ident = input("Enter name or phone to delete: ")
            app.delete(ident)
        elif choice == '5':
            print("1. Update phone by name\n2. Update name by phone")
            m = int(input("Choose mode: "))
            t = input("Enter target (name or phone): ")
            v = input("Enter new value: ")
            app.update(t, v, m)
        elif choice == '6':
            print("Goodbye!")
            break