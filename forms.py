from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextAreaField, validators, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL
#import phonenumbers

from enums import Genres, Seek, States


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class EntityForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        default=States.AL, validators=[DataRequired()],
        choices= States.choices(), coerce=States.coerce
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    # def validate_phone(form, field):
    #     if len(field.data) > 16:
    #         raise ValidationError('Phone number contians more than 16 characters')
    #     else:
    #         try:
    #             input_number = phonenumbers.parse(field.data)
    #             if not (phonenumbers.is_valid_number(input_number)):
    #                 raise ValidationError('Invalid phone number.')
    #         except:
    #             input_number = phonenumbers.parse("+1"+field.data)
    #             if not (phonenumbers.is_valid_number(input_number)):
    #                 raise ValidationError('Invalid phone number.')

    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField('genres', validators=[DataRequired()],
            choices=Genres.choices(), coerce=Genres.coerce
            )
    
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

    image_link = StringField(
        'image_link', validators=[URL()]
    )

    website = StringField(
        'website', validators=[URL()]
    )

    seeking_description = TextAreaField(
        'seeking_description')
class VenueForm(EntityForm):
    address = StringField(
        'address', validators=[DataRequired()]
    )

    seeking_talent = SelectField(
        'seeking_talent', default=Seek.Yes, validators=[DataRequired()],
        choices= Seek.choices(), coerce=Seek.coerce
    )

class ArtistForm(EntityForm):

    seeking_venue = SelectField('seeking_venue',
        default=Seek.Yes, validators=[DataRequired()],
        choices=Seek.choices(), coerce=Seek.coerce
    )
