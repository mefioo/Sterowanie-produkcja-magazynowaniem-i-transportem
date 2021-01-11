from geopy import Nominatim
import haversine as hs
from haversine import Unit
from app import dbconnection as db


def normalizeCompanyAddress(address):
    if len(address.split(',')) > 1:
        address = address.split(',')[0]
        if len(address.split('-')) > 1:
            address = address.split('-')[0]
    return address


def findGeolocationFromAddress(addres):
    geolocator = Nominatim(user_agent="Sterowanie-produkcja-magazynowanie-i-transportem")
    location = geolocator.geocode(addres)
    result = []
    result.append(location.latitude)
    result.append(location.longitude)
    return result


def countDistanceBetweenLocations(locationOne, locationTwo):
    distance = hs.haversine(locationOne, locationTwo, unit=Unit.METERS)
    return int(format(distance, '.0f'))


def getAddressesOfClients(ids):
    addresses = []

    #get clients from database and add their addresses (normalized street name with city) to list
    for id in ids:
        client = db.findClientById(id)
        addresses.append(normalizeCompanyAddress(client[2]) + " " + client[3])
    return addresses


def generateMatrixForAlgorithm(addresses):
    #Create list of geolocations
    size = len(addresses)
    geolocations = []
    for address in addresses:
        geolocations.append(findGeolocationFromAddress(address))

    #Create cost matrix
    costMatrix = []
    for geolocation in geolocations:
        row = []
        for i in range(size):
            row.append(countDistanceBetweenLocations(geolocation, geolocations[i]))
        costMatrix.append(row)
    return costMatrix, size


def countWorkingHoursFromDay(reservations):
    sum = 0
    for reservation in reservations:
        sum += db.findServiceTimeById(reservation[1])[0]
    return sum
