"""
Schema Migration — refactor the legacy denormalized schema.
"""

import sqlite3


def create_legacy_schema(conn):
    """The OLD schema — denormalized, no indexes."""
    conn.execute('''
        CREATE TABLE IF NOT EXISTS legacy_orders (
            id INTEGER PRIMARY KEY,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone TEXT,
            product_name TEXT,
            product_price DECIMAL,
            quantity INTEGER,
            total DECIMAL,
            order_date DATE,
            status TEXT
        )
    ''')


def migrate_schema(conn):
    """Create the NEW normalized schema."""

    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            line_total DECIMAL(10,2) NOT NULL
        )
    ''')


def migrate_data(conn):
    """Move data from legacy_orders to new normalized tables."""

    # If same customer_email appears multiple times, it creates duplicates
    conn.execute('''
        INSERT INTO customers (name, email, phone)
        SELECT customer_name, customer_email, customer_phone
        FROM legacy_orders
    ''')

    conn.execute('''
        INSERT INTO products (name, price)
        SELECT product_name, product_price
        FROM legacy_orders
    ''')

    conn.commit()
