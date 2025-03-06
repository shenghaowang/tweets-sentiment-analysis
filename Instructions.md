Lab 2: Sentiment Analysis
Deadline: 5 Mar 2018(Mon, 1800 Hrs)

### Introduction to DATASET
This dataset contains tweets with following 3 sentiment classes:
0. negative
1. neutral
2. positive

The total size of dataset is about 5,000 tweets. The tweets are in json format and organised as each one a line in ./data/tweets.txt. The groundtruth of these tweets is provided in ./data/labels.txt.

The tweet data is in json format, which contains all available information provided by Twitter.
For details about the definition of each field, please refer to https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.
For better visualization, you can utilize online json editor tool (http://jsoneditoronline.org/).
If you need to get more information (e.g., comments, images, social relations), you could use the Twitter API: https://developer.twitter.com/

sentiment_lexicon.txt: the file is tab delimited with TOKEN, MEAN-SENTIMENT-RATING, STANDARD DEVIATION, and RAW-HUMAN-SENTIMENT-RATINGS
The current algorithm makes immediate use of the first two elements (token and mean valence).


### Policy
This dataset contains original data crawled from Twitter.
Due to privacy issues, please do not public this dataset to anyone or for any use outside the class. Thank you.


### Environment Setting
1. Ubuntu 16.04
2. Python 2.7

### Set up Python 2 Environment with Anaconda
1. conda create -n py27 python=2.7
2. source activate py27
3. source deactivate

### Installation
1. nltk
2. simplejson
3. pickle
4. numpy
5. scipy
6. scikit-learn
Note: All these libraries can be installed via pip. (e.g., pip install nltk)



### Usage
1. Run './Step1_preprocess.py' to prepocess tweet content, including data cleaning (e.g., remove url, time).
2. Run 'Step2_basic_sentiment_analyzer.py', which leverages sentiment lexicon. You are supposed to see performances (classification score, average percision, average recall) printing into the screen.
