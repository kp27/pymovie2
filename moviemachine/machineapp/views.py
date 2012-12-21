
from datetime import timedelta,datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet
from django.shortcuts import render_to_response, render, redirect
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import locale
from machineapp.forms import ContactForm
from machineapp.models import Person, Studio, BoxOffice, Casting, Picture, Feedback
from machineapp.parser import IMDBParser
from models import Movie
from parser import BoxOfficeMojoParser

# Create your views here.

def getFeaturedMovie():
    saturday = datetime.now()
    saturday +=timedelta(days=5-saturday.weekday())

#    saturday.weekday = 7
    sunday = datetime.now()
    sunday +=timedelta(6-sunday.weekday()-7)
    gross_map =   BoxOffice.objects.values("movie").filter(box_office_date__gte=sunday, box_office_date__lte=saturday).annotate(Sum("gross")).order_by("-gross")

    if(len(gross_map) == 0):
        saturday -=timedelta(days=14)
        sunday -=timedelta(days=25)
        gross_map =   BoxOffice.objects.values("movie").annotate(Sum("gross")).order_by("-gross")




    return gross_map
#    query.filter(box_office_date__gte=sunday, box_office_date__lte=saturday)
#    return QuerySet(query=query, model=BoxOffice)

#    movies = models.Movie.objects.ftime_now = datetime.now()
#    four_months_ago = time_now - timedelta(days=(4 * 365) / 12 + 1)
#    calculate day one through 7 of week
#

#    query = BoxOffice.objects.all().aggregate(Sum('gross'))
#    query.aggregate(Sum('gross'))
#    query.filter(approve_result=0)


    #get the phot

    #try returning a tuple!

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

def index(request):

    gross_map = ValuesQuerySetToDict(getFeaturedMovie())
    m_featured = Movie.objects.get(id = gross_map[0]['movie'])
    week_gross = gross_map[0]['gross__sum']
    #Todo remove featured from all
    m_list = Movie.objects.all().order_by('release_date')
    p_list = Picture.objects.filter(movie__in=m_list)#.order_by('release_date')
    paginator = Paginator(m_list, 20)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)


    t = loader.get_template('movies/index.html')
    c = Context({
        'm_list': movies, 'p_list':p_list, 'm_featured': m_featured, 'week_gross': budget_display(week_gross)
    })
    return HttpResponse(t.render(c))


def seed_movies(request):
    print('seed movies')
    bo = IMDBParser()

    m_list = Movie.objects.all().order_by('release_date')[:100]
    parser_m = 'Parser Ran'
    return render_to_response('movies/index.html', {'m_list': m_list,"parser_m": parser_m})

def parse_daily(request):
    print('parse_daily movies')

    bo = BoxOfficeMojoParser()
    bo.seed_movies_database()
    bo.parse_daily()
    imdb = IMDBParser()
    imdb.extract_imdb()
    m_list = Movie.objects.all().order_by('release_date')[:200]
    parser_m = 'Parser Ran Daily'
    return render_to_response('movies/index.html', {'m_list': m_list,"parser_m": parser_m})

def details(request, m_id):
    #cast, studio, boxoffice
    movie = Movie.objects.get(id=m_id)
    b_data = BoxOffice.objects.filter(movie = movie)
    pic = Picture.objects.filter(movie = movie)
    sum = BoxOffice.objects.filter(movie = movie).aggregate(Sum('gross'))

    results_a_string = ""
    for mv in b_data:
        results_a_string = results_a_string+','+mv.gross.__str__()

    results_a_string = results_a_string.lstrip(',')
    sum = sum['gross__sum']
    sum_show =sum_display(sum)
    print('in details' + m_id)
    t = loader.get_template('movies/detail.html')
    c = Context({
        'b_data': b_data, 'movie' :movie, 'sum_show' : sum_show, 'results_a_string':results_a_string,
        'pic': pic
        })
    return HttpResponse(t.render(c))




def about(request):
#    if request.method == 'POST': # If the form has been submitted...
#        form = ContactForm(request.POST) # A form bound to the POST data
#        if form.is_valid(): # All validation rules pass
#            # Process the data in form.cleaned_data
#            # ...
#            return HttpResponseRedirect('/thanks/') # Redirect after POST
#    else:
#        form = ContactForm() # An unbound form
#
#    return render(request, 'movies/about.html', {
#        'form': form,
#        })
    return render(request, 'movies/about.html', {})

def feedback(request):

    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    f = Feedback()
    f.name = name
    f.email = email
    f.message = message
    f.save()
    return render(request, 'movies/thanks.html')


def sum_display(sum):
    if(sum is None):
        sum = 0
    locale.setlocale( locale.LC_MONETARY, 'en_CA.UTF-8' )
    'English_United States.1252'
    return locale.currency( sum, grouping=True )


def budget_display(amt):
    locale.setlocale( locale.LC_MONETARY, 'en_CA.UTF-8' )
    'English_United States.1252'
    return locale.currency( amt, grouping=True )


def redir(request):
    return index(request)