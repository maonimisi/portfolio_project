from flask import render_template, request, Blueprint
from forecasting.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html', title='Home')


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/community")
def community():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('community.html', title='Community', posts=posts)


@main.route("/premium")
def premium():
    return render_template('premium.html', title='Premium')