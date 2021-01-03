from flask import render_template
from app import app
from app import dbconnection as db


@app.route('/')
@app.route('/main')
def main():
    print(db.finsService())
    return render_template('main.html', title='Strona główna')
