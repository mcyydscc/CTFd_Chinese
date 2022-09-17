from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.models import TeamFieldEntries, TeamFields
from CTFd.utils.countries import SELECT_COUNTRIES_LIST
from CTFd.utils.user import get_current_team


def build_custom_team_fields(
    form_cls,
    include_entries=False,
    fields_kwargs=None,
    field_entries_kwargs=None,
    blacklisted_items=("affiliation", "website"),
):
    if fields_kwargs is None:
        fields_kwargs = {}
    if field_entries_kwargs is None:
        field_entries_kwargs = {}

    fields = []
    new_fields = TeamFields.query.filter_by(**fields_kwargs).all()
    user_fields = {}

    # Only include preexisting values if asked
    if include_entries is True:
        for f in TeamFieldEntries.query.filter_by(**field_entries_kwargs).all():
            user_fields[f.field_id] = f.value

    for field in new_fields:
        if field.name.lower() in blacklisted_items:
            continue

        form_field = getattr(form_cls, f"fields[{field.id}]")

        # Add the field_type to the field so we know how to render it
        form_field.field_type = field.field_type

        # Only include preexisting values if asked
        if include_entries is True:
            initial = user_fields.get(field.id, "")
            form_field.data = initial
            if form_field.render_kw:
                form_field.render_kw["data-initial"] = initial
            else:
                form_field.render_kw = {"data-initial": initial}

        fields.append(form_field)
    return fields


def attach_custom_team_fields(form_cls, **kwargs):
    new_fields = TeamFields.query.filter_by(**kwargs).all()
    for field in new_fields:
        validators = []
        if field.required:
            validators.append(InputRequired())

        if field.field_type == "text":
            input_field = StringField(
                field.name, description=field.description, validators=validators
            )
        elif field.field_type == "boolean":
            input_field = BooleanField(
                field.name, description=field.description, validators=validators
            )

        setattr(form_cls, f"fields[{field.id}]", input_field)


class TeamJoinForm(BaseForm):
    name = StringField("团队名称", validators=[InputRequired()])
    password = PasswordField("团队密码", validators=[InputRequired()])
    submit = SubmitField("加入")


def TeamRegisterForm(*args, **kwargs):
    class _TeamRegisterForm(BaseForm):
        name = StringField("团队名称", validators=[InputRequired()])
        password = PasswordField("团队密码", validators=[InputRequired()])
        submit = SubmitField("创建")

        @property
        def extra(self):
            return build_custom_team_fields(
                self, include_entries=False, blacklisted_items=()
            )

    attach_custom_team_fields(_TeamRegisterForm)
    return _TeamRegisterForm(*args, **kwargs)


def TeamSettingsForm(*args, **kwargs):
    class _TeamSettingsForm(BaseForm):
        name = StringField(
            "团队名",
            description="展示给其他团队的名称",
        )
        password = PasswordField(
            "新团队密码", description="设置一个新的加入团队密码"
        )
        confirm = PasswordField(
            "密码",
            description="提供您当前的团队密码（或您的密码）以更新您团队的密码",
        )
        affiliation = StringField(
            "组织",
            description="展示给其他团队的组织名",
        )
        website = URLField(
            "Web",
            description="展示给其他团队的Web",
        )
        country = SelectField(
            "国家",
            choices=SELECT_COUNTRIES_LIST,
            description="展示给其他团队的国家",
        )
        submit = SubmitField("提交")

        @property
        def extra(self):
            fields_kwargs = _TeamSettingsForm.get_field_kwargs()
            return build_custom_team_fields(
                self,
                include_entries=True,
                fields_kwargs=fields_kwargs,
                field_entries_kwargs={"team_id": self.obj.id},
            )

        def get_field_kwargs():
            team = get_current_team()
            field_kwargs = {"editable": True}
            if team.filled_all_required_fields is False:
                # Show all fields
                field_kwargs = {}
            return field_kwargs

        def __init__(self, *args, **kwargs):
            """
            Custom init to persist the obj parameter to the rest of the form
            """
            super().__init__(*args, **kwargs)
            obj = kwargs.get("obj")
            if obj:
                self.obj = obj

    field_kwargs = _TeamSettingsForm.get_field_kwargs()
    attach_custom_team_fields(_TeamSettingsForm, **field_kwargs)

    return _TeamSettingsForm(*args, **kwargs)


class TeamCaptainForm(BaseForm):
    # Choices are populated dynamically at form creation time
    captain_id = SelectField("团队队长", choices=[], validators=[InputRequired()])
    submit = SubmitField("提交")


class TeamSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "团队名"),
            ("id", "ID"),
            ("affiliation", "组织"),
            ("website", "Web"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class PublicTeamSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "团队名"),
            ("affiliation", "组织"),
            ("website", "Web"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class TeamBaseForm(BaseForm):
    name = StringField("团队名称", validators=[InputRequired()])
    email = EmailField("邮箱")
    password = PasswordField("密码")
    website = URLField("Web")
    affiliation = StringField("组织")
    country = SelectField("国家", choices=SELECT_COUNTRIES_LIST)
    hidden = BooleanField("隐藏")
    banned = BooleanField("封禁")
    submit = SubmitField("提交")


def TeamCreateForm(*args, **kwargs):
    class _TeamCreateForm(TeamBaseForm):
        pass

        @property
        def extra(self):
            return build_custom_team_fields(self, include_entries=False)

    attach_custom_team_fields(_TeamCreateForm)

    return _TeamCreateForm(*args, **kwargs)


def TeamEditForm(*args, **kwargs):
    class _TeamEditForm(TeamBaseForm):
        pass

        @property
        def extra(self):
            return build_custom_team_fields(
                self,
                include_entries=True,
                fields_kwargs=None,
                field_entries_kwargs={"team_id": self.obj.id},
            )

        def __init__(self, *args, **kwargs):
            """
            Custom init to persist the obj parameter to the rest of the form
            """
            super().__init__(*args, **kwargs)
            obj = kwargs.get("obj")
            if obj:
                self.obj = obj

    attach_custom_team_fields(_TeamEditForm)

    return _TeamEditForm(*args, **kwargs)


class TeamInviteForm(BaseForm):
    link = URLField("邀请链接")


class TeamInviteJoinForm(BaseForm):
    submit = SubmitField("加入")
