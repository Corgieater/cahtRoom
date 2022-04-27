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

    def get_newest_data_from_database(self):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT message, imgName FROM message ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            cursor.close()
            connection.close()

    def get_old_data(self, start_point):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT message, imgName FROM message ORDER BY id DESC LIMIT %s, 5', (start_point,))
            # 越新的留言越先貼 %s從0開始
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            return results
        finally:
            cursor.close()
            connection.close()


# pool = pooling.MySQLConnectionPool(
#         pool_name='pool',
#         pool_size=5,
#         pool_reset_session=True,
#         host=MYSQL_HOST,
#         database=MYSQL_DATABASE,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD
#     )


# def add_to_database(sql, inputs):
#     cnt = pool.get_connection()
#     cursor = cnt.cursor()
#     try:
#         cursor.execute(sql, inputs)
#
#     except Exception as e:
#         print(e)
#         cnt.rollback()
#         return False
#     else:
#         cnt.commit()
#         return True
#     finally:
#         cursor.close()
#         cnt.close()


# def get_newest_data_from_database():
#     cnt = pool.get_connection()
#     cursor = cnt.cursor()
#     cursor.execute('SELECT MAX(id) FROM message')
#     last_id = cursor.fetchone()[0]
#     cursor.execute('SELECT * FROM message WHERE id = %s', (last_id,))
#     result = cursor.fetchone()
#     return result

# def get_all_data():
#     cnt = pool.get_connection()
#     cursor = cnt.cursor()
#     cursor.execute('SELECT message, imgName FROM message LIMIT %s, 4')
#     results = cursor.fetchall()
#     print(results)
#     return results
