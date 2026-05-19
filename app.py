import sqlite3
from tabulate import tabulate
from database import get_connection, initialize_db

def add_hardware():
    name = input("Device name: ")
    type_ = input("Type (laptop/server/monitor/other): ")
    serial = input("Serial number: ")
    
    conn = get_connection()
    labs = conn.execute("SELECT * FROM labs").fetchall()
    print("\nAvailable labs:")
    print(tabulate(labs, headers=labs[0].keys() if labs else []))
    lab_id = int(input("\nLab ID: "))
    
    conn.execute(
        "INSERT INTO hardware (name, type, serial_number, lab_id) VALUES (?, ?, ?, ?)",
        (name, type_, serial, lab_id)
    )
    conn.commit()
    conn.close()
    print(f"✓ {name} added successfully.")

def add_software():
    conn = get_connection()
    hardware = conn.execute("SELECT h.id, h.name, l.name as lab FROM hardware h JOIN labs l ON h.lab_id = l.id").fetchall()
    print("\nAvailable hardware:")
    print(tabulate(hardware, headers=hardware[0].keys() if hardware else []))
    
    hw_id = int(input("\nHardware ID to assign software to: "))
    name = input("Software name: ")
    version = input("Version: ")
    license_key = input("License key (optional, press Enter to skip): ")
    
    conn.execute(
        "INSERT INTO software (name, version, license_key, hardware_id) VALUES (?, ?, ?, ?)",
        (name, version, license_key or None, hw_id)
    )
    conn.commit()
    conn.close()
    print(f"✓ {name} added successfully.")

def view_all_assets():
    conn = get_connection()
    results = conn.execute('''
        SELECT h.id, h.name, h.type, h.serial_number, h.status,
               l.name as lab, l.location,
               GROUP_CONCAT(s.name || ' v' || s.version, ', ') as software
        FROM hardware h
        LEFT JOIN labs l ON h.lab_id = l.id
        LEFT JOIN software s ON s.hardware_id = h.id
        GROUP BY h.id
    ''').fetchall()
    conn.close()
    
    if not results:
        print("No assets found.")
        return
    print("\n" + tabulate(results, headers=results[0].keys()))

def search_assets():
    term = input("Search by name or serial number: ")
    conn = get_connection()
    results = conn.execute('''
        SELECT h.id, h.name, h.type, h.serial_number, h.status, l.name as lab
        FROM hardware h
        LEFT JOIN labs l ON h.lab_id = l.id
        WHERE h.name LIKE ? OR h.serial_number LIKE ?
    ''', (f'%{term}%', f'%{term}%')).fetchall()
    conn.close()
    
    if not results:
        print("No results found.")
        return
    print("\n" + tabulate(results, headers=results[0].keys()))

def update_status():
    view_all_assets()
    hw_id = int(input("\nHardware ID to update: "))
    status = input("New status (active/inactive/maintenance/retired): ")
    
    conn = get_connection()
    conn.execute("UPDATE hardware SET status = ? WHERE id = ?", (status, hw_id))
    conn.commit()
    conn.close()
    print("✓ Status updated.")

def delete_asset():
    view_all_assets()
    hw_id = int(input("\nHardware ID to delete: "))
    confirm = input(f"Are you sure? (yes/no): ")
    if confirm.lower() == 'yes':
        conn = get_connection()
        conn.execute("DELETE FROM software WHERE hardware_id = ?", (hw_id,))
        conn.execute("DELETE FROM hardware WHERE id = ?", (hw_id,))
        conn.commit()
        conn.close()
        print("✓ Asset deleted.")

def lab_report():
    conn = get_connection()
    results = conn.execute('''
        SELECT l.name as lab, l.location,
               COUNT(h.id) as total_devices,
               SUM(CASE WHEN h.status = 'active' THEN 1 ELSE 0 END) as active,
               SUM(CASE WHEN h.status = 'inactive' THEN 1 ELSE 0 END) as inactive,
               SUM(CASE WHEN h.status = 'maintenance' THEN 1 ELSE 0 END) as maintenance
        FROM labs l
        LEFT JOIN hardware h ON h.lab_id = l.id
        GROUP BY l.id
    ''').fetchall()
    conn.close()
    print("\n" + tabulate(results, headers=results[0].keys()))

def main():
    initialize_db()
    while True:
        print("\n=== IT Asset Management System ===")
        print("1. Add hardware asset")
        print("2. Add software to hardware")
        print("3. View all assets")
        print("4. Search assets")
        print("5. Update asset status")
        print("6. Delete asset")
        print("7. Lab report")
        print("0. Exit")
        
        choice = input("\nChoice: ")
        
        if choice == '1': add_hardware()
        elif choice == '2': add_software()
        elif choice == '3': view_all_assets()
        elif choice == '4': search_assets()
        elif choice == '5': update_status()
        elif choice == '6': delete_asset()
        elif choice == '7': lab_report()
        elif choice == '0': break
        else: print("Invalid choice.")

if __name__ == '__main__':
    main()