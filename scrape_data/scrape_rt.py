import pandas as pd
import sys
sys.path.append(__file__)
from rotten_class import RottenTomatoes

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