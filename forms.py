from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextAreaField, validators, ValidationError
from wtforms.validators import DataRequired, InputRequired, AnyOf, URL


from enums import Genres, Seek, States
import re

# Form for Shows
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

# Entity Form common to Artists and Venues
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
    phone = StringField(
        'phone'
    )
    def validate_phone(form, field):
        print ('validating phone')
        data = field.data
        if (data is not None):
            phone_number = data.replace('-', '')
            print (phone_number)
            if len(phone_number) != 10:
                raise ValidationError("Phone number must be of the formation XXX-XXX-XXXX")
            else:
                pattern = re.compile("^[\d]{10}$")
                if (pattern.match(phone_number) is None):
                    raise ValidationError("Phone number must be of the formation XXX-XXX-XXXX")

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

# Form for Venue
class VenueForm(EntityForm):
    address = StringField(
        'address'
    )

    seeking_talent = SelectField(
        'seeking_talent', default=Seek.Yes, validators=[InputRequired()],
        choices= Seek.choices(), coerce=Seek.coerce
    )

# Form for Artist
class ArtistForm(EntityForm):

    seeking_venue = SelectField(
        'seeking_venue',
        default=Seek.Yes, validators=[InputRequired()],
        choices=Seek.choices(), coerce=Seek.coerce
    )
