from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

class Wikimedia:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(driver_path)

    def scrape_data(self, year):
        url = "https://en.wikipedia.org/wiki/List_of_American_films_of_{}".format(str(year))  
        isReal = self.reality_check(self, url)
        if isReal:

            # All elements with the class name "wikitable"
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
                    # These would be the warning rows about no films being produced during covid
                    if len(cells) == 5:
                        film = cells[1].text
                        production = cells[2].text
                        cast = cells[3].text
                        film_meta.append([film, production, cast])

                    elif len(cells) == 4:
                        film = cells[0].text
                        production = cells[1].text
                        cast = cells[2].text
                        film_meta.append([film, production, cast])

            return film_meta
    
    def reality_check(self, url):
        isReal = requests.get(url)
        if isReal.status_code == 200:
            return True
        else:
            return False
