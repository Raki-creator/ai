
import os
import django
from django.core.management import call_command
from io import StringIO
import sys

# Configure settings to use PostgreSQL but force version and mock connection
from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',  # Doesn't matter, we will mock connection
        'PORT': '5432',
    }
}

if not settings.configured:
    settings.configure(
        DATABASES=DATABASES,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'api.apps.ApiConfig',
            'rest_framework',
            'rest_framework.authtoken',
            'corsheaders',
        ],
    )

django.setup()

# Set the version manually on the connection to avoid DB hit
from django.db import connections
connections['default'].features.interprets_empty_strings_as_nulls = False
# Monkeypatch the connection to avoid actual connect
from django.db.backends.postgresql.base import DatabaseWrapper
DatabaseWrapper.connect = lambda self: None
# Mock internal version check
DatabaseWrapper.pg_version = 170000 

def get_sql():
    all_sql = []
    from django.db.migrations.loader import MigrationLoader
    loader = MigrationLoader(connections['default'])
    
    apps = ['contenttypes', 'auth', 'admin', 'sessions', 'api', 'authtoken']
    
    for app in apps:
        # Get all migrations for this app in order
        app_nodes = [node for node in loader.graph.nodes if node[0] == app]
        # Sort migrations (basic alphabetical for now, loader would be better but this is usually fine for initial)
        app_nodes.sort() 
        
        for app_name, migration_name in app_nodes:
            print(f"Exporting {app_name} {migration_name}...")
            out = StringIO()
            try:
                call_command('sqlmigrate', app_name, migration_name, stdout=out)
                all_sql.append(f"-- MIGRATION: {app_name} {migration_name}\n")
                all_sql.append(out.getvalue())
                all_sql.append("\n")
            except Exception as e:
                print(f"  Error exporting {app_name} {migration_name}: {e}")

    with open("pg_migrations.sql", "w") as f:
        f.writelines(all_sql)
    print("Export complete: pg_migrations.sql")

if __name__ == "__main__":
    get_sql()
