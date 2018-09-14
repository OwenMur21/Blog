from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import Required
from wtforms import ValidationError

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class PitchForm(FlaskForm):
    content = TextAreaField("What is your blog about?",validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    description = TextAreaField('Add comment',validators=[Required()])
    submit = SubmitField()