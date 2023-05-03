import pandas as pd
import time
import csv
import os
import sys
sys.path.append(__file__)
from rotten_class import RottenTomatoes
from datetime import datetime

tomatoes = RottenTomatoes(driver_path = 'path.exe')

def film_review():
    for film in film_list:
        score, review = tomatoes.scrape_data(film)
        write_data(film, data=score, dtype='score', headers=['Film', 'Audience Score', 'Tomatometer Score'])
        write_data(film, data=review, dtype='review', headers=['Film', 'Critic', 'Publication', 'Review'])

        # Pause in place to reduce load on RT servers
        time.sleep(1)

def write_data(film, data, dtype, headers):
    # To be replaced with an S3 bucket at some point
    with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/data/RT/{}/{}_{}.csv'.format(dtype, film, dtype), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Headers for the table returned
        writer.writerow(headers)
        writer.writerows(row for row in data)
