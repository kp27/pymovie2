import datetime
from datetime import timedelta
from datetime import datetime
from time import mktime
import random
import time
#from dateutil import parser
import time
import urllib
import urllib2
from django.core.files.base import File

from PIL import Image, ImageFile
from django.core.files.temp import NamedTemporaryFile
import html5lib
from bs4 import BeautifulSoup
import itertools
import os
import models
import re
from django.db.models import Q
from sys import argv, stdout


class BoxOfficeMojoParser(object):

#    __init__(self):
#
    base_url = 'http://boxofficemojo.com'
    base_file = "counter.txt"

    def current_seed_url(self):
    	url = 'http://boxofficemojo.com/schedule/?view=&release=&date=%r-%r-%r%s'

        nextFriday = datetime.today()
        while nextFriday.weekday() != 4:
            nextFriday += timedelta(1)

        weeks = '&showweeks=15&p=.htm'
        y = nextFriday.year
        return url %(nextFriday.year,nextFriday.month,nextFriday.day,weeks)


    def seed_movies_database(self):
        #friday url
        seed_url = self.current_seed_url()
        #get the release schedule page
        con = urllib2.urlopen(seed_url)
        data = con.read()
        bs = BeautifulSoup(data)

        for table in bs.find_all('table',width='500', cellspacing='1', cellpadding='5', border='0'):
            for item in table.find_all('td',bgcolor='#f4f4ff'):
                if not item.a == None:
                    if item.a['href'].startswith('/movies'):
                        m_url = BoxOfficeMojoParser.base_url+item.a['href']
                        m_title = item.a.text
                        obj, created = models.Movie.objects.get_or_create(title=m_title, boxofficemojo_url=m_url)
                        print(created)
                        print(obj.title)
                        print(obj.boxofficemojo_url)

        con.close()

    def movie_summary(self, s_table, movie):
        for td in s_table.find_all('td', valign='top'):
            if 'Distributor' in td.text:
                dist = td.text.replace('Distributor:','')
                s_url = td.a['href']
                obj, created = models.Studio.objects.get_or_create(name=dist, boxofficemojo_url=s_url)
                movie.studio = obj
            elif 'Release Date:' in td.text:
                ts = time.strptime(td.text.replace('Release Date:',''), ' %B %d, %Y')
                movie.release_date = datetime.fromtimestamp(time.mktime(ts))
            elif 'Genre:' in td.text:
                movie.genre = td.text.replace('Genre:','')
            elif 'MPAA Rating:' in td.text:
                movie.mpaa_rating = td.text.replace('MPAA Rating:','')
            elif 'Production Budget:' in td.text:
                amt_text = td.text.replace('Production Budget: ','')
                #$14 million or $400,000 todo make this  work
                if(amt_text == 'N/A'):
                    movie.budget =0
                else:
                    amt = (amt_text.replace('$','').replace(',','').replace(' million','000000'))
                    movie.budget = amt
            elif 'Runtime:' in td.text:
                runtime_text = td.text.replace('Runtime: ','')
                runtime_text = runtime_text.replace('<br>','').replace('</br>','')
                #$14 million or $400,000 todo make this  work
                if(runtime_text == 'N/A'):
                    movie.runtime =0
                else:
                    hours = runtime_text[:runtime_text.find('hrs')-1]
                    minutes = runtime_text[runtime_text.find('min')-3:runtime_text.find('min')-1]
                    runtime = int(hours)*60+int(minutes)
                    movie.runtime = runtime
#                    print(movie.runtime)
        movie.save();
        return movie;

    def four_months_ago(self):
        time_now = datetime.now()
        four_months_ago = time_now - timedelta(days=(4 * 365) / 12 + 1)
        return four_months_ago

    def do_i_run(self, movie):

        txt = open(self.base_file,'rb')
#        print "Contents: %s" % txt.read()
        nums = txt.read().split(",")
        found = False

        for num in nums:
            if((not num== "") and long(num) == movie.id):
                found = True

        txt.close()

        if(not found):
            txt = open(self.base_file,'a')
            txt.write(str(movie.id))
            txt.write(",")
            txt.flush()
            os.fsync(txt)
            txt.close()


        return not found

    def reset_file(self):
        txt = open(self.base_file,'a')
        txt.truncate()
        txt.close()
        return
    def parse_daily(self):
        # get list of active movies (?) date for now
        four_months_ago = self.four_months_ago()

        #select movies where release_date < today - 4 months or is null
        movies = models.Movie.objects.filter(Q(release_date__gte=four_months_ago) | Q(release_date__isnull=True)).order_by('id')
        #iterate, we will keep a file of ids, once the id is
        last_id = 0;
        for movie in movies :
            if self.do_i_run(movie):
                print(movie.title)
                con = urllib2.urlopen(movie.boxofficemojo_url)
                data = con.read()
                bs = BeautifulSoup(data)

                s_table = bs.find('table', width='95%', cellpadding='4', border='0', bgcolor='#dcdcdc')
                self.movie_summary(s_table, movie)
                divs = bs.find_all('div')

                for div in divs:
                    if 'class' in div.attrs and 'mp_box' in div['class'] and 'The Players' in div.text:
                        c_table = div.find('table')
                        self.cast_extract(c_table, movie)

                con.close()
                self.extract_dailies(movie)
                time.sleep(random.randint(8, 16))
            last_id = movie.id

        last_movie = movies.reverse()[0]
        if(not self.do_i_run(last_movie) and last_movie == last_id):
            self.reset_file()

    def cast_extract(self, c_table, movie):

        for tr in c_table.find_all('tr'):
            for td in tr.find_all('td'):
                if('Director' in td.text):
                    self.extract_players(tr,movie,'Director')
                elif ('Writer' in td.text):
                    self.extract_players(tr,movie,'Writer')
                elif ('Actor' in td.text):
                    self.extract_players(tr,movie,'Actor')
                elif ('Producer' in td.text):
                    self.extract_players(tr,movie,'Producer')


        return movie

    def extract_players(self, tr, mmovie, role_type):
        tds = tr.find_all('td')

        for td in itertools.islice(tds,1,2):
            ass = (td.find_all('a'))
            for a in ass:
                d_name = a.text
                names = d_name.split(' ')
                d_url = a['href']
                #does he exist?
                print d_url+' '+d_name
                def name():
                    if(len(names) == 1):
                        return ''
                    else:
                        return names[1]

                obj, created = models.Person.objects.get_or_create(first_name=names[0], last_name=name() ) #todo make imdb url
                #link to casting
                obj2, created = models.Casting.objects.get_or_create(movie=mmovie,person=obj,role=role_type)

    def extract_dailies(self, mmovie):

        url = mmovie.boxofficemojo_url.replace('movies/?', 'movies/?page=daily&')
        con = urllib2.urlopen(url)
        data = con.read()
        bs = BeautifulSoup(data)

        for table in bs.find_all('table', width='100%', cellspacing='0', cellpadding='3', bordercolor='#111111',
            border='1'):
            for item in table.find_all('td', valign='top'):
                if(item.a is not None):
                    link = item.a['href']
                    #extract the date
                    m = re.search('\d\d\d\d-\d\d-\d\d',link)
                    date_string = m.group(0)
#                   date = parser.parse(date_string)
                    date = time.strptime(date_string, '%Y-%m-%d')

                    if(item.find('font', color='#000080') is not None):
                        amt = item.find('font', color='#000080').next_element
                        est = True
#                        if(amt is not None): Todo estimations
#                            est = False
                        if(amt is not None and not amt == 'Daily Gross'):
                            #parse the actual value
                            amt = amt.replace('$','').replace(',','')
                            print('In all dates'+date.__str__()+' '+amt)
                            dt = datetime.fromtimestamp(time.mktime(date))
                            obj, created = models.BoxOffice.objects.get_or_create(box_office_date=dt, movie=mmovie, gross=amt, estimate=False)
#                            obj.gross = amt

                            obj.save()





class IMDBParser(object):

    base_url = 'http://www.imdb.com'

    def extract_imdb(self):

        bm = BoxOfficeMojoParser()
        four_months_ago = bm.four_months_ago()
        movies = models.Movie.objects.filter(Q(release_date__gte=four_months_ago) | Q(release_date__isnull=True))
        #iterate
        for m in movies :
            pic, created = models.Picture.objects.get_or_create(movie = m,description=m.title+' main image')
            if(created or pic.image is None):
                #post a search in imdb
                con = urllib2.urlopen(self.base_url+'/find?q='+m.title)
                data = con.read()
                bs = BeautifulSoup(data)

                #take first link (year match)
                #<a onclick="(new Image()).src='/rg/find-title-1/title_popular/images/b.gif?link=/title/tt0431021/';" href="/title/tt0431021/">The Possession</a>
                aas = bs.find_all('a')
                for a in aas:
                    if(a.get('href',None) is not None and a.text == m.title):
                        print(a['href'])
                        con2 = urllib2.urlopen(self.base_url+a['href'])
                        data2 = con2.read()
                        bs2 = BeautifulSoup(data2)
#                       <img height="317" itemprop="image" title="The Possession Poster" alt="The Possession Poster" style="max-width:214px; max-height:317px;" src="http://ia.media-imdb.com/images/M/MV5BMTc0NTcxMDU0MV5BMl5BanBnXkFtZTcwNTgwMzExOA@@._V1._SY317_.jpg">
                        img_tag = bs2.find("img",height="317", itemprop="image")
                        if(img_tag is not None and img_tag['src'] is not None):
                            #raw_data = urllib2.urlopen(img_tag['src']).read()
                            raw_data = NamedTemporaryFile(delete=True)
                            raw_data.write(urllib2.urlopen(img_tag['src']).read())
                            raw_data.flush()
                            pic.image.save(m.title+' main image.jpg', File(raw_data))


                            m.imdb_url = a['href']
                            pic.movie = m
                            pic.description = m.title+' main image'
                            pic.save()
                            m.save()
                            con2.close()
                con.close()
                time.sleep(random.randint(8, 15))











