import pandas as pd
import csv
import time
import sys
sys.path.append(__file__)
from wiki_class import Wikimedia

wikis = Wikimedia(driver_path = 'path.exe')

for film_year in range(2021, 2023):
    film_meta = wikis.scrape_data(film_year)

    with open('C:/Users/swgle/Desktop/Rotten Tomatoes Rater/output {}.csv'.format(film_year), 'w', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Headers for the table returned
        writer.writerow(['Film', 'Production', 'Cast'])
        writer.writerows(row for row in film_meta)

    #meta_data = pd.DataFrame(meta_data, columns=['Film', 'Production', 'Cast'])

    # Be gentle to the Wiki servers. Wikipedia needs your support: https://wikimediafoundation.org/news/2021/11/30/five-reasons-wikipedia-needs-your-support/
    time.sleep(1)

#meta_data = pd.DataFrame(meta_data, columns=['Film', 'Production', 'Cast'])
#print(meta_data)
