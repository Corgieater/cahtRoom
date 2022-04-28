import os
from dotenv import load_dotenv
from mysql.connector import pooling
from flask import Blueprint

model_blueprint = Blueprint(
    'model_blueprint',
    __name__,
)

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')


class Database:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name='pool',
            pool_size=5,
            pool_reset_session=True,
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

    def add_to_database(self, inputs):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO message VALUES (%s, %s, %s)', inputs)
        except Exception as e:
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()

    def get_old_data(self):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT message, imgName FROM message ORDER BY id DESC LIMIT 0, 5')
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            return results
        finally:
            cursor.close()
            connection.close()
