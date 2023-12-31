from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text,nullable=False)
    mimetype_profile = db.Column(db.Text,nullable=False)
    name =db.Column(db.Text,nullable=False)
    email =db.Column(db.String(150),unique=True)
    username =db.Column(db.String(150),unique=True)
    password =db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    is_admin = db.Column(db.Boolean, default=False)
    is_creater = db.Column(db.Boolean, default=False)
    Song = db.relationship("Song",backref="user",passive_deletes=True)
    playlists = db.relationship('Playlist', back_populates='user')
    album=db.relationship("Album",back_populates='user')
    ratings = db.relationship("Rating", back_populates="user")


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_profile = db.Column(db.Text,nullable=True)
    mimetype_song_profile = db.Column(db.Text,nullable=True)
    song = db.Column(db.Text,nullable=False)
    song_name = db.Column(db.Text,nullable=False)
    mimetype_song_audio = db.Column(db.Text,nullable=False)
    song_lyrics = db.Column(db.Text,nullable=True)
    mimetype_song_lyrics= db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer,db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    artist= db.Column(db.Text,nullable=True)
    gernre = db.Column(db.Text,nullable=True)
    ratings = db.relationship('Rating', back_populates='song') 


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text,nullable=False)
    mimetype_profile = db.Column(db.Text,nullable=False)
    songs = db.relationship('Song', secondary='playlist_song', backref='playlists')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    user = db.relationship('User', back_populates='playlists')
    ratings = db.relationship('Rating', back_populates='playlist')



playlist_song = db.Table('playlist_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    artist= db.Column(db.Text, nullable=False)
    image = db.Column(db.Text,nullable=False)
    gernre = db.Column(db.Text,nullable=True)
    songs = db.relationship('Song', secondary='album_song', backref='album')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    user = db.relationship('User', back_populates='album')
    
 
album_song = db.Table('album_song',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id',ondelete="CASCADE")),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id',ondelete="CASCADE"))
)




class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)  # You can use an integer to represent the rating value (e.g., 1-5 stars)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='ratings',)

    song_id = db.Column(db.Integer, db.ForeignKey('song.id',ondelete="CASCADE"), nullable=True)
    song = db.relationship('Song', back_populates='ratings') # Associate the rating with a song

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id',ondelete="CASCADE"),nullable=True)
    playlist = db.relationship('Playlist', back_populates='ratings')