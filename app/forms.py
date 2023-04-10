# 表单类
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(message= u'username不能为空')])
    userNumber = StringField(u'学号', validators=[DataRequired(message= u'学号不能为空')])
    password = PasswordField(u'密码', validators=[DataRequired(message= u'密码不能为空')])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField(u'姓名', validators=[DataRequired(message= u'姓名不能为空')])
    userNumber = StringField(u'学号', validators=[DataRequired(message= u'学号不能为空')])
    email = StringField(u'邮箱', validators=[DataRequired(message= u'邮箱不能为空'), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(message= u'密码不能为空')])
    password2 = PasswordField(
        u'重新输入密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_userNumber(self, userNumber):
        user = User.query.filter_by(userNumber=userNumber.data).first()
        if user is not None:
            raise ValidationError('该学号已注册,请使用其它学号.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已注册,请使用其它邮箱.')
