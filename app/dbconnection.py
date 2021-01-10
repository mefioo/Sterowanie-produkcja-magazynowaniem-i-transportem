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


def findServiceIdByName(name):
    cursor.execute("SELECT ID_service FROM service WHERE Name = '{}'".format(name))
    result = cursor.fetchall()
    try:
        return result[0]
    except Exception as e:
        pass


def findClientIdByName(name):
    cursor.execute("SELECT ID_client FROM client WHERE Name = '{}'".format(name))
    result = cursor.fetchall()
    try:
        return result[0]
    except Exception as e:
        pass


def insertServiceReservation(date, company, service):
    sql_query = "INSERT INTO service_reservations (ID_client, ID_service, Date) VALUES ({}, {}, '{}')".format(company, service, date)
    try:
        cursor.execute(sql_query)
        link.commit()
        return True
    except Exception as e:
        return False
