import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    logger.debug(OmegaConf.to_container(cfg))


if __name__ == "__main__":
    main()
