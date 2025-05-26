from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email
from app.models import UserRole


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=3, max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=3, max=12)])
    role = SelectField("Role", choices=[(role.name, role.value) for role in UserRole])
    submit = SubmitField("Create User")
