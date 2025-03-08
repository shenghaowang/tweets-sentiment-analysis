import hydra
import pandas as pd
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

from preprocess.tweet_columns import TweetColumns
from sentiment_risk.classifier import TweetClassifier

tqdm.pandas()


@hydra.main(version_base=None, config_path="../../config", config_name="config")
def main(cfg: DictConfig) -> None:
    logger.debug(OmegaConf.to_container(cfg))

    # Load processed tweets
    tweets_df = pd.read_csv(cfg.processed_filepath)

    # Handle missing columns
    tweet_cols = TweetColumns()
    tweets_df[tweet_cols.text] = tweets_df[tweet_cols.text].fillna("")
    tweets_df[tweet_cols.text] = tweets_df[tweet_cols.text].astype(str)

    # Classify by sentiment
    classifier = TweetClassifier()
    tweets_df[tweet_cols.sentiment] = tweets_df[tweet_cols.text].progress_apply(
        classifier.classify_sentiment
    )
    logger.info(
        f"Distribution of posts by sentiment: \n{tweets_df[tweet_cols.sentiment].value_counts()}"
    )
    tweets_df[tweet_cols.sentiment].value_counts().to_csv(
        cfg.distribution_filepath.sentiment, index=True, header=True
    )

    # Classify by risk level
    tweets_df[tweet_cols.risk_level] = tweets_df[tweet_cols.text].progress_apply(
        classifier.classify_risk
    )
    logger.info(
        f"Distribution of posts by risk level: \n{tweets_df[tweet_cols.risk_level].value_counts()}"
    )
    tweets_df[tweet_cols.risk_level].value_counts().to_csv(
        cfg.distribution_filepath.risk_level, index=True, header=True
    )


if __name__ == "__main__":
    main()
