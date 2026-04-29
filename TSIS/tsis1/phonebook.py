import json
import os
from datetime import datetime

import psycopg2
import psycopg2.extras
from connect import get_connection

# Helper functions
def _conn():
    return get_connection()

def _fmt_date(d):
    return d.strftime("%d.%m.%Y") if d else "--"

def _parse_date(s):
    s = (s or "").strip()
    if not s: 
        return None
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def _print_contacts(rows):
    if not rows:
        print("  No contacts found")
        return
    print("-" * 80)
    for r in rows:
        bday = _fmt_date(r.get('birthday'))
        group = r.get('group_name') or "No group"
        phones = r.get('phones', '')
        print(f" [{r['id']}] {r['first_name']} {r.get('last_name', '')} | Email: {r.get('email') or '--'} | Birthday: {bday} | Group: {group}")
        if phones:
            print(f"      Phones: {phones}")
    print("-" * 80)

def _get_groups():
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, name FROM groups ORDER BY name")
            return cur.fetchall()

# Main functions
def add_contact_manual():
    print("\n--- Add New Contact ---")
    name = input("First Name: ").strip()
    last_name = input("Last Name (optional): ").strip() or None
    email = input("Email: ").strip() or None
    bday_str = input("Birthday (DD-MM-YYYY): ").strip()
    bday = _parse_date(bday_str)
    
    groups = _get_groups()
    print("\nAvailable groups:")
    for g in groups:
        print(f"  {g['id']}. {g['name']}")
    
    group_id = input("Group ID (or press Enter for none): ").strip()
    group_id = int(group_id) if group_id.isdigit() else None
    
    with _conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, email, birthday, group_id) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (name, last_name, email, bday, group_id))
            contact_id = cur.fetchone()[0]
            
            while True:
                add_phone = input("Add phone number? (y/n): ").strip().lower()
                if add_phone != 'y':
                    break
                phone = input("Phone number: ").strip()
                print("Phone types: home, work, mobile")
                ptype = input("Type (default mobile): ").strip() or "mobile"
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone, ptype)
                )
        conn.commit()
    print("Contact added successfully!")

def search_and_filter():
    print("\n--- Search Contacts ---")
    search = input("Search (name, email, or phone): ").strip()
    
    groups = _get_groups()
    print("\nFilter by group (optional):")
    print("  0. All groups")
    for g in groups:
        print(f"  {g['id']}. {g['name']}")
    group_filter = input("Select group ID (or 0): ").strip()
    group_filter = int(group_filter) if group_filter.isdigit() else 0
    
    print("\nSort by:")
    print("  1. Name")
    print("  2. Birthday")
    print("  3. Date added")
    sort_choice = input("Choose sort (1-3): ").strip()
    
    sort_map = {
        '1': 'c.first_name',
        '2': 'c.birthday NULLS LAST',
        '3': 'c.created_at DESC'
    }
    order_by = sort_map.get(sort_choice, 'c.first_name')
    
    page = 0
    page_size = 5
    
    while True:
        offset = page * page_size
        
        with _conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                query = """
                    SELECT DISTINCT 
                        c.id, c.first_name, c.last_name, c.email, c.birthday, 
                        COALESCE(g.name, 'No group') as group_name,
                        STRING_AGG(DISTINCT p.phone || ' (' || p.type || ')', ', ') as phones
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                    LEFT JOIN phones p ON c.id = p.contact_id
                    WHERE (c.first_name ILIKE %s OR c.last_name ILIKE %s 
                           OR c.email ILIKE %s OR p.phone ILIKE %s)
                """
                params = [f'%{search}%', f'%{search}%', f'%{search}%', f'%{search}%']
                
                if group_filter > 0:
                    query += " AND c.group_id = %s"
                    params.append(group_filter)
                
                query += f" GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name"
                query += f" ORDER BY {order_by} LIMIT %s OFFSET %s"
                params.extend([page_size, offset])
                
                cur.execute(query, params)
                rows = cur.fetchall()
        
        print(f"\n-- Page {page + 1} --")
        _print_contacts(rows)
        
        if not rows:
            print("No more contacts found.")
            break
        
        cmd = input("[n] Next, [p] Previous, [q] Quit: ").strip().lower()
        if cmd == 'n' and len(rows) == page_size:
            page += 1
        elif cmd == 'p' and page > 0:
            page -= 1
        elif cmd == 'q':
            break

def export_json():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "contacts_export.json")
    
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    c.first_name as name,
                    c.last_name,
                    c.email,
                    c.birthday,
                    g.name as group,
                    JSON_AGG(json_build_object('phone', p.phone, 'type', p.type)) as phones
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            """)
            rows = cur.fetchall()
    
    for r in rows:
        if r['birthday']:
            r['birthday'] = r['birthday'].isoformat()
        if not r['phones']:
            r['phones'] = []
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Data exported to {path}")

def import_json():
    path = input("Path to JSON file [contacts_import.json]: ").strip() or "contacts_import.json"
    
    if os.path.isdir(path):
        path = os.path.join(path, "contacts_import.json")
    
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        imported = 0
        skipped = 0
        
        with _conn() as conn:
            with conn.cursor() as cur:
                for item in data:
                    if item.get('email'):
                        cur.execute("SELECT id FROM contacts WHERE email = %s", (item.get('email'),))
                        if cur.fetchone():
                            print(f"  - Skipped (duplicate email): {item.get('email')}")
                            skipped += 1
                            continue
                    
                    bday = _parse_date(item.get('birthday'))
                    cur.execute("""
                        INSERT INTO contacts (first_name, last_name, email, birthday) 
                        VALUES (%s, %s, %s, %s) RETURNING id
                    """, (
                        item.get('name'),
                        item.get('last_name'),
                        item.get('email'),
                        bday
                    ))
                    contact_id = cur.fetchone()[0]
                    
                    phones = item.get('phones', [])
                    for phone_data in phones:
                        if isinstance(phone_data, dict):
                            cur.execute(
                                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (contact_id, phone_data.get('phone'), phone_data.get('type', 'mobile'))
                            )
                        elif isinstance(phone_data, str):
                            cur.execute(
                                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                                (contact_id, phone_data, 'mobile')
                            )
                    
                    print(f"  + Imported: {item.get('name')} {item.get('last_name', '')}")
                    imported += 1
            conn.commit()
        
        print(f"Import completed. Imported: {imported}, Skipped: {skipped}")
    except Exception as e:
        print(f"Error reading file: {e}")

def use_procedure_add_phone():
    print("\n--- Add Phone to Existing Contact ---")
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    print("Phone types: home, work, mobile")
    ptype = input("Type (default mobile): ").strip() or "mobile"
    
    with _conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.callproc('add_phone', (name, phone, ptype))
                conn.commit()
                print("Phone added successfully!")
            except Exception as e:
                print(f"Error: {e}")

def use_procedure_move_to_group():
    print("\n--- Move Contact to Group ---")
    name = input("Contact name: ").strip()
    group_name = input("Group name: ").strip()
    
    with _conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.callproc('move_to_group', (name, group_name))
                conn.commit()
                print("Contact moved to group successfully!")
            except Exception as e:
                print(f"Error: {e}")

def use_search_function():
    print("\n--- Global Search (Using Stored Function) ---")
    query = input("Enter search term: ").strip()
    
    if not query:
        print("No search term entered.")
        return
    
    try:
        with _conn() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (query,))
                rows = cur.fetchall()
        
        if rows:
            print(f"\nFound {len(rows)} contact(s):")
            _print_contacts(rows)
        else:
            print("No contacts found.")
    except Exception as e:
        print(f"Error during search: {e}")

# Main menu
MENU = """
1. Add Contact
2. Search & Filter (with pagination)
3. Export to JSON
4. Import from JSON
5. Add Phone to Contact (Procedure)
6. Move Contact to Group (Procedure)
7. Global Search (Function)
8. Exit
"""

def main():
    while True:
        print(MENU)
        choice = input("Select action: ")
        
        if choice == "1":
            add_contact_manual()
        elif choice == "2":
            search_and_filter()
        elif choice == "3":
            export_json()
        elif choice == "4":
            import_json()
        elif choice == "5":
            use_procedure_add_phone()
        elif choice == "6":
            use_procedure_move_to_group()
        elif choice == "7":
            use_search_function()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()