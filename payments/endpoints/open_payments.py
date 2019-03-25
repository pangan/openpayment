"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging

from flask import Blueprint, jsonify, render_template, request, Response, json

from payments.fetch_data.tasks import get_data_from_celery, get_fields_from_celery
from payments.common.utils import (get_keys_from_dict, get_all_values_of_a_key_from_list_of_dict,
                                   get_keys_from_dict_2, get_data_from_dict)


from wtforms import StringField, Form, SelectField, SubmitField, HiddenField

import flask_excel


my_excel = flask_excel

bp = Blueprint('open_payment', __name__)


_LOG = logging.getLogger(__name__)

autocomplete_data = []


class SearchForm(Form):

    fields = get_fields_from_celery()

    fields.insert(0, ('', 'Select a field ...'))
    search_field = SelectField(u'Searching field', choices=fields, id='search_field', )
    search_data = StringField('', id='search_data_complete', render_kw={'class': 'search_box'})
    field_to_search = HiddenField(id='field_to_search')
    submit_search = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def search_payment():
    search_result = None
    column_titles = None
    global autocomplete_data
    autocomplete_data = []
    form = SearchForm(request.form)

    search_field = None
    search_keyword = None

    if request.method == 'POST':

        autocomplete_data = get_all_values_of_a_key_from_list_of_dict(get_data_from_celery(),
                                                                          form.search_field.data)


        if form.submit_search.data:
            search_keyword = form.search_data.data
            search_field = form.field_to_search.data

            autocomplete_data = get_all_values_of_a_key_from_list_of_dict(get_data_from_celery(),
                                                                          search_field)

            search_result = get_data_from_dict(get_data_from_celery(), search_field,
                                               search_keyword)

            form.search_field.data = search_field
            column_titles = get_fields_from_celery()

        else:
            form.field_to_search.data = form.search_field.data

    return render_template("search.html", form=form, search_field= search_field,
                           search_keyword=search_keyword,
                           search_result=search_result, column_titles=column_titles)


@bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(autocomplete_data), mimetype='application/json')


@bp.route('/download_excel', methods=['GET'])
def download_excel():

    field = request.args.get('field')
    keyword = request.args.get('keyword')
    excel_list = []
    titles = []
    raw_title = []
    for raw_column, column in get_fields_from_celery():
        titles.append(column)
        raw_title.append(raw_column)

    data = get_data_from_dict(get_data_from_celery(), field, keyword)
    excel_list.append(titles)
    for record in data:
        record_list = []
        for field in raw_title:
            record_list.append(record.get(field, ''))
        excel_list.append(record_list)

    return my_excel.make_response_from_array(excel_list, 'xls', file_name='payments')
