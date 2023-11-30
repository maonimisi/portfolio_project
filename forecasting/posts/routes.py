from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from forecasting import db
from forecasting.models import Post
from forecasting.posts.forms import PostForm
from forecasting.users.utils import save_picture

posts = Blueprint('posts', __name__)

@posts.route("/share", methods=['GET', 'POST'])
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
            return redirect(url_for('main.community'))
        else:
            flash('Invalid file type. Allowed file types are: png, jpg, jpeg, gif', 'danger')

    return render_template('share.html', title='Share Ideas', form=form, legend='New Idea')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('share.html', title='Update Ideas', form=form, legend='Update Idea')
