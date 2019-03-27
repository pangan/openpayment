"""
By Amir Mofakhar <amir@mofakhar.info>
"""
from wtforms import Form, HiddenField, SelectField, StringField, SubmitField

from payments.fetch_data.tasks import get_fields_from_celery


class SearchForm(Form):

    fields = get_fields_from_celery()

    fields.insert(0, ('', 'Select a field ...'))
    search_field = SelectField(u'Searching field', choices=fields, id='search_field', )
    search_data = StringField('', id='search_data_complete', render_kw={'class': 'search_box'})
    field_to_search = HiddenField(id='field_to_search')
    submit_search = SubmitField('Search')
