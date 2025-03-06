CN4242 Lab 2: Sentiment Analysis of Microblog Streams
Student: A0105772H

## Usage of tweet classifier
1. Open terminal (Ubuntu/Mac) or command line prompt (Windows).
2. Check the current version of Python. Ensure that Python 3 is in use.
3. Redirect to the project folder: "tweet-sentiment-analysis".
4. Run the following command to prepare the tweet features for sentiment analysis.
python tweet_mixed_preprocessor.py
5. Type "python" plus the script name of the analyzer to perform classification. Press Enter key to execute the script.
e.g. "python tweets_late_fusion_analyzer.py",  "python tweets_vader_sentiment_analyzer.py".
6. There are 5 analyzers available:
Level 0: "tweets_vader_sentiment_analyzer.py", "tweets_tfidf_sentiment_analyzer.py", "tweets_social_counts_analyzer.py"
Level 1: "tweets_late_fusion_analyzer.py"


## Remarks
1. Take note that the classifier scripts are written in Python 3.
2. The titles of relevant webpage from expanded urls are scraped with the Scrapy library. The project files are kept in the folder of "tweet_context".
