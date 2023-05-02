import pandas as pd
import selenium
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class RottenTomatoes:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(driver_path)

    def scrape_data(self, film):
        
        url = self.generate_url(film)

        isReal = self.reality_check(url)
        if isReal:
            scores = self.rotten_scores(url)
            reviews = self.rotten_reviews(url)
            
            # Let's only average 1 request per second to spare the poor RT servers
            time.sleep(3)

        self.driver.close()
        return scores, reviews

    def reality_check(self, url):
        isReal = requests.get(url)
        if isReal.status_code == 200:
            return True
        else:
            return False

    def generate_url(self, film):
        url = film.replace(".", "").replace(",", "").replace("'", "").replace(":", "").replace("&", "and").replace(" ", "_")
        url = url.lower()
        url = 'https://www.rottentomatoes.com/m/'+url
        return url

    def rotten_scores(self, url):
        self.driver.get(url)
        tomatometer_container = self.driver.find_elements(By.XPATH,'//score-board')
        film = url.split('/')[-1]
        audience = tomatometer_container[0].get_attribute('audiencescore')
        tomatometer = tomatometer_container[0].get_attribute('tomatometerscore')

        return [film, audience, tomatometer]

    def rotten_reviews(self, url):
        self.driver.get(url+'/reviews?type=top_critics')
        film = url.split('/')[-1]
        critics = self.driver.find_elements(By.CSS_SELECTOR, '.reviewer-name-and-publication .display-name')
        publications = self.driver.find_elements(By.CSS_SELECTOR, '.reviewer-name-and-publication .publication')
        review_text = self.driver.find_elements(By.CLASS_NAME, "review-text")
        
        return [film, critics[0].text, publications[0].text, review_text[0].text]

    def test(self):
        # Test generate_url method
        assert self.generate_url("The Shawshank Redemption") == "https://www.rottentomatoes.com/m/the_shawshank_redemption"
        
        # Test reality_check method
        assert self.reality_check("https://www.rottentomatoes.com/m/the_shawshank_redemption") == True

tomatoes = RottenTomatoes(driver_path = 'path.exe')

scores = []
reviews = []
for i in ['High School Musical']:
    score, review = tomatoes.scrape_data(i)
    scores.append(score)
    reviews.append(review)

scores = pd.DataFrame(scores, columns=['Film', 'Audience Score', 'Tomatometer Score'])
reviews = pd.DataFrame(reviews, columns=['Film', 'Critic', 'Publication', 'Review'])

print(scores)
print(reviews)