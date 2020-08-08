# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import render_template, request, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler
from forms import ShowForm, VenueForm, ArtistForm
from config import db, app
from models import Venue, Artist, Show

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.distinct(Venue.city, Venue.state).all()
    data = [venue.serialize_by_city_and_state for venue in venues]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    data = {
        "count": len(venues),
        "data": [venue.serialize_by_name_id for venue in venues]
    }
    return render_template('pages/search_venues.html', results=data, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    return render_template('pages/show_venue.html', venue=venue.serialize)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    if form.validate_on_submit():
        data = request.form
        try:
            is_seeking_talent = True if data['seeking_description'].strip() else False
            venue = Venue(name=data['name'],
                          city=data['city'],
                          state=data['state'],
                          address=data['address'],
                          genres=request.form.getlist('genres'),
                          phone=data['phone'],
                          image_link=data['image_link'],
                          facebook_link=data['facebook_link'],
                          website=data['website'],
                          seeking_talent=is_seeking_talent,
                          seeking_description=data['seeking_description']
                          )
            db.session.add(venue)
            db.session.commit()
            flash(f'Venue {data["name"]} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Venue {data["name"]} could not be listed.')
        finally:
            db.session.close()
        return render_template('pages/home.html')
    # Flashing current errors
    for input, errors in form.errors.items():
        flash(f'Invalid value for "{input}". {"".join(errors)}')
    return render_template('forms/new_venue.html', form=form)

#  Venue Update
#  ----------------------------------------------------------------


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.filter_by(id=venue_id).first_or_404()
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()

    if form.validate_on_submit():
        data = request.form
        try:
            is_seeking_talent = True if data['seeking_description'].strip() else False
            venue = Venue.query.get(venue_id)
            venue.name = data['name']
            venue.city = data['city']
            venue.state = data['state']
            venue.address = data['address']
            venue.genres = request.form.getlist('genres')
            venue.phone = data['phone']
            venue.image_link = data['image_link']
            venue.facebook_link = data['facebook_link']
            venue.website = data['website']
            venue.seeking_talent = is_seeking_talent
            venue.seeking_description = data['seeking_description']
            db.session.commit()
            flash(f'Venue {data["name"]} was successfully edited!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Venue {data["name"]} could not be edited.')
        finally:
            db.session.close()
    # Flashing form validation errors
    for input, errors in form.errors.items():
        flash(f'Invalid value for "{input}". {"".join(errors)}')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Venue Delete
#  ----------------------------------------------------------------


@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue with id {venue_id} was successfully deteled!')
    except:
        db.session.rollback()
        flash(f'An error occured. Venue with id {venue_id} could not be deleted')
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = [artist.serialize_by_name_id for artist in artists]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    data = {
        "count": len(artists),
        "data": [artist.serialize_by_name_id for artist in artists]
    }
    return render_template('pages/search_artists.html', results=data, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first_or_404()
    return render_template('pages/show_artist.html', artist=artist.serialize)

#  Artists Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first_or_404()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()

    if form.validate_on_submit():
        data = request.form
        try:
            is_seeking_venue = True if data['seeking_description'].strip() else False
            artist = Artist.query.get(artist_id)
            artist.name = data['name']
            artist.city = data['city']
            artist.state = data['state']
            artist.genres = request.form.getlist('genres')
            artist.phone = data['phone']
            artist.image_link = data['image_link']
            artist.facebook_link = data['facebook_link']
            artist.website = data['website']
            artist.seeking_venue = is_seeking_venue
            artist.seeking_description = data['seeking_description']
            db.session.commit()
            flash(f'Artist {data["name"]} was successfully edited!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Artist {data["name"]} could not be edited.')
        finally:
            db.session.close()
    # Flashing form validation errors
    for input, errors in form.errors.items():
        flash(f'Invalid value for "{input}". {"".join(errors)}')

    return redirect(url_for('show_artist', artist_id=artist_id))

#  Artists Create
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    if form.validate_on_submit():
        data = request.form
        try:
            is_seeking_venue = True if data['seeking_description'].strip() else False
            artist = Artist(name=data['name'],
                            city=data['city'],
                            state=data['state'],
                            genres=request.form.getlist('genres'),
                            phone=data['phone'],
                            image_link=data['image_link'],
                            facebook_link=data['facebook_link'],
                            website=data['website'],
                            seeking_venue=is_seeking_venue,
                            seeking_description=data['seeking_description']
                            )
            db.session.add(artist)
            db.session.commit()
            flash(f'Artist {data["name"]} was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occurred. Artist {data["name"]} could not be listed.')
        finally:
            db.session.close()
        return render_template('pages/home.html')
    # Flashing current errors
    for input, errors in form.errors.items():
        flash(f'Invalid value for "{input}". {"".join(errors)}')
    return render_template('forms/new_artist.html', form=form)

#  Artists Delete
#  ----------------------------------------------------------------


@app.route('/artists/<artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        flash(f'Venue with id {artist_id} was successfully deteled!')
    except:
        db.session.rollback()
        flash(f'An error occured. Venue with id {artist_id} could not be deleted')
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = [show.serialize for show in shows]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    if form.validate_on_submit():
        try:
            data = request.form
            show = Show(artist_id=data['artist_id'],
                        venue_id=data['venue_id'],
                        start_time=data['start_time'])
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except:
            db.session.rollback()
            flash(f'An error occured. Show could not be listed')
        finally:
            db.session.close()
        return render_template('pages/home.html')
    # Flashing current errors
    for input, errors in form.errors.items():
        flash(f'Invalid value for "{input}". {"".join(errors)}')
    return render_template('forms/new_show.html', form=form)


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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
