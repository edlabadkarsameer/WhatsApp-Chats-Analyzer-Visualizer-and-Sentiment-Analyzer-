import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

text = "this app is bogus"

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Analyze the sentiment of the text
sentiment = sia.polarity_scores(text)

# Print the sentiment scores
print(sentiment)
