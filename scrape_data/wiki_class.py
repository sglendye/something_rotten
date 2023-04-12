# Import the selenium library and the webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class Wikimedia:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(driver_path)

    def scrape_data(self, year):
        # See if the web page exists, if not, skip this one
        try:
            self.driver.get("https://en.wikipedia.org/wiki/List_of_American_films_of_{}".format(str(year)))
        except:
            return None
        
        # Find all the elements with the class name "wikitable"
        tables = self.driver.find_elements(By.CLASS_NAME, "wikitable")
        tables = tables[1:] # The first table is top grossing films of the year. While interesting, these films already exist in the tables below

        # Storage location for all of the lists of table data
        film_meta = []

        # Nested, nested, nested...
        for table in tables:
            # Find all the rows in the table body
            rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
            for row in rows:
                # Don't forget that you need the table data... in the table row... in the table itself...
                cells = row.find_elements(By.TAG_NAME, "td")

                # Note: Intentionally not collecting table rows with fewer than 4 elements.
                # This would be the warning rows about no films being produced during covid
                if len(cells) == 5:
                    film = cells[1].text
                    production = cells[2].text
                    cast = cells[3].text
                elif len(cells) == 4:
                    film = cells[0].text
                    production = cells[1].text
                    cast = cells[2].text

                film_meta.append([film, production, cast])

        return film_meta

wikis = Wikimedia(driver_path = 'path.exe')
meta_data = []
for i in range(2021, 2023):
    # Be gentle to the Wiki servers. Wikipedia needs your support: https://wikimediafoundation.org/news/2021/11/30/five-reasons-wikipedia-needs-your-support/
    time.sleep(1)
    film_meta = wikis.scrape_data(i)
    meta_data.extend(film_meta)

meta_data = pd.DataFrame(meta_data, columns=['Film', 'Production', 'Cast'])
print(meta_data)

