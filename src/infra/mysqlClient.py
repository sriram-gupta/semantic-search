import mysql.connector
import os

# Create a MySQL connection
dbClient = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'),
    )

# Export 'create_mysql_connection' function to be used in other files
__all__ = ['dbClient']