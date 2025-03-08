import time

import hydra
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from tqdm import tqdm

from geolocation.analysis import get_geocode, identify_location
from preprocess.tweet_columns import TweetColumns

tqdm.pandas()


@hydra.main(version_base=None, config_path="../../config", config_name="config")
def main(cfg: DictConfig) -> None:
    logger.debug(OmegaConf.to_container(cfg))

    # Load processed tweets
    tweets_df = pd.read_csv(cfg.processed_filepath)

    # Handle missing columns
    tweet_cols = TweetColumns()
    for col in (tweet_cols.text, tweet_cols.location, tweet_cols.hashtags):
        tweets_df[col] = tweets_df[col].fillna("")
        tweets_df[col] = tweets_df[col].astype(str)

    # Classify by location
    tweets_df[tweet_cols.valid_location] = tweets_df.progress_apply(
        lambda row: identify_location(
            row[tweet_cols.location] + row[tweet_cols.hashtags] + row[tweet_cols.text]
        ),
        axis=1,
    )
    location_counts_df = (
        tweets_df[tweet_cols.valid_location].value_counts().reset_index()
    )
    location_counts_df.columns = ["location", "count"]
    logger.info(f"Distribution of posts by valid location: \n{location_counts_df}")
    location_counts_df.to_csv(
        cfg.distribution_filepath.location, index=True, header=True
    )

    # Plot heatmap for the top 20 locations
    geocode_data = []
    for _, row in location_counts_df[:20].iterrows():
        lat, lng = get_geocode(row["location"])
        geocode_data.append((lat, lng, row["location"], row["count"]))

        # There is a rate limit of 1 request per second.
        time.sleep(2)

    geocode_df = pd.DataFrame(
        data=geocode_data, columns=["latitude", "longitude", "location", "count"]
    )
    logger.info(f"Geocode data: \n{geocode_df}")

    fig = px.density_mapbox(
        geocode_df,
        lat="latitude",
        lon="longitude",
        z="count",  # The intensity of the heatmap
        radius=30,  # Adjust the radius for heat intensity
        # center={"lat": 37.0902, "lon": -95.7129},  # Centered around the USA
        zoom=1,
        mapbox_style="carto-positron",
    )

    fig.add_trace(
        go.Scattermapbox(
            lat=geocode_df["latitude"],  # Germany, France
            lon=geocode_df["longitude"],
            mode="text",
            text=geocode_df["location"],
            textfont={"size": 14, "color": "black"},
        )
    )

    fig.show()

    pio.write_image(
        fig, cfg.distribution_filepath.heatmap, width=1600, height=1200, scale=2
    )


if __name__ == "__main__":
    main()
