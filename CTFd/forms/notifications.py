from wtforms import BooleanField, RadioField, StringField, TextAreaField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField


class NotificationForm(BaseForm):
    title = StringField("标题", description="公告标题")
    content = TextAreaField(
        "内容",
        description="公告内容，支持html和markdown",
    )
    type = RadioField(
        "公告类型",
        choices=[("toast", "右下角弹窗"), ("alert", "中间弹窗"), ("background", "不提醒")],
        default="toast",
        description="公告提醒类型",
        validators=[InputRequired()],
    )
    sound = BooleanField(
        "声音",
        default=True,
        description="发布公告是时候响铃",
    )
    submit = SubmitField("提交")
