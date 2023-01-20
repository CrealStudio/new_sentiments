import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import pipeline
limit = 1000

# Creating a list to append all tweet
tweets = []

# Creating query
query = "luna lang:en until:2022-06-01 since:2021-01-01"
q = sntwitter.TwitterSearchScraper(query)
# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(q.get_items()):
    if i>limit:
        break
    else:
        tweets.append([tweet.date, tweet.user, tweet.content])

# Converting data to dataframe
tweets_df = pd.DataFrame(tweets, columns=["Date", "User", "Tweet"])
#tweets_df.head()



sentiment_analysis = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment-latest")

# Creating a list to append all tweet attributes(data)
tweet_analysed = []

# Creating query

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# Predicting the sentiments of tweets
for i,tweet in enumerate(q.get_items()):
    if i>limit:
        break
    else:
        content = tweet.content
        content = preprocess(content)
        sentiment = sentiment_analysis(content)
        tweet_analysed.append({ "Date": tweet.date, 
                                "Tweet": tweet.content,
                                'Sentiment': sentiment[0]['label']})

pd.set_option('max_colwidth', None)

# Converting data to dataframe
data_frame = pd.DataFrame(tweet_analysed)
data_frame.head()
#Saving the data in a csv file
data_frame.to_csv('tweets.csv')