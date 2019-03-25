"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging

from flask import Blueprint, jsonify, render_template, request, Response, json

from payments.fetch_data.tasks import get_data_from_celery
from payments.common.utils import (get_keys_from_dict, get_all_values_of_a_key_from_list_of_dict,
                                   get_keys_from_dict_2, get_data_from_dict)


from wtforms import StringField, Form, SelectField, SubmitField, HiddenField


bp = Blueprint('open_payment', __name__)


_LOG = logging.getLogger(__name__)

autocomplete_data = []


class SearchForm(Form):
    data = get_data_from_celery()

    # TODO: find keys and store them in celery and here read them from celery

    fields_2 = []

    if data:
        fields = get_keys_from_dict(data[0])
        fields_2 = get_keys_from_dict_2(data[0])

    fields.insert(0, ('', 'Select a field ...'))
    search_field = SelectField(u'Searching field', choices=fields, id='search_field', )
    search_data = StringField('', id='search_data_complete', render_kw={'class': 'search_box'})
    field_to_search = HiddenField(id='field_to_search')
    sub = SubmitField('Search')


@bp.route('/', methods=['GET', 'POST'])
def search_payment():
    search_result = None
    column_titles = None
    global autocomplete_data
    autocomplete_data = ['london', 'stockholm']
    form = SearchForm(request.form)
    #form.field_to_search.data = form.search_field.data
    if request.method == 'POST':

        autocomplete_data = get_all_values_of_a_key_from_list_of_dict(get_data_from_celery(),
                                                                          form.search_field.data)


        if form.sub.data:
            autocomplete_data = get_all_values_of_a_key_from_list_of_dict(get_data_from_celery(),
                                                                          form.field_to_search.data)

            search_result = get_data_from_dict(form.data, form.field_to_search.data,
                                               form.search_data.data)

            form.search_field.data = form.field_to_search.data
            column_titles = form.fields_2

        else:
            form.field_to_search.data = form.search_field.data


    return render_template("search.html", form=form,
                           search_result=search_result, column_titles=column_titles)



@bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(autocomplete_data), mimetype='application/json')
