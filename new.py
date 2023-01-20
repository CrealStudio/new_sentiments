import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "luna lang:en until:2022-06-01 since:2021-01-01"
tweets = []
limit = 100

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username,
         tweet.content])

data_frame = pd.DataFrame(tweets, columns=['Date', 'User', 'Content'])
print(data_frame)