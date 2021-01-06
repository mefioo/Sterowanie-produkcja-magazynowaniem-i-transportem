from flask import render_template
from app import app
from app import dbconnection as db
from app import helpers as hp
from app import branchAndBound as bb


@app.route('/')
@app.route('/main')
def main():
    addresses = hp.getAddressesOfClients(['1', '24', '14', '12', '2', '1'])
    costMatrix, size = hp.generateMatrixForAlgorithm(addresses)
    data = bb.read_data(costMatrix, size)
    data.prep_data()
    data.doBranchAndBound()
    path = data.path
    for row in costMatrix:
        print(row)
    for id in path:
        print(str(id) + " " + addresses[id+1])
    return render_template('main.html', title='Strona główna')
