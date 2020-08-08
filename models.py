from datetime import datetime, timezone
from config import db


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f'<Show id: {self.id}>'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            'start_time': self.start_time
        }


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(50)), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship("Show", cascade="all, delete", backref="venue")

    def __repr__(self):
        return f'<Venue id: {self.id}, name: {self.name}>'

    @property
    def serialize(self):
        past_shows = self._get_past_shows()
        upcoming_shows = self._get_upcoming_shows()
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'genres': self.genres,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'past_shows': past_shows,
            'past_shows_count': len(past_shows),
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': len(upcoming_shows)
        }

    @property
    def serialize_by_name_id(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': len(self._get_upcoming_shows())
        }

    @property
    def serialize_by_city_and_state(self):
        return {
            'city': self.city,
            'state': self.state,
            'venues': self._get_venues_by_city_and_state()
        }

    def _get_upcoming_shows(self):
        return list(filter(lambda s: s.start_time >= datetime.now(timezone.utc), self.shows))

    def _get_past_shows(self):
        return list(filter(lambda s: s.start_time < datetime.now(timezone.utc), self.shows))

    def _get_venues_by_city_and_state(self):
        venues = Venue.query.filter_by(city=self.city, state=self.state).all()
        return [venue.serialize_by_name_id for venue in venues]


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String(50)), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship("Show", cascade="all, delete", backref="artist")

    def __repr__(self):
        return f'<Artist id: {self.id}, name: {self.name}>'

    @property
    def serialize(self):
        past_shows = self._get_past_shows()
        upcoming_shows = self._get_upcoming_shows()
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'genres': self.genres,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'past_shows': past_shows,
            'past_shows_count': len(past_shows),
            'upcoming_shows': upcoming_shows,
            'upcoming_shows_count': len(upcoming_shows)
        }

    @property
    def serialize_by_name_id(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_upcoming_shows': len(self._get_upcoming_shows())
        }

    def _get_upcoming_shows(self):
        return list(filter(lambda s: s.start_time >= datetime.now(timezone.utc), self.shows))

    def _get_past_shows(self):
        return list(filter(lambda s: s.start_time < datetime.now(timezone.utc), self.shows))
