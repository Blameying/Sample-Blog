# -*- coding:utf-8 -*- 
from flask import render_template,flash,redirect
from app import app
from .forms import LoginForm,RegisterForm
from app.models import User,Post,Comment,Tag
from app import db

@app.route('/')
@app.route('/index')
def index():
    flash("Hello!")
    return render_template("index.html",title="Monkey Li",nickname="Li")

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash('登录需要您的用户名和密码')
        return redirect('/index')
    return render_template('login.html',title='登录',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash(
            "你的账户已成功注册，请登录！",
            category='success'
        )
        users = User.query.all()
        print(users)
        return redirect('/login')
    return render_template('register.html',form=form)
