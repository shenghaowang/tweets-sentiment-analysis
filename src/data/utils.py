import json
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from random import randint
from typing import Any, Dict, List

from loguru import logger
from twikit import Client
from twikit.tweet import Tweet
from twikit.utils import Result

from data.post import Post


def search(client: Client, query: str, tweets: Result[Tweet] = None) -> Result[Tweet]:
    """
    Search for tweets based on a given query

    Args:
        client (Client): Twikit client
        query (str): query to be used for searching tweets
        tweets (Result[Tweet], optional): search results. Defaults to None.

    Returns:
        Result[Tweet]: _description_
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
    """

    Args:
        query (str): _description_

    Returns:
        str: _description_
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'{query.replace(" ", "_")}_{timestamp}.csv'


def export(file_path: Path, tweets: Result[Tweet], attributes: List[str]) -> None:
    """

    Args:
        file_path (str): _description_
        tweets (Result[Tweet]): _description_
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
    """

    Args:
        tweet (Tweet): _description_
        attributes (List[str]): _description_

    Returns:
        dict: _description_
    """
    res = Post.from_object(tweet)

    return asdict(res)
