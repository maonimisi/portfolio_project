import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from forecasting import app, db, bcrypt
from werkzeug.utils import secure_filename
from forecasting.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from forecasting.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/community")
def community():
    posts = Post.query.all()
    return render_template('community.html', title='Community', posts=posts)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    
    # output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/share", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.chart.data:
            chart_file = form.chart.data
            chart_filename = save_picture(chart_file)
            post = Post(
                title=form.title.data,
                content=form.content.data,
                author=current_user,
                chart=chart_filename  # Store the file name
            )
            db.session.add(post)
            db.session.commit()

            flash('Your Post has been created', 'success')
            return redirect(url_for('community'))
        else:
            flash('Invalid file type. Allowed file types are: png, jpg, jpeg, gif', 'danger')

    return render_template('share.html', title='Share Ideas', form=form, legend='New Idea')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        # Check if a new file was provided in the form
        if form.chart.data:
            chart_file = form.chart.data
            chart_filename = save_picture(chart_file)
            post.chart = chart_filename

        db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('share.html', title='Update Ideas', form=form, legend='Update Idea')


@app.route("/premium")
def premium():
    return render_template('premium.html', title='Premium')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
         db.session.add(user)
         db.session.commit()
         flash('Account Created Successfully!', 'success')
         return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
         user = User.query.filter_by(email=form.email.data).first()
         if user and bcrypt.check_password_hash(user.password, form.password.data):
             login_user(user, remember=form.remember.data)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect(url_for('home'))
         else:
              flash('Login Unsuccessfull. Please check email and password', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        image_file = url_for('static', filename='uploads/'
        + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)