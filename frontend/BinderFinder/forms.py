import re

from wtforms import Form, StringField, TextAreaField, validators
from wtforms import HiddenField, PasswordField


strip_filter = lambda x: x.strip() if x else None
split_filter = lambda x: re.split('\W+', x)

class SearchCreateForm(Form):
    id = HiddenField()
    keywords = StringField('Keywords', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    pfams = StringField('pfam-IDs', [validators.Length(max=255)],
                         filters=[strip_filter])

class SearchUpdateForm(SearchCreateForm):
    id = HiddenField()

