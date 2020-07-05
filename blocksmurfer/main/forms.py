from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    search = StringField('', validators=[InputRequired()],
                         render_kw={"placeholder": "enter address, transaction, block id or hash, key, etc"})
    submit = SubmitField('Search')


class TransactionSendForm(FlaskForm):
    rawtx = TextAreaField('Raw Transaction Hex', validators=[InputRequired()],)
    submit = SubmitField('Broadcast Transaction')


class TransactionDecomposeForm(FlaskForm):
    rawtx = TextAreaField('Raw Transaction Hex', validators=[InputRequired()],)
    submit = SubmitField('Decompose Transaction')
