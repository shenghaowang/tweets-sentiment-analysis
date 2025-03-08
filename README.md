# Tweet Sentiment Analysis

## Installation
Python >3.10 is recommended.

```
python -m venv x_env
source x_env/bin/activate
pip install -r requirements.txt
pre-commit install
```

An X account needs to be registered to extract the microblogs data. The credentials of the X account needs to be provided in the [config file](config/config.yaml).

## Usage

1. Extract Tweet Messages with a Specific Query
To extract tweet messages based on a specific query, a query needs to be provided in the [config file](config/config.yaml).

Initial Setup: On the first run, the login option must be set to `True`. This will initiate the login process.
```
export PYTHONPATH=src
python src/data/main.py login=True  # Set login=True on the first run
```

Subsequent Runs: After logging in, set `login=False` to skip the login process for future runs.
```
export PYTHONPATH=src
python src/data/main.py login=False  # Set to False after first login
```

2. Classify Posts by Sentiment and Risk Level
Once the tweet messages are extracted, the posts can be classified based on sentiment and risk level. Run the following command to perform sentiment and risk classification:
```
export PYTHONPATH=src
python src/sentiment_risk/main.py
```
This will output the sentiment and risk levels of the posts to csv files.

3. Identify Location from Posts and Plot Heatmap
To identify the location from the posts and generate a heatmap, execute:
```
export PYTHONPATH=src
python src/geolocation/main.py
```
This script will extract geolocation and generate a heatmap visualizing the locations of the posts.

## Extracted tweet messages
* [Raw messages in json format](raw/)
* [Processed tweet messages](data/tweets.csv)

## Results from the analysis
* [Tweets distribution by sentiment](data/distribution_by_sentiment.csv)
* [Tweets distribution by crisis risk level](data/distribution_by_risk_level.csv)
* [Tweets distribution by geo-location](data/distribution_by_location.csv)
* [Heatmap of crisis-related posts](data/heatmap.png)
