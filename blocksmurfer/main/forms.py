# -*- coding: utf-8 -*-
#
#    Blocksmurfer - Blockchain Explorer
#
#    © 2020-2021 March - 1200 Web Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
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


class ScriptForm(FlaskForm):
    script_hex = TextAreaField('Script Hex', validators=[InputRequired()], )
    submit = SubmitField('Decompose Script')
