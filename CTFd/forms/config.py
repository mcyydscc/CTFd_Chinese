from wtforms import BooleanField, FileField, SelectField, StringField, TextAreaField
from wtforms.fields.html5 import IntegerField, URLField
from wtforms.widgets.html5 import NumberInput

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.csv import get_dumpable_tables


class ResetInstanceForm(BaseForm):
    accounts = BooleanField(
        "Accounts",
        description="Deletes all user and team accounts and their associated information",
    )
    submissions = BooleanField(
        "Submissions",
        description="Deletes all records that accounts gained points or took an action",
    )
    challenges = BooleanField(
        "Challenges", description="Deletes all challenges and associated data"
    )
    pages = BooleanField(
        "Pages", description="Deletes all pages and their associated files"
    )
    notifications = BooleanField(
        "Notifications", description="Deletes all notifications"
    )
    submit = SubmitField("Reset CTF")


class AccountSettingsForm(BaseForm):
    domain_whitelist = StringField(
        "邮箱白名单",
        description="允许注册的邮箱域名 (e.g. ctfd.io, gmail.com, yahoo.com)",
    )
    team_creation = SelectField(
        "团队创建",
        description="Control whether users can create their own teams (Teams mode only)",
        choices=[("true", "Enabled"), ("false", "Disabled")],
        default="true",
    )
    team_size = IntegerField(
        widget=NumberInput(min=0),
        description="Amount of users per team (Teams mode only)",
    )
    num_teams = IntegerField(
        "团队最大数量(非团队人数)",
        widget=NumberInput(min=0),
        description="Max number of teams (Teams mode only)",
    )
    verify_emails = SelectField(
        "邮箱验证",
        description="Control whether users must confirm their email addresses before playing",
        choices=[("true", "开启"), ("false", "关闭")],
        default="false",
    )
    team_disbanding = SelectField(
        "团队解散",
        description="Control whether team captains are allowed to disband their own teams",
        choices=[
            ("inactive_only", "Enabled for Inactive Teams"),
            ("disabled", "Disabled"),
        ],
        default="inactive_only",
    )
    name_changes = SelectField(
        "名称修改",
        description="Control whether users and teams can change their names",
        choices=[("true", "Enabled"), ("false", "Disabled")],
        default="true",
    )
    incorrect_submissions_per_min = IntegerField(
        "每分钟提交错误次数",
        widget=NumberInput(min=1),
        description="Amount of submissions allowed per minute for flag bruteforce protection (default: 10)",
    )

    submit = SubmitField("Update")


class ExportCSVForm(BaseForm):
    table = SelectField("Database Table", choices=get_dumpable_tables())
    submit = SubmitField("Download CSV")


class ImportCSVForm(BaseForm):
    csv_type = SelectField(
        "CSV Type",
        choices=[("users", "Users"), ("teams", "Teams"), ("challenges", "Challenges")],
        description="Type of CSV data",
    )
    csv_file = FileField("CSV File", description="CSV file contents")


class LegalSettingsForm(BaseForm):
    tos_url = URLField(
        "Terms of Service URL",
        description="External URL to a Terms of Service document hosted elsewhere",
    )
    tos_text = TextAreaField(
        "Terms of Service", description="Text shown on the Terms of Service page",
    )
    privacy_url = URLField(
        "Privacy Policy URL",
        description="External URL to a Privacy Policy document hosted elsewhere",
    )
    privacy_text = TextAreaField(
        "Privacy Policy", description="Text shown on the Privacy Policy page",
    )
    submit = SubmitField("Update")
