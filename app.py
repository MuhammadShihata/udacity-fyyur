# IMPORTS
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask.globals import session
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *


# APP CONFIG
app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate.init_app(app, db)

moment = Moment(app)


# FILTERS
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


# CONTROLLERS

""" HOME PAGE """

@app.route('/')
def index():
    return render_template('pages/home.html')


""" VENUES """

# CREATE
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    """Returns a form to the user for adding a new venue"""
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """ Called upon submitting the new artist listing form """
    # Get the data
    form = VenueForm(request.form,  meta={'csrf': False})
    form_data = form.data
    form_data.update({"seeking_talent": bool(form_data['seeking_talent'])})

    # Create the venue
    created = Venue.create(form_data)
    
    # Update the user 
    if created:
        flash('Venue listed successfully!')
    else: 
        flash('Sorry, an error occurred.')

    return render_template('pages/home.html')

# READ
@app.route('/venues')
def venues():
    """List venues grouped by area (city, state)"""
    data = Venue.group_by_area()
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    """Search venues"""
    search_term = request.form.get('search_term', '')
    response = Venue.search(search_term)
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    """Show the venue details page"""
    venue = Venue.query.get(venue_id)
    return render_template('pages/show_venue.html', venue=venue.serialize())

# UPDATE
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    """Returns form populated with the artist data"""
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    """Edit a venue using it's id"""
    # Get form data
    form = VenueForm(request.form, meta={'csrf': False})
    form_data = form.data

    # Get the venue
    venue = Venue.query.get(venue_id)  

    # Update the venue
    updated = venue.update(**form_data)
    
    if updated:
        flash('Venue updatdeded successfully!')
        return redirect(url_for('show_venue', venue_id=venue_id))
    else: 
        flash('Sorry, an error occurred.')
        return redirect(url_for('edit_venue', venue_id=venue_id))


# DELETE
@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    """Delete a venue using it's id"""
    venue = Venue.query.get(venue_id)
    print('del invoked')
    deleted = venue.delete()
    print(deleted)
    if deleted:
        flash('Venue deleted successfully!')
    else: 
        flash('Sorry, an error occurred.')

    return redirect(url_for('venues'))



""" Artists """

# CREATE
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    """Returns a form to the user for adding a new Artist"""
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():  
    """ Called upon submitting the new artist listing form """
    # Get the data
    form = ArtistForm(request.form, csrf_enabled=False)
    form_data = form.data
    form_data.update({'seeking_venue': bool(form_data['seeking_venue'])})
    
    # Create the venue
    created = Artist.create(form_data)
    
    # Update the user 
    if created:
        flash('Artist listed successfully!')
    else: 
        flash('Sorry, an error occurred.')

    return render_template('pages/home.html')

# READ
@app.route('/artists')
def artists():
    artists = Artist.query.all() 
    data = [{'id': artist.id, 'name': artist.name} for artist in artists]
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    """Search Artists"""
    search_term = request.form.get('search_term', '')
    response = Artist.search(search_term)
    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    """Show the venue details page"""
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist.serialize())


# UPDATE
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """Returns form populated with the artist data"""
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)
    

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id): 
    """Edit a venue using it's id"""
    # Get form data
    form = ArtistForm(request.form, meta={'csrf': False})
    form_data = form.data

    # Get the artist
    artist = Artist.query.get(artist_id)  

    # Update the venue
    updated = artist.update(**form_data)
    
    if updated:
        flash('Artist updatdeded successfully!')
        return redirect(url_for('show_artist', artist_id=artist_id))                       
    else: 
        flash('Sorry, an error occurred.')
        return redirect(url_for(f'edit_artist', artist_id=artist_id))                       
    


""" SHOWS """

# READ
@app.route('/shows')
def shows():                                                      #DONE
  """ displays list of shows at /shows """
  shows = Show.query.all()
  data = [show.serialize() for show in shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  """ renders form. do not touch """
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():                                      #DONE
    """ called upon submitting the new artist listing form """

    form = ShowForm(request.form, csrf_enabled=False)
    form_data = form.data
 
    # Create the venue
    created = Show.create(form_data)
    
    # Update the user 
    if created:
        flash('Show listed successfully!')
    else: 
        flash('Sorry, an error occurred.')

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


# LAUNCH

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''