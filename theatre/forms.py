
from flask_wtf import FlaskForm
from wtforms.fields.core import IntegerField, SelectField, StringField
from wtforms.fields.simple import FileField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class ShowAddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')
    year = IntegerField('Year', validators=[DataRequired()])
    category = SelectField('Category', choices=[('movie', 'Movie'), ('series', 'Web Series')])
    path = FileField('Select Video File', validators=[DataRequired(), FileAllowed(['mp4'])])
    poster_path = FileField('Select Poster File', validators=[DataRequired(), FileAllowed(['jpeg', 'jpg', 'webp', 'png'])])
    submit = SubmitField('Add')


class ShowUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description')
    year = IntegerField('Year', validators=[DataRequired()])
    submit = SubmitField('Update')


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
