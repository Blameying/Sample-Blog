# -*- coding:utf-8 -*- 
from flask import render_template,flash,redirect,session,g
from app import app
from .forms import LoginForm,RegisterForm,PostForm
from app.models import User,Post,Comment,Tag,tags
from app import db
from sqlalchemy import func,desc
from datetime import datetime

@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page,10)
    recent,top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags=post.tags
    comments=post.comments.order_by(Comment.date.desc()).all()
    recent,top_tags = sidebar_data()

    return render_template(
        'post.html',
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags
    )

@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent,top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent = recent,
        top_tags = top_tags
    )

@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent,top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=user,
        posts=posts,
        recent=recent,
        top_tags = top_tags
    )


@app.before_request
def before_request():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session['username']
        ).one()
    else:
        g.current_user=None

@app.route('/login',methods=['GET','POST'])
def login():
    if 'username' in session:
        flash("您已经登录！")
        return redirect('/')
    
    form=LoginForm()

    if form.validate_on_submit():
        session['username']=form.username.data

    return render_template('login.html',title='登录',form=form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    g.current_user=None
    return redirect('login')

@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return redirect('/home')
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
        return redirect('.login')
    return render_template('register.html',form=form)


@app.route('/new',methods=['GET','POST'])
def new_post():
    if 'username' not in session:
        return redirect('login')
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.text = form.text.data
        new_post.user_id = g.current_user.id
        new_post.publish_date = datetime.now()

        db.session.add(new_post)
        db.session.commit()
    return render_template('new.html',form = form)

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_post(id):
    if 'username' not in session:
        return redirect('login')
    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.now()

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('/post',post_id=post.id))
    form.text.data=post.text

    return render_template('edit.html',form=form,post=post)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html',wrong="404"),404

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(Tag,func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent,top_tags