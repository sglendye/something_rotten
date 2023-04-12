# Import the selenium library and the webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create a webdriver instance using Chrome
driver = webdriver.Chrome()

# Navigate to the web page
driver.get("https://en.wikipedia.org/wiki/List_of_American_films_of_2020")

# Find all the elements with the class name "wikitable"
tables = driver.find_elements(By.CLASS_NAME, "wikitable")
tables = tables[1:] # The first table is top grossing films of the year. While interesting, these films already exist in the tables below

results = []

# Loop through each table
for table in tables:
    # Find all the rows in the table body
    rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    # Loop through each row
    for row in rows:
        
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

        results.append([film, production, cast])

print(results)
#print(films)
# Close the driver
driver.close()
