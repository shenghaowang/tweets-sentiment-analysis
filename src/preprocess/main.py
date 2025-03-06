import json
from pathlib import Path

import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf


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


if __name__ == "__main__":
    main()
