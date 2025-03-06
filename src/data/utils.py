import json
import re
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Any, Dict

from loguru import logger
from twikit import Client
from twikit.tweet import Tweet
from twikit.utils import Result

from data.post import Post


def search(client: Client, query: str, tweets: Result[Tweet] = None) -> Result[Tweet]:
    """Search for tweets based on a given query

    Parameters
    ----------
    client : Client
        Twikit client
    query : str
        query to be used for searching tweets
    tweets : Result[Tweet], optional
        search results, by default None

    Returns
    -------
    Result[Tweet]
        Tweets relevant to the given query
    """
    if tweets is None:
        logger.info(f"{datetime.now()} - Getting tweets...")
        tweets = client.search_tweet(query=query, product="Top")

    else:
        wait_time = randint(5, 10)
        logger.info(
            f"{datetime.now()} - Getting next tweets after {wait_time} seconds ..."
        )
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


def get_tweets_filename(query: str) -> str:
    """Get the name of the file for storing tweets

    Parameters
    ----------
    query : str
        query used for searching tweets

    Returns
    -------
    str
        name of the file for storing tweets
    """
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{query.replace(" ", "_")}_{timestamp}.json'


def export(file_path: Path, tweets: Result[Tweet]) -> None:
    """Write tweets to a JSON file

    Parameters
    ----------
    file_path : Path
        file path for saving tweets
    tweets : Result[Tweet]
        search results
    """
    # Initialize output file if it does not exist
    if not file_path.exists():
        with open(file_path, "w") as file:
            json.dump([], file, indent=4)

    # Read existing tweets from the file
    with open(file_path, "r") as file:
        data = json.load(file)

    data.extend([parse_tweet(tweet) for tweet in tweets])
    logger.debug(f"Number of tweets: {len(data)}")

    # Write the updated list back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def parse_tweet(tweet: Tweet) -> Dict[str, Any]:
    """Extract relevant attributes from a tweet instance

    Parameters
    ----------
    tweet : Tweet
        Tweet object

    Returns
    -------
    Dict[str, Any]
        Dictionary containing tweet attributes
    """
    res = Post.from_object(tweet)

    return asdict(res)
