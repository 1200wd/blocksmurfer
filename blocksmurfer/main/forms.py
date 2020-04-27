from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('Address, transaction, wif, key', validators=[DataRequired()])
    submit = SubmitField('Search')
