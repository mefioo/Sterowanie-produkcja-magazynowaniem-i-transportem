from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length


class addReservation(FlaskForm):
    date = StringField('Data zlecenia', validators=[DataRequired(), Length(min=10, max=10)])
    companyName = SelectField('Nazwa firmy', choices=[])
    service = SelectField('Nazwa zlecenia', choices=[])
    submit = SubmitField('Dodaj rezerwację')


class dailyRoute(FlaskForm):
    date = SelectField('Data zlecenia', choices=[])
    submit = SubmitField('Wyznacz trasę')
