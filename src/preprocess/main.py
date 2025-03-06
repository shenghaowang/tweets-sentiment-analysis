import json
from pathlib import Path

import hydra
import pandas as pd
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from preprocess.tweet_columns import TweetColumns
from preprocess.utils import process_tags, process_text


@hydra.main(version_base=None, config_path="../../config", config_name="data")
def main(cfg: DictConfig) -> None:
    logger.debug(OmegaConf.to_container(cfg))

    raw_dir = Path(cfg.raw_dir)
    raw_files = raw_dir.glob("*.json")
    tweets = []
    for file in raw_files:
        logger.debug(f"Processing {file}")

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            tweets.extend(data)

    logger.info(f"Number of tweets: {len(tweets)}")

    # Convert tweets to dataframe
    tweets_df = pd.DataFrame(tweets)

    # Process text and hashtags
    tweet_cols = TweetColumns()
    tweets_df[tweet_cols.text] = tweets_df[tweet_cols.text].apply(process_text)
    tweets_df[tweet_cols.hashtags] = tweets_df[tweet_cols.hashtags].apply(process_tags)
    logger.debug(f"\n{tweets_df.head()}")

    # Remove duplicate tweets
    tweets_df = tweets_df.drop_duplicates(
        subset=[tweet_cols.post_id, tweet_cols.user_id], keep="first"
    )

    # Write processed tweets to file
    tweets_df.to_csv(cfg.processed_filepath, index=False)
    logger.info(f"{tweets_df.shape[0]} tweets written to {cfg.processed_filepath}")


if __name__ == "__main__":
    main()
