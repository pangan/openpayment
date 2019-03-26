"""
By Amir Mofakhar <amir@mofakhar.info>
"""
import logging

from flask import Blueprint, render_template, request, Response, json

from payments.fetch_data.tasks import get_data_from_celery, get_fields_from_celery
from payments.common.utils import get_all_values_of_a_key_from_list_of_dict, get_data_from_dict

from payments.common.forms import SearchForm


bp = Blueprint('open_payment', __name__)


_LOG = logging.getLogger(__name__)

autocomplete_data = []


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

    return render_template("search.html", form=form, search_field=search_field,
                           search_keyword=search_keyword,
                           search_result=search_result, column_titles=column_titles)


@bp.route('/_autocomplete', methods=['GET'])
def autocomplete():
    return Response(json.dumps(autocomplete_data), mimetype='application/json')



