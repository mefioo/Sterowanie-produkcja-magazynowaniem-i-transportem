import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'spmit',
    'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)
cursor = link.cursor(buffered=True)


def finsService():
    cursor.execute("SELECT * FROM service")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass
