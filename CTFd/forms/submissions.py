from wtforms import SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class SubmissionSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("provided", "提交内容"),
            ("id", "提交ID"),
            ("account_id", "账户ID"),
            ("challenge_id", "题目ID"),
            ("challenge_name", "题目名"),
        ],
        default="provided",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")
