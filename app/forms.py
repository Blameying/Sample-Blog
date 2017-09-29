# -*- coding:utf-8 -*- 
from flask_wtf import FlaskForm as Form
from wtforms import StringField,BooleanField,TextAreaField,PasswordField
from wtforms.validators import DataRequired,Length,EqualTo,URL
from app.models import *

class LoginForm(Form):
    username=StringField('用户名',[DataRequired(),Length(max=255)])
    password=PasswordField('密码',[DataRequired(),Length(max=255,min=8)])
    remember_me = BooleanField('记住我',default=False)

    def validate(self):
        check_validate = super(LoginForm,self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(
            username=self.username.data
        ).first()

        if not user:
            self.username.errors.append('Invalid username or password')
            return False
            
        if not user.check_password(self.password.data):
            self.username.errors.append(
               'Invalid username or password' 
            )
            return False
        return True

class RegisterForm(Form):
    username=StringField('用户名',[DataRequired(),Length(max=255)])
    password=PasswordField('密码',[DataRequired(),Length(max=255,min=8)])

    confirm = PasswordField('确认密码',[DataRequired(),EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm,self).validate()

        if not check_validate:
            print("Wrong")
            return False
        user=User.query.filter_by(
            username = self.username.data
        ).first()

        if user:
            self.username.errors.append(
                "该用户名已被使用！"
            )
            return False

        return True

class PostForm(Form):
    title = StringField('标题',[DataRequired(),Length(max=255)])
    text = TextAreaField('正文',[DataRequired()])