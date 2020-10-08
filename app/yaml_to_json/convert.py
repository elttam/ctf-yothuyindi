import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired

from . import _yaml_to_json

bp = Blueprint('convert', __name__)

class ConvertForm(FlaskForm):
    """
    Form using WTForm to convert YAML to JSON
    """
    yaml = TextAreaField('yaml', validators=[DataRequired()])
    json = TextAreaField('json', render_kw={'disabled':''})
    submit = SubmitField('Convert')

@bp.route('/', methods=('GET', 'POST'))
def convert():
    form = ConvertForm()
    if form.validate_on_submit():
        form.json.data = _yaml_to_json.to_json(form.yaml.data)
        return render_template('convert.html', form=form)
    return render_template('convert.html', form=form)
