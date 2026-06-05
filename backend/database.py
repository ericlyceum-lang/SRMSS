import sqlite3
from contextlib import contextmanager
from config import Config

DB_NAME = Config.DB_NAME

def get_db():
    """Get database connection with Row factory"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_context():
    """Context manager for database connections"""
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize database schema"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        );

        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            registration_no TEXT UNIQUE,
            type TEXT,
            capacity INTEGER,
            mileage INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            license_no TEXT UNIQUE,
            license_expiry TEXT,
            assigned_route TEXT
        );

        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY,
            route_name TEXT,
            start_point TEXT,
            end_point TEXT,
            distance_km REAL,
            path_geometry TEXT,
            stops TEXT
        );

        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY,
            route_id INTEGER,
            vehicle_id INTEGER,
            driver_id INTEGER,
            departure_time TEXT,
            recurrence TEXT DEFAULT 'Once',
            status TEXT DEFAULT 'Scheduled'
        );

        CREATE TABLE IF NOT EXISTS fuel_logs (
            id INTEGER PRIMARY KEY,
            vehicle_id INTEGER,
            date TEXT,
            liters REAL,
            cost REAL,
            status TEXT DEFAULT 'Pending'
        );

        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id INTEGER PRIMARY KEY,
            vehicle_id INTEGER,
            type TEXT,
            description TEXT,
            cost REAL
        );
    ''')
    
    # Migration: Add missing columns
    cursor.execute("PRAGMA table_info(routes)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'stops' not in columns:
        cursor.execute("ALTER TABLE routes ADD COLUMN stops TEXT")
    if 'path_geometry' not in columns:
        cursor.execute("ALTER TABLE routes ADD COLUMN path_geometry TEXT")

    cursor.execute("PRAGMA table_info(vehicles)")
    v_cols = [info[1] for info in cursor.fetchall()]
    if 'mileage' not in v_cols:
        cursor.execute("ALTER TABLE vehicles ADD COLUMN mileage INTEGER DEFAULT 0")

    cursor.execute("PRAGMA table_info(drivers)")
    d_cols = [info[1] for info in cursor.fetchall()]
    if 'license_expiry' not in d_cols:
        cursor.execute("ALTER TABLE drivers ADD COLUMN license_expiry TEXT")
    if 'assigned_route' not in d_cols:
        cursor.execute("ALTER TABLE drivers ADD COLUMN assigned_route TEXT")

    cursor.execute("PRAGMA table_info(schedules)")
    s_cols = [info[1] for info in cursor.fetchall()]
    if 'recurrence' not in s_cols:
        cursor.execute("ALTER TABLE schedules ADD COLUMN recurrence TEXT DEFAULT 'Once'")
    if 'status' not in s_cols:
        cursor.execute("ALTER TABLE schedules ADD COLUMN status TEXT DEFAULT 'Scheduled'")

    cursor.execute("PRAGMA table_info(fuel_logs)")
    f_cols = [info[1] for info in cursor.fetchall()]
    if 'status' not in f_cols:
        cursor.execute("ALTER TABLE fuel_logs ADD COLUMN status TEXT DEFAULT 'Pending'")
    if 'cost' not in f_cols:
        cursor.execute("ALTER TABLE fuel_logs ADD COLUMN cost REAL")

    cursor.execute("PRAGMA table_info(maintenance_logs)")
    m_cols = [info[1] for info in cursor.fetchall()]
    if 'cost' not in m_cols:
        cursor.execute("ALTER TABLE maintenance_logs ADD COLUMN cost REAL")

    # Seed default users
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'Administrator')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('super', 'super123', 'Supervisor')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('staff', 'staff123', 'Operational Staff')")
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized: {DB_NAME}")