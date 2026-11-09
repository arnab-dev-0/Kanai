from app.memory.database import Database


database = Database()

print("Database initialized successfully!")
print("Database location:", database.db_path)

connection = database.get_connection()

tables = connection.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    """
).fetchall()

for table in tables:
    print(table["name"])

connection.close()