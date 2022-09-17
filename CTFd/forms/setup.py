from wtforms import (
    FileField,
    HiddenField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.constants.themes import DEFAULT_THEME
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.config import get_themes


class SetupForm(BaseForm):
    ctf_name = StringField(
        "平台名称", description="你的CTF平台名称"
    )
    ctf_description = TextAreaField(
        "平台描述", description="介绍一下你的CTF"
    )
    user_mode = RadioField(
        "模式设置",
        choices=[("teams", "团队模式"), ("users", "单人模式")],
        default="teams",
        description="控制用户是组队玩（团队模式）还是自己玩（单人模式）",
        validators=[InputRequired()],
    )

    name = StringField(
        "管理员用户名",
        description="管理帐户的用户名",
        validators=[InputRequired()],
    )
    email = EmailField(
        "管理员邮箱",
        description="您的管理帐户的电子邮件地址",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "管理员密码",
        description="管理帐户的密码",
        validators=[InputRequired()],
    )

    ctf_logo = FileField(
        "Logo",
        description="用于网站的徽标，而不是CTF名称。用作主页按钮。可选",
    )
    ctf_banner = FileField(
        "首页图片", description="主页使用的横幅。 可选."
    )
    ctf_small_icon = FileField(
        "ico图片",
        description="用户浏览器中使用的图标。仅接受PNG。必须是32x32px. 可选.",
    )
    ctf_theme = SelectField(
        "主题",
        description="CTFd主题使用。可以稍后更改。",
        choices=list(zip(get_themes(), get_themes())),
        default=DEFAULT_THEME,
        validators=[InputRequired()],
    )
    theme_color = HiddenField(
        "主题颜色",
        description="主题用于控制颜色。需要主题支持. 可选.",
    )

    start = StringField(
        "开始时间", description="您的CTF计划开始的时间. 可选."
    )
    end = StringField(
        "结束时间", description="您的CTF计划结束的时间. 可选."
    )
    submit = SubmitField("完成")
