#!/usr/bin/env python
import os
import sys
import time

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings_dev")
    #from django.core.management import execute_from_command_line
    #execute_from_command_line(sys.argv)

    from machineapp import parser

    print ("starting cron")
#    for x in range(0, 100):
    imdb = parser.IMDBParser()
    imdb.extract_imdb()

    bo = parser.BoxOfficeMojoParser()
    bo.seed_movies_database()
    bo.parse_daily()
    #
    #imdb = parser.IMDBParser()
    #imdb.extract_imdb()
    #        time.sleep(78000)