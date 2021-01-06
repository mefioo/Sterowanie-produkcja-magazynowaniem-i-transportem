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


def findService():
    cursor.execute("SELECT * FROM service")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass


def findClient():
    cursor.execute("SELECT * FROM client")
    result = cursor.fetchall()
    try:
        return result
    except Exception as e:
        pass


def findClientById(id):
    cursor.execute("SELECT * FROM client WHERE ID_client = '{}'".format(id))
    result = cursor.fetchall()
    try:
        return result[0]
    except Exception as e:
        pass



