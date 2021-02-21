from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import sys

from sqlalchemy.sql.operators import startswith_op

db = SQLAlchemy()
migrate = Migrate()

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())
    shows = db.relationship('Show', backref='venue', lazy='dynamic') 
    # Enabled dynamic to be able to compare between start_time and now

    def upcoming_shows(self):
        return self.shows.filter(Show.start_time > datetime.now()).all()

    def upcoming_shows_count(self):
        return self.shows.filter(Show.start_time > datetime.now()).count()

    def past_shows(self):
        return self.shows.filter(Show.start_time < datetime.now()).all()

    def past_shows_count(self):
        return self.shows.filter(Show.start_time < datetime.now()).count()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows": [
                show.serialize_for_venue() for show in self.past_shows()],
            "upcoming_shows": [
                show.serialize_for_venue() for show in self.upcoming_shows()],
            "past_shows_count": self.past_shows_count(),
            "upcoming_shows_count": self.upcoming_shows_count()
        }

    @classmethod
    def group_by_area(cls):
        data = []
        # Distinct Areas -> area = (city, state)
        areas = db.session.query(cls.city, cls.state)\
            .group_by(cls.city, cls.state).all()

        # Grouping
        for area in areas:
            venues = cls.query.filter(cls.state==area.state)\
                .filter(cls.city==area.city).all()
            data.append({
                "city": area.city,
                "state": area.state,
                "venues": [{
                        "id": venue.id,
                        "name": venue.name,
                        "num_upcoming_shows": venue.upcoming_shows_count()
                    } for venue in venues]
            })
        return data

    @classmethod
    def create(cls, data):
        error = False
        try:
            venue = cls(**data)
            db.session.add(venue)
            db.session.commit()
            
        except:
            print(sys.exc_info())
            error = True
            db.session.rollback()

        finally:
            db.session.close

        return not error

    @classmethod
    def search(cls, search_term):
        venues = cls.query.filter(cls.name.ilike(f'%{search_term}%'))
        return {
            "count": venues.count(),
            "data": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.upcoming_shows_count()    
            } for venue in venues]
        }

    def update(self, name, city, state, address, phone, image_link, genres, facebook_link, website, seeking_talent, seeking_description):
        error = False
        try:
            # Updating the available fields in the update form 
            self.name = name
            self.city = city
            self.state = state
            self.address = address
            self.phone = phone
            self.image_link = image_link
            self.genres = genres
            self.facebook_link = facebook_link
            self.website = website
            self.seeking_talent = bool(seeking_talent)
            self.seeking_description = seeking_description
            db.session.commit()
        except:
            print(sys.exc_info())
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        return not error

    def delete(self):
        error = False
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            print(sys.exc_info())
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        return not error


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String()))
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String())
    website = db.Column(db.String())
    facebook_link = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String())
    image_link = db.Column(db.String())
    shows = db.relationship('Show', backref='artist', lazy='dynamic')

    def upcoming_shows(self):
        return self.shows.filter(Show.start_time > datetime.now()).all()

    def upcoming_shows_count(self):
        return self.shows.filter(Show.start_time > datetime.now()).count()

    def past_shows(self):
        return self.shows.filter(Show.start_time < datetime.now()).all()

    def past_shows_count(self):
        return self.shows.filter(Show.start_time < datetime.now()).count()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genres": self.genres,
            "city": self.city,
            "state": self.state,
            "phone": self.phone,
            "website": self.website,
            "facebook_link": self.facebook_link,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "image_link": self.image_link,
            "past_shows": [
                show.serialize_for_artist() for show in self.past_shows()],
            "upcoming_shows": [
                show.serialize_for_artist() for show in self.upcoming_shows()],
            "past_shows_count": self.past_shows_count(),
            "upcoming_shows_count": self.upcoming_shows_count()
        }

    @classmethod
    def create(cls, data):
        error = False
        try:
            artist = cls(**data)
            db.session.add(artist)
            db.session.commit()
            
        except:
            print(sys.exc_info())
            error = True
            db.session.rollback()

        finally:
            db.session.close

        return not error
    
    @classmethod
    def search(cls, search_term):
        artists = cls.query.filter(cls.name.ilike(f'%{search_term}%'))
        return {
            "count": artists.count(),
            "data": [{
                "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": artist.upcoming_shows_count()    
            } for artist in artists]
        }

    def update(self, name, city, state, phone, image_link, genres, facebook_link, website, seeking_venue, seeking_description):
        error = False
        try:
            # Updating the available fields in the update form 
            self.name = name
            self.city = city
            self.state = state
            self.phone = phone
            self.image_link = image_link
            self.genres = genres
            self.facebook_link = facebook_link
            self.website = website
            self.seeking_venue = bool(seeking_venue)
            self.seeking_description = seeking_description
            db.session.commit()
        except:
            print(sys.exc_info())
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        return not error


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
    start_time = db.Column(db.DateTime())

    def serialize(self):
        return {
            "venue_id": self.venue.id,
            "venue_name": self.venue.name,
            "artist_id": self.artist.id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": str(self.start_time)
        }   
    
    def serialize_for_venue(self):
        return {
            "artist_id": self.artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": str(self.start_time)
        }

    def serialize_for_artist(self):
        return {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "start_time": str(self.start_time)
        }

    @classmethod
    def create(cls, data):
        error = False
        try:
            show = cls(**data)
            db.session.add(show)
            db.session.commit()
            
        except:
            print(sys.exc_info())
            error = True
            db.session.rollback()

        finally:
            db.session.close

        return not error
    