"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from flask import Blueprint, request
import flask_excel

from payments.common.utils import get_data_from_dict
from payments.fetch_data.tasks import get_data_from_celery, get_fields_from_celery

output_excel = flask_excel


bp = Blueprint('download', __name__)


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
    return_file = output_excel.make_response_from_array(excel_list, 'xls', file_name='payments')
    return return_file
