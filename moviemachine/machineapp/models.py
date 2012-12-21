from django.db import models
#import Image

##### Types #####
#GenreType = (
#    ('Action', 'Action'), #('Adventure','Adventure'), 	('Animation',) ,	('Biography',),
#    ('Comedy', 'Comedy'), #('Crime',) ,	('Documentary',), 	('Drama',),
#    ('Family', 'Family'), #('Fantasy',) 	('Film-Noir',) 	('Game-Show',)
#    ('History', 'History'), #('Horror',) 	('Music') 	('Musical',)
#    ('Mystery', 'Mystery'), #('News',)	('Reality-TV') 	('Romance',)
#    ('Sci-Fi', 'Sci-Fi'), #('Sport',) 	('Talk-Show') 	('Thriller',)
#    ('War', 'War'),    #('Western',)
#    )
import locale

RoleType = (
    ('Actor', 'Actor'),
    ('Director','Director'),
    ('Producer','Producer'),
    ('Writer','Writer'),
    )

RatingType = (
    ('G', 'G'),
    ('PG','PG'),
    ('PG-13','PG-13'),
    ('R','R'),
    ('NC17','NC17'),
    ('No Rating', 'No Rating')
    )

# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=128)
    state = models.CharField(max_length=32)
    country = models.CharField(max_length=128)
    boxofficemojo_url = models.URLField()
    imdb_url = models.URLField()
    thenumbers_url = models.URLField()
    fandango_url = models.URLField()
    extra = models.CharField(max_length=256,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    def __unicode__(self):
        return self.name+', '+self.state+', '+self.country


class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128,blank=True)
    middle_name = models.CharField(max_length=128,blank=True)
    birth_date = models.DateField(null=True)
    height = models.IntegerField(null=True)
    bname_first = models.CharField(max_length=128)
    bname_last = models.CharField(max_length=128,null=True)
    bname_middle = models.CharField(max_length=128,null=True)
    birth_city = models.CharField(max_length=128,null=True)
    birth_state = models.CharField(max_length=128,null=True)
    birth_country = models.CharField(max_length=128,null=True)
    bio = models.TextField(null=True)
    known_for = models.CharField(max_length=64,choices=RoleType,null=True)
    boxofficemojo_url = models.URLField(null=True)
    imdb_url = models.URLField(null=True)
    thenumbers_url = models.URLField(null=True)
    fandango_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    def __unicode__(self):
        return self.first_name+' '+self.last_name

class Movie(models.Model):
    title = models.CharField(max_length=128)
    studio = models.ForeignKey(Studio, null=True)
    genre = models.CharField(max_length=64, null=False)
    mpaa_rating = models.CharField(max_length=16, choices=RatingType, null=True)
    release_date = models.DateTimeField(auto_now_add=False,null=True)
    runtime = models.IntegerField(null=True,default=0)
    budget = models.IntegerField(default=0)
    cast = models.ManyToManyField(Person, through='Casting')
    boxofficemojo_url = models.URLField()
    imdb_url = models.URLField()
    thenumbers_url = models.URLField()
    fandango_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    def __unicode__(self):
        return self.title+', '+unicode(self.studio)+', '+unicode(self.release_date)

    def budget_display(self):
        locale.setlocale( locale.LC_MONETARY, 'en_CA.UTF-8' )
        'English_United States.1252'
        return locale.currency( self.budget, grouping=True )


class Casting(models.Model):
    person = models.ForeignKey(Person)
    movie = models.ForeignKey(Movie)
    role = models.CharField(max_length=64, choices=RoleType, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)


class BoxOffice(models.Model):
    box_office_date = models.DateField('Date')
    movie = models.ForeignKey(Movie)
    gross = models.IntegerField()
    rank = models.IntegerField(null=True)
    estimate = models.BooleanField()
    total_gross = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    def __unicode__(self):
        return self.movie+', '+unicode(self.gross)+', '+self.box_office_date

class Prediction(models.Model):
    prediction_date = models.DateField()
    movie = models.ForeignKey(Movie)
    gross = models.IntegerField()
    total_gross = models.IntegerField(null=True)
    rank = models.IntegerField()
    accuracy = models.DecimalField(decimal_places=4,max_digits=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)
    def __unicode__(self):
        return self.name+', '+unicode(self.venue)+', '+unicode(self.city)+', '+self.event_type

class Picture(models.Model):
    image = models.ImageField(upload_to = 'img')
    movie = models.ForeignKey(Movie, null=True)
    person = models.ForeignKey(Person, null=True)
    description = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return self.name+', '+unicode(self.venue)+', '+unicode(self.city)+', '+self.event_type

class EmailSignup(models.Model):
    email_address = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

class Feedback(models.Model):
    sender = models.EmailField()
    name = models.CharField(max_length=256, null=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)