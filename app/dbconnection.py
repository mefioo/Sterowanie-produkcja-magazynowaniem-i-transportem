import mysql.connector
import random
import string

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


def findClientsAndAddIfDBIsEmpty():
    cursor.execute("SELECT * FROM client")
    result = cursor.fetchall()
    if len(result) < 1:
        data = []
        file = open("app/static/Text/kontrahenci 2020.csv", "r", encoding="utf8")
        for line in file:
            parts = line.split(';')
            parts[3] = ''.join(random.choices(string.digits, k=9))
            parts[3] = '+48' + parts[3]
            sql_query = "INSERT INTO client (Name, Street, City, Phone) VALUES ('{}','{}','{}','{}')".format(parts[0],
                                                                                                             parts[1],
                                                                                                             parts[2],
                                                                                                             parts[3])
            try:
                cursor.execute(sql_query)
                link.commit()
            except Exception as e:
                pass


def finsService():
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



