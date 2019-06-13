from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('로그인')


class RegisterForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()], description="test")
    email = EmailField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    submit = SubmitField('회원가입')


class ForgotPasswordForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('회원정보 조회')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('repeat password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('재설정')

class PurchaseGameForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    game_id = StringField('game_id', validators=[DataRequired()])
    submit = SubmitField('구매하기')