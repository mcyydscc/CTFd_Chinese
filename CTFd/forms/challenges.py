from wtforms import MultipleFileField, SelectField, StringField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class ChallengeSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "题目名"),
            ("id", "ID"),
            ("category", "分类"),
            ("type", "类型"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class ChallengeFilesUploadForm(BaseForm):
    file = MultipleFileField(
        "上传文件",
        description="使用Control+Click或Cmd+Click附加多个文件。",
        validators=[InputRequired()],
    )
    submit = SubmitField("上传")
