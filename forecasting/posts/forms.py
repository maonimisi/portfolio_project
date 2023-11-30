from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    chart = FileField('Chart Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
