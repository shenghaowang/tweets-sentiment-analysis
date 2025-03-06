from dataclasses import dataclass

from twikit.tweet import Tweet


@dataclass
class Post:
    """
    Post dataclass
    """

    created_at: str
    text: str
    retweet_count: int
    favorite_count: int
    reply_count: int
    quote_count: int

    @classmethod
    def from_object(cls, tweet: Tweet):
        return cls(
            created_at=tweet.created_at,
            text=tweet.text,
            retweet_count=tweet.retweet_count,
            favorite_count=tweet.favorite_count,
            reply_count=tweet.reply_count,
            quote_count=tweet.quote_count,
        )
