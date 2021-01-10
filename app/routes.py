from flask import render_template, redirect, url_for, flash
from app import app
from app import dbconnection as db
from app import helpers as hp
from app import branchAndBound as bb
import app.forms as forms


@app.route('/')
@app.route('/main')
def main():
    # addresses = hp.getAddressesOfClients(['1', '24', '14', '12', '2'])
    # costMatrix, size = hp.generateMatrixForAlgorithm(addresses)
    # data = bb.read_data(costMatrix, size)
    # data.prep_data()
    # data.doBranchAndBound()
    # path = data.path
    # for row in costMatrix:
    #     print(row)
    # print(f"{path}")
    # print(f"{addresses}")
    # for id in path:
    #     print(str(id) + " " + addresses[id])
    return render_template('main.html', title='Strona główna')


@app.route('/')
@app.route('/addReservation', methods=['GET', 'POST'])
def addReservation():
    form = forms.addReservation()
    clients = db.findClient()
    for client in clients:
        client_name = [client[1], client[1]]
        form.companyName.choices.append(client_name)
        services = db.findService()
    for service in services:
        print(service)
        service_name = [service[2], service[2]]
        form.service.choices.append(service_name)
    if form.validate_on_submit():
        company_id = db.findClientIdByName(form.companyName.data)
        service_id = db.findServiceIdByName(form.service.data)
        print(f"{company_id[0]} company name")
        print(f"{service_id[0]} service id")
        db.insertServiceReservation(form.date.data, company_id[0], service_id[0])
        flash('Rezerwacja została dodana!', 'success')
        return redirect(url_for('main'))
    return render_template('addReservation.html', title='Dodaj rezerwację zlecenia', form=form)
