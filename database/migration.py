from connection import Database, CreateDatabase
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Manage database tables.')
parser.add_argument('operation', choices=[
                    'create_database', 'create_table', 'drop'], help='The operation to perform.')
# optional arguments
parser.add_argument('--table', help='The name of the table to operate on.')
args = parser.parse_args()

# command-line arguments
# create database
# python migration.py create_database

# create table users
# python migration.py create_table --table users
# drop table users
# python migration.py drop --table users

# create table attendance
# python migration.py create_table --table attendance
# drop table attendance
# python migration.py drop --table attendance

def connection():
    try:
        db = Database(
            db_name="attendance_webapp",
            user="postgres",
            password="sundaya2023",
            host="localhost",
            port=5432
        )
        return db
    except Exception as e:
        print(e)
        return False

def create_table():
    # database connection
    db = connection()
    try:
        if args.table == 'users':
            # table users
            db.create_table(
                table_name="users",
                columns='id SERIAL PRIMARY KEY, npm VARCHAR, nama_lengkap VARCHAR, foto VARCHAR, "createdAt" TIMESTAMP DEFAULT NOW()',
            )
        
        if args.table == 'attendance':
            # table absensi
            db.create_table(
                table_name="attendance",
                columns='id SERIAL PRIMARY KEY, npm VARCHAR, tanggal_absen VARCHAR, foto VARCHAR, "createdAt" TIMESTAMP DEFAULT NOW()',
            )
    except Exception as e:
        print(e)
        return False

def drop_table():
    # database connection
    db = connection()
    try:
        db.drop_table(table_name=args.table)
    except Exception as e:
        print(e)
        return False

def create_database():
    db = CreateDatabase(
        user="postgres",
        password="sundaya2023",
        host="localhost",
        port=5432
    )
    db.create_database(db_name="attendance_webapp")


# Perform operation
if args.operation == 'create_database':
    create_database()
if args.operation == 'create_table':
    create_table()
elif args.operation == 'drop':
    drop_table()
