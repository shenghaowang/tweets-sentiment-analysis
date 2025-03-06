import re

import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")


def rm_html_tags(text: str) -> str:
    html_prog = re.compile(r"<[^>]+>", re.S)
    return html_prog.sub("", text)


def rm_html_escape_characters(text: str) -> str:
    pattern_str = (
        r"&quot;|&amp;|&lt;|&gt;|&nbsp;|&#34;|&#38;|&#60;|&#62;|&#160;|"
        r"&#20284;|&#30524;|&#26684;|&#43;|&#20540;|&#23612;"
    )
    escape_characters_prog = re.compile(pattern_str, re.S)
    return escape_characters_prog.sub("", text)


def rm_at_user(text: str) -> str:
    return re.sub(r"@[a-zA-Z_0-9]*", "", text)


def rm_url(text: str) -> str:
    return re.sub(r"http[s]?:[/+]?[a-zA-Z0-9_\.\/]*", "", text)


def rm_repeat_chars(text: str) -> str:
    return re.sub(r"(.)(\1){2,}", r"\1\1", text)


def rm_hashtag_symbol(text: str) -> str:
    return re.sub(r"#", "", text)


def rm_time(text: str) -> str:
    return re.sub(r"[0-9][0-9]:[0-9][0-9]", "", text)


def rm_emojis(text: str) -> str:
    return emoji.replace_emoji(text, replace="")


def rm_stopwords(text: str) -> str:
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])


def pre_process(text: str) -> str:
    text = text.lower()
    text = rm_url(text)
    text = rm_at_user(text)
    text = rm_repeat_chars(text)
    text = rm_hashtag_symbol(text)
    text = rm_time(text)
    text = rm_emojis(text)

    return text
