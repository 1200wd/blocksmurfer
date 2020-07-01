from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):

    submit = SubmitField('Search')
    search = StringField('', validators=[DataRequired()],
                         render_kw={"placeholder": "enter address, transaction, block id or hash, key, etc"})
