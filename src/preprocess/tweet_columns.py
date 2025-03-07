from dataclasses import dataclass


@dataclass
class TweetColumns:
    post_id: str = "post_id"
    user_id: str = "user_id"
    created_at: str = "created_at"
    text: str = "text"
    retweet_count: str = "retweet_count"
    favorite_count: str = "favorite_count"
    reply_count: str = "reply_count"
    quote_count: str = "quote_count"
    hashtags: str = "hashtags"
    location: str = "location"
    place: str = "place"
    sentiment: str = "sentiment"
    risk_level: str = "risk_level"
