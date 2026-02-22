import pytest, sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from migration import create_legacy_schema, migrate_schema

class TestMigration:
    @pytest.fixture
    def conn(self):
        c = sqlite3.connect(':memory:')
        yield c
        c.close()

    def test_customers_unique_email(self, conn):
        migrate_schema(conn)
        info = conn.execute("PRAGMA index_list(customers)").fetchall()
        unique_indexes = [i for i in info if i[2] == 1]  # is_unique
        assert len(unique_indexes) > 0, "customers.email should have UNIQUE constraint"

    def test_orders_has_foreign_key(self, conn):
        migrate_schema(conn)
        fks = conn.execute("PRAGMA foreign_key_list(orders)").fetchall()
        assert len(fks) > 0, "orders table should have foreign key to customers"

    def test_orders_has_index(self, conn):
        migrate_schema(conn)
        indexes = conn.execute("PRAGMA index_list(orders)").fetchall()
        assert len(indexes) > 0, "orders should have index on customer_id"
