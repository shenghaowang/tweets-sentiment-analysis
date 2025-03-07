import asyncio
import json
import time
from datetime import datetime
from pathlib import Path

import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from twikit import Client, TooManyRequests

from data.utils import export, get_tweets_filename, search


async def extract_tweets(cfg: DictConfig) -> None:

    client = Client(language="en-US")
    if isinstance(cfg.login, bool) and cfg.login:

        await client.login(
            auth_info_1=cfg.username, auth_info_2=cfg.email, password=cfg.password
        )
        client.save_cookies("cookies.json")
        logger.debug("Logged in")

    client.load_cookies("cookies.json")

    count = 0
    tweets = None

    # Initialize output file
    output_file = Path(cfg.raw_dir) / get_tweets_filename(cfg.query)
    with open(output_file, "w") as f:
        json.dump([], f, indent=4)

    while count < cfg.max_tweets:
        try:
            tweets = await search(client=client, query=cfg.query, tweets=tweets)

        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            logger.warning(
                f"{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}"
            )

            wait_time = rate_limit_reset - datetime.now()
            time.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            logger.info(f"{datetime.now()} - No more tweets found")
            break

        # Save tweets to file
        export(file_path=output_file, tweets=tweets)
        count += len(tweets)
        logger.info(f"{datetime.now()} - {count} tweets saved to {output_file}")


@hydra.main(version_base=None, config_path="../../config", config_name="config")
def main(cfg: DictConfig) -> None:
    logger.debug(OmegaConf.to_container(cfg))
    asyncio.run(extract_tweets(cfg))


if __name__ == "__main__":
    main()
