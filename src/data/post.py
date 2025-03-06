from dataclasses import dataclass
from typing import Any, Dict, List

from twikit.tweet import Tweet


@dataclass
class Post:
    """
    Post dataclass
    """

    post_id: str
    user_id: str
    created_at: str
    text: str
    retweet_count: int
    favorite_count: int
    reply_count: int
    quote_count: int
    hashtags: List[str]
    location: str
    place: Dict[str, Any]

    @classmethod
    def from_object(cls, tweet: Tweet):
        return cls(
            post_id=tweet.id,
            user_id=tweet.user.id,
            created_at=tweet.created_at,
            text=tweet.text,
            retweet_count=tweet.retweet_count,
            favorite_count=tweet.favorite_count,
            reply_count=tweet.reply_count,
            quote_count=tweet.quote_count,
            hashtags=tweet.hashtags,
            location=tweet.user.location,
            place=tweet.place,
        )
