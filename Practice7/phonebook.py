import psycopg2
from config import load_config
import csv
import os

class PhoneBookApp:
    def __init__(self):
        #загрузка из database.ini через config.py
        self.config = load_config()
        self.prepare_database()

    def prepare_database(self):
        commands = [
            #создание табл
            """
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                phone_number VARCHAR(20) NOT NULL
            );
            """,
            #функция поиска 
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
            #функция для пагинации
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
            #Процедур Upsert (Insert or Update)
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
            #Процедура дилейт
            """
            CREATE OR REPLACE PROCEDURE delete_contact_proc(p_ident VARCHAR)
            AS $$
            BEGIN
                DELETE FROM phonebook WHERE username = p_ident OR phone_number = p_ident;
            END;
            $$ LANGUAGE plpgsql;
            """
        ]
        
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                for cmd in commands:
                    cur.execute(cmd)
            conn.commit()
        print("Бд готова.")

    def import_from_csv(self, filename):
        # Get the directory where phonebook.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Join it with the filename
        file_path = os.path.join(base_dir, filename)
        
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                next(reader) # skip header
                for name, phone in reader:
                    self.upsert(name, phone)
            print("CSV imported successfully.")
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found in {base_dir}")

    def console_insert(self):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        self.upsert(name, phone)
    def upsert(self, name, phone):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
        print(f"Contact {name} add/upd.")

    def search(self, text):
        print(f"\nresults of search '{text}':")
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (text,))
                for row in cur.fetchall():
                    print(row)

    def get_page(self, limit, offset):
        print(f"\nPage of data (limit {limit}, offset {offset}):")
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_paginated_contacts(%s, %s)", (limit, offset))
                for row in cur.fetchall():
                    print(row)

    def delete(self, identifier):
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact_proc(%s)", (identifier,))
            conn.commit()
        print(f"Comtact {identifier} deleted.")
if __name__ == "__main__":
       app = PhoneBookApp()
       while True:
        print("\n1. Insert from Console\n2. Import from CSV\n3. Search\n4. Delete\n5. Exit")
        choice = input("Choose: ")
        
        if choice == '1':
            app.console_insert()
        elif choice == '2':
            app.import_from_csv('contacts.csv')
        elif choice == '3':
            s = input("Search for: ")
            app.search(s)
        # и так далее...

"""if __name__ == "__main__":
    app = PhoneBookApp()
    
    #demo
    app.upsert("Ayzhamal", "87071112233")
    app.upsert("Ayzhamal", "87770000000") #Upd , because same name
    app.upsert("TestUser", "87001234567")
    
    app.search("Ayz")
    app.get_page(1, 0) #show only 1 
    app.delete("TestUser")"""