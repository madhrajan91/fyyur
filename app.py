#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import label
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Artist, Venue, Show

import datetime

import sys

from utils import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

#migrate
migrate =  Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  venues = Venue.query.filter().order_by(Venue.state, Venue.city, Venue.name)
  
  currCity = ""
  cityVenues = {}
  for venue in venues:
      if currCity != venue.city:
        if currCity != "":
          data.append(cityVenues)
        currCity = venue.city
        cityVenues = {}
        cityVenues["city"] = venue.city
        cityVenues["state"] = venue.state
        cityVenues["venues"] = []
      
      cityVenue = {}
      cityVenue["id"] = venue.id
      cityVenue["name"] = venue.name
      cityVenue["num_upcoming_shows"] = len(venue.upcoming_shows)     
      
      cityVenues['venues'].append(cityVenue)

  data.append(cityVenues)
    
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  key = request.form["search_term"]

  venues = Venue.query.filter(Venue.name.ilike("%"+key+"%"))
  response = {}
  response["count"] = venues.count()
  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_show_count
    })

  response["data"] = data
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  
  data = {}
  data["id"] = venue.id
  data["name"] = venue.name
  data["genres"] = eval(venue.genres) if venue.genres != '' else ''
  data["city"] = venue.city
  data["state"] = venue.state
  data["address"] = venue.address
  data["phone"] = venue.phone
  data["website"] = venue.website
  data["facebook_link"] = venue.facebook_link
  data["seeking_talent"] = venue.seeking_talent
  data["seeking_description"] = venue.seeking_description
  data["image_link"] = venue.image_link

  upcoming_shows = []
  for show in venue.upcoming_shows:
    showData = {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    upcoming_shows.append(showData)

  past_shows = []
  for show in venue.past_shows:
    showData = {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    past_shows.append(showData)


  data["upcoming_shows_count"] = len(venue.upcoming_shows)
  data["upcoming_shows"] = upcoming_shows

  data["past_shows_count"] = len(venue.past_shows)
  data["past_shows"] = past_shows

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm(request.form)
  if (form.validate()):
    error = False
    try:
      venue = Venue(name = request.form['name'],
                      city = request.form['city'],
                      state = request.form['state'],
                      address = request.form['address'],
                      phone = request.form['phone'],
                      genres = str(request.form.getlist('genres')),
                      facebook_link = request.form['facebook_link'],
                      image_link = request.form['image_link'],
                      seeking_talent = str_to_bool(request.form['seeking_talent']),
                      website = request.form['website'])
      
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if not error:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    else:
      flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
    return render_template('pages/home.html')
  else:
    print(form.data)
    flash(form.errors)
    return redirect(url_for('create_venue_form'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  
  # TODO: populate form with values from venue with ID <venue_id>
  error = False
  try:
    #print(venue_id)
    venue = Venue.query.get(venue_id)
    form = VenueForm()
    print(venue)
    data={
      "id": venue.id,
      "name": venue.name,
      "genres": eval(venue.genres) if venue.genres != '' else '',
      "address": venue.address,
      "city": venue.city,
      "state": States(venue.state),
      "phone": venue.phone,
      "website": venue.website,
      "facebook_link": venue.facebook_link,
      "seeking_talent": Seek(venue.seeking_talent),
      "seeking_description": venue.seeking_description,
      "image_link": venue.image_link
    }
    
    form.state.data = States(venue.state)
    form.seeking_talent.data = Seek(venue.seeking_talent)
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if not error:
    return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  form = VenueForm(request.form)
  if (form.validate()):

    try:
      venue = Venue.query.get(venue_id)
      venue.name = request.form['name']
      venue.city = request.form['city']
      venue.state = request.form['state']
      venue.phone = request.form['phone']
      venue.address = request.form['address']
      venue.genres = str(request.form.getlist('genres'))
      venue.facebook_link = request.form['facebook_link']
      venue.image_link = request.form['image_link']
      venue.seeking_talent = str_to_bool(request.form['seeking_talent'])
      venue.seeking_description = request.form['seeking_description']
      venue.website = request.form['website']
      
      print(venue)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    print(form.data)
    flash(form.errors)
    return redirect(url_for('edit_venue', venue_id=venue_id))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  print("DELETE")
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  return redirect(url_for('.index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  artists = Artist.query.filter().order_by(Artist.name)
  
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  key = request.form["search_term"]
  artists = Artist.query.filter(Artist.name.ilike("%"+key+"%"))
  response = {}
  response["count"] = artists.count()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": len(artist.upcoming_shows)
    })

  response["data"] = data
  print(response)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get(artist_id)
 
  data = {}
  data["id"] = artist.id
  data["name"] = artist.name
  data["genres"] = eval(artist.genres) if artist.genres != '' else ''
  data["city"] = artist.city
  data["state"] = artist.state
  data["phone"] = artist.phone
  data["website"] = artist.website
  data["facebook_link"] = artist.facebook_link
  data["seeking_venue"] = artist.seeking_venue
  data["seeking_description"] = artist.seeking_description
  data["image_link"] = artist.image_link
  
  past_shows = []
  upcoming_shows = []
  
  upcoming_shows = []
  for show in artist.upcoming_shows:
    showData = {
       "venue_id": show.venue.id,
       "venue_name": show.venue.name,
       "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    upcoming_shows.append(showData)

  past_shows = []
  for show in artist.past_shows:
    showData = {
        "venue_id": show.venue.id,
       "venue_name": show.venue.name,
       "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    past_shows.append(showData)


  
  data["past_shows_count"] = len(artist.past_shows)
  data["upcoming_shows_count"] = len(artist.upcoming_shows)
  data["past_shows"] = past_shows
  data["upcoming_shows"] = upcoming_shows
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  error = False
  try:
    artist = Artist.query.get(artist_id)
    data = {
      "id": artist.id,
      "name": artist.name,
      "genres": eval(artist.genres) if artist.genres != '' else '',
      "city": artist.city,
      "state": artist.state,
      "phone": artist.phone,
      "website": artist.website,
      "image_link": artist.image_link,
      "facebook_link": artist.facebook_link,
      "seeking_venue": artist.seeking_venue,
      "seeking_description": artist.seeking_description
    }
    
    form.state.data = States(artist.state)
    form.seeking_venue.data= Seek(artist.seeking_venue)
    print(data)
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if not error:
    return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  
  form = ArtistForm(request.form)
  if (form.validate()):
    error = False
    try:
      artist = Artist.query.get(artist_id)
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.genres = str(request.form.getlist('genres'))
      artist.facebook_link = request.form['facebook_link']
      artist.image_link = request.form['image_link']
      artist.seeking_venue =  str_to_bool(request.form['seeking_venue'])
      artist.seeking_description = request.form['seeking_description']
      artist.website = request.form['website']
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()

    if not error:
      return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    print(form.data)
    flash(form.errors)
    return redirect(url_for('edit_artist', artist_id=artist_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = ArtistForm(request.form)
  if (form.validate()):
    error = False
    try:
      artist = Artist(name = request.form['name'],
                      city = request.form['city'],
                      state = request.form['state'],
                      phone = request.form['phone'],
                      genres = str(request.form.getlist('genres')),
                      facebook_link = request.form['facebook_link'],
                      image_link = request.form['image_link'],
                      seeking_venue = str_to_bool(request.form['seeking_venue']),
                      seeking_description = request.form['seeking_description'],
                      website = request.form['website'])

      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    
    if not error:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    else:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be created.')
    return render_template('pages/home.html')
  else:
    print(form.data)
    flash(form.errors)
    return redirect(url_for('create_artist_form'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  for show in Show.query.all():
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    })
 
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:

    show = Show(artist_id = request.form['artist_id'],
              venue_id = request.form['venue_id'],
              start_time = request.form['start_time'])

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  if not error:
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
      flash('An error occurred. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
