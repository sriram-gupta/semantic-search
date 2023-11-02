import mysql.connector
import pymysql
import os

# Create a MySQL connection
dbClient = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE'),
    )

# Export 'create_mysql_connection' function to be used in other files
__all__ = ['dbClient']