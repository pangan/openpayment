"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging

from flask import Blueprint, jsonify, render_template, request, Response, json

from payments.fetch_data.tasks import get_data_from_celery
from payments.common.utils import get_keys_from_dict


from wtforms import StringField, Form, SelectField, SubmitField


bp = Blueprint('open_payment', __name__)


_LOG = logging.getLogger(__name__)

autocomplete_data = []



@bp.route('/aa')
def index():
    variables = {'columns': []}
    data = get_data_from_celery()

    # TODO: find keys and store them in celery and here read them from celery
    if data:
        variables = {'columns': get_keys_from_dict(data)[0]}

    return render_template('search.html', variables=variables)


@bp.route('/search2')
def search_payment():
    """Sample route for endpoint.
    """
    _LOG.info('received request!')

    data = get_data_from_celery()

    #data = 1
    return jsonify({'data': data})


class SearchForm(Form):
    data = get_data_from_celery()

    # TODO: find keys and store them in celery and here read them from celery
    fields = []
    if data:
        fields = get_keys_from_dict(data[0])

    search_field = SelectField(u'Searching field', choices=fields, id='amir')
    search_data = StringField('Insert City', id='search_data_complete')
    sub = SubmitField()


@bp.route('/', methods=['GET', 'POST'])
def automine():
    search_result = None
    global autocomplete_data
    autocomplete_data = ['london', 'stockholm']
    form = SearchForm(request.form)
    if request.method == 'POST':
        autocomplete_data = ['amir', 'tehran', form.search_field.data]
        if form.sub.data:
            search_result = 'DDD'

    return render_template("automine.html", form=form, search_result=search_result)



@bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(autocomplete_data), mimetype='application/json')
