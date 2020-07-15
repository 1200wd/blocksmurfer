from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
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


class StoreDataForm(FlaskForm):
    data = TextAreaField('Data', validators=[InputRequired()],)
    transaction_fee = IntegerField('Transaction Fee in Satoshi', validators=[InputRequired()], default=0)
    # blocksmurfer_gift = IntegerField('Blocksmurfer Gift', validators=[InputRequired()], default=0)
    submit = SubmitField('Create Transaction')
