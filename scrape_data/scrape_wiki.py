import pandas as pd
import csv
import time
import os
import sys
sys.path.append(__file__)
from wiki_class import Wikimedia
from datetime import datetime

wikis = Wikimedia(driver_path = 'path.exe')

def backfill():
    # 20 years of data, wiki is structured differently prior to 2004
    for film_year in range(2004, int(datetime.now().year)+1):
        film_meta = wikis.scrape_data(film_year)

        # To be replaced with an S3 bucket at some point
        with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/data/wiki/wiki_film_list_{}.csv'.format(film_year), 'w', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Headers for the table returned
            writer.writerow(['Film', 'Production', 'Cast'])
            writer.writerows(row for row in film_meta)

        # Be gentle to the Wiki servers. Wikipedia needs your support: https://wikimediafoundation.org/news/2021/11/30/five-reasons-wikipedia-needs-your-support/
        time.sleep(1)

