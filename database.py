import sqlite3

def get_connection():
    conn = sqlite3.connect('assets.db')
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hardware (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            serial_number TEXT UNIQUE,
            status TEXT DEFAULT 'active',
            lab_id INTEGER,
            FOREIGN KEY (lab_id) REFERENCES labs(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT,
            license_key TEXT,
            hardware_id INTEGER,
            FOREIGN KEY (hardware_id) REFERENCES hardware(id)
        )
    ''')

    # Seed some labs
    cursor.execute("INSERT OR IGNORE INTO labs (name, location) VALUES ('Lab A', 'Building 1')")
    cursor.execute("INSERT OR IGNORE INTO labs (name, location) VALUES ('Lab B', 'Building 2')")
    cursor.execute("INSERT OR IGNORE INTO labs (name, location) VALUES ('Lab C', 'Building 3')")

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    initialize_db()