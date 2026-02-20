
import os
import sys
from unittest.mock import MagicMock

# Mock psycopg2 before Django loads it
mock_psycopg2 = MagicMock()
mock_psycopg2.__version__ = '2.9.9'
sys.modules['psycopg2'] = mock_psycopg2
sys.modules['psycopg2.extensions'] = MagicMock()
sys.modules['psycopg2.extras'] = MagicMock()
sys.modules['psycopg2.errors'] = MagicMock()

# Mock the connection and cursor
mock_conn = MagicMock()
mock_psycopg2.connect.return_value = mock_conn
mock_cursor = MagicMock()
mock_conn.cursor.return_value = mock_cursor

# Django needs to check version
mock_cursor.fetchone.return_value = ['PostgreSQL 17.0']

import django
from django.core.management import call_command
from io import StringIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

apps = ['admin', 'auth', 'contenttypes', 'sessions', 'api', 'authtoken']

def get_sql():
    all_sql = []
    # We need to get the list of migrations for each app
    from django.db.migrations.loader import MigrationLoader
    from django.db import connections
    loader = MigrationLoader(connections['default'])
    
    # Filter for migrations we care about
    for app in apps:
        app_migrations = [m[1] for m in loader.graph.leaf_nodes() if m[0] == app]
        # This only gets leaf nodes, we need all migrations in order
        # Actually loader.graph.forwards_plan( (app, migration) ) is better
        
        # Simpler way: just iterate all nodes in the graph
        for node in loader.graph.nodes:
            if node[0] == app:
                migration_name = node[1]
                print(f"Exporting {app} {migration_name}...")
                out = StringIO()
                try:
                    call_command('sqlmigrate', app, migration_name, stdout=out)
                    all_sql.append(f"-- MIGRATION: {app} {migration_name}\n")
                    all_sql.append(out.getvalue())
                    all_sql.append("\n")
                except Exception as e:
                    print(f"  Error: {e}")

    with open("pg_migrations.sql", "w") as f:
        f.writelines(all_sql)
    print("Export complete: pg_migrations.sql")

if __name__ == "__main__":
    get_sql()
