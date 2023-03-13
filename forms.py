from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators

class SignUp(FlaskForm):
    username = StringField(label='Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), validators.Email()])
    password = StringField('Password',validators=[DataRequired()])
    pass_confirm = StringField('pass_confirm', validators=[DataRequired(), 
                                                          validators.EqualTo('pass_confirm', message="password must match")  
                                                            ])
    submit = SubmitField('Sign In')