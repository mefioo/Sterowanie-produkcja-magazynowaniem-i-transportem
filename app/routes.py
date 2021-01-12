from flask import render_template, redirect, url_for, flash, session
from app import app
from app import dbconnection as db
from app import helpers as hp
from app import branchAndBound as bb
import app.forms as forms


@app.route('/')
@app.route('/main')
def main():
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
        service_name = [service[2], service[2]]
        form.service.choices.append(service_name)
    if form.validate_on_submit():
        reservations = db.findReservationsByDate(form.date.data)
        total_time = hp.countWorkingHoursFromDay(reservations)
        service_id = db.findServiceIdByName(form.service.data)
        if total_time + db.findServiceTimeById(service_id[0])[0] < 7:
            company_id = db.findClientIdByName(form.companyName.data)
            print(company_id)
            if company_id[0] == 1:
                flash('Nie można wykonać rezerwacji dla samego siebie!', 'danger')
            else:
                db.insertServiceReservation(form.date.data, company_id[0], service_id[0])
                flash('Rezerwacja została dodana!', 'success')
                return redirect(url_for('main'))
        else:
            flash('Nie można wykonać rezerwacji w podanym terminie - pełen terminarz!', 'danger')
    return render_template('addReservation.html', title='Dodaj rezerwację zlecenia', form=form)


@app.route('/chooseDate', methods=['GET', 'POST'])
def chooseDate():
    form = forms.dailyRoute()
    dates = []
    for date in db.findDates():
        dates.append(date[0])
    dates = set(dates)
    for date in dates:
        form.date.choices.append(date)
    if form.validate_on_submit():
        session['messages'] = form.date.data
        return redirect(url_for('route', data=form.date.data))
    return render_template('chooseDate.html', title='Wybierz datę', form=form)


@app.route('/route')
def route():
    date = session['messages']
    data = []

    clients = db.findCompanyIdsInReservationsByDate(date)
    fin_clients = [1]
    for client in clients:
        fin_clients.append(client[0])

    addresses = hp.getAddressesOfClients(fin_clients)
    costMatrix, size = hp.generateMatrixForAlgorithm(addresses)
    alg = bb.read_data(costMatrix, size)
    alg.prep_data()
    alg.doBranchAndBound()
    path = alg.path
    for i in range(len(addresses)):
        if i not in path:
            path.append(i)
            break
    for i in range(len(path)):
        company = list(db.findClientById(fin_clients[path[i]]))
        company.append(i)
        data.append(company)

    return render_template('route.html', title='Trasa', data=data)
