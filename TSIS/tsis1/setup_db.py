import psycopg2
from config import load_config

def setup_database():
    """Initialize database with schema, functions, and procedures"""
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("=== Setting up database ===\n")
        
        # Drop existing functions and procedures
        print("Cleaning up old functions/procedures...")
        try:
            cur.execute("DROP FUNCTION IF EXISTS search_contacts(TEXT) CASCADE")
            cur.execute("DROP FUNCTION IF EXISTS get_contacts_paginated(INTEGER, INTEGER) CASCADE")
            cur.execute("DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR) CASCADE")
            cur.execute("DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR) CASCADE")
            print("✓ Cleanup completed")
        except Exception as e:
            print(f"  Note: {e}")
        
        # Execute schema.sql
        print("\nCreating tables...")
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        print("✓ Tables created")
        
        # Execute functions.sql
        print("\nCreating functions...")
        with open('functions.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        print("✓ Functions created")
        
        # Execute procedures.sql
        print("\nCreating procedures...")
        with open('procedures.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        print("✓ Procedures created")
        
        cur.close()
        print("\n✅ Database setup completed successfully!")
        print("\nYou can now run: python phonebook.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("1. PostgreSQL is running")
        print("2. database.ini has correct credentials")
        print("3. All .sql files are in the same folder")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()