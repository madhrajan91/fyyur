from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
db = SQLAlchemy()

class Entity(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120)) 


    seeking_description = db.Column(db.String(), nullable=True)

    @hybrid_property
    def upcoming_shows(self):
        upcomingShows = []
        current_time = datetime.datetime.utcnow()
        for show in self.shows:
            if show.start_time > current_time:
                upcomingShows.append(show)
        return upcomingShows
    
    @hybrid_property
    def past_shows(self):
        pastShows = []
        current_time = datetime.datetime.utcnow()
        for show in self.shows:
            if show.start_time <= current_time:
                pastShows.append(show)
        return pastShows

class Venue(Entity):
    __tablename__ = 'Venue'
  
    address = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean, nullable=True)
    
    # past shows and up coming shows from the shows table
    def __repr__(self):
        return f'<Venue Id: {self.id} Name: {self.name} City: {self.city} State: {self.state} phone: {self.phone} genres: {self.genres} image_link: {self.image_link} fb_link: {self.facebook_link}>'

class Artist(Entity):
    __tablename__ = 'Artist'   

    seeking_venue = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<Artist Id: {self.id} Name: {self.name} City: {self.city} State: {self.state} phone: {self.phone} genres: {self.genres} image_link: {self.image_link} fb_link: {self.facebook_link}>'




#TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    start_time = db.Column(db.DateTime(), nullable=False)

    artist = db.relationship("Artist", backref=db.backref("shows"))
    venue = db.relationship("Venue", backref=db.backref("shows"))

    def __repr__(self):
        return f'<Show Id: {self.id}, Artist Id: {self.artist_id} Venue Id: {self.venue_id}>'
