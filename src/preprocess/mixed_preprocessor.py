# encoding=utf8
import csv
import os
import pickle
import re
import sys

import emoji
import numpy as np

# import nltk
# nltk.download()
# from nltk.corpus import stopwords
import simplejson as json

# reload(sys)
# sys.setdefaultencoding('utf8')




def rm_html_tags(str):
    html_prog = re.compile(r"<[^>]+>", re.S)
    return html_prog.sub("", str)


def rm_html_escape_characters(str):
    pattern_str = r"&quot;|&amp;|&lt;|&gt;|&nbsp;|&#34;|&#38;|&#60;|&#62;|&#160;|&#20284;|&#30524;|&#26684|&#43;|&#20540|&#23612;"
    escape_characters_prog = re.compile(pattern_str, re.S)
    return escape_characters_prog.sub("", str)


def rm_at_user(str):
    return re.sub(r"@[a-zA-Z_0-9]*", "", str)


def rm_url(str):
    return re.sub(r"http[s]?:[/+]?[a-zA-Z0-9_\.\/]*", "", str)


def rm_repeat_chars(str):
    return re.sub(r"(.)(\1){2,}", r"\1\1", str)


def rm_hashtag_symbol(str):
    return re.sub(r"#", "", str)


def rm_time(str):
    return re.sub(r"[0-9][0-9]:[0-9][0-9]", "", str)


def split_emojis(str):
    text_part = "".join(c for c in str if c not in emoji.UNICODE_EMOJI)
    emoji_part = " ".join(c for c in str if c in emoji.UNICODE_EMOJI)
    return text_part + " " + emoji_part


def pre_process(str):
    # do not change the preprocessing order only if you know what you're doing
    # str = str.lower()
    str = rm_url(str)
    str = rm_at_user(str)
    str = rm_repeat_chars(str)
    str = rm_hashtag_symbol(str)
    str = rm_time(str)
    # str = emoji.demojize(str, delimiters=(' emoji_', ' '))
    str = split_emojis(str)

    return str


if __name__ == "__main__":
    data_dir = "./data"  ##Setting your own file path here.
    features_dir = "./features"
    context_dir = "./tweet_context"

    x_filename = "context.csv"
    y_filename = "tweets.txt"

    ## Load and process samples
    print("start loading and process samples...")
    tweets = []
    expanded_urls = []
    social_counts = []

    ## Import tweet contexts
    with open(os.path.join(context_dir, x_filename), mode="r") as f_context:
        reader = csv.reader(f_context)
        context_dict = {rows[1]: rows[0] for rows in reader}
        print(context_dict["2793"])

    with open(os.path.join(data_dir, y_filename)) as f:
        for i, line in enumerate(f):
            tweet_obj = json.loads(line.strip(), encoding="utf-8")
            content = tweet_obj["text"].replace("\n", " ")
            key = str(i + 1)
            if key in context_dict.keys():
                title = context_dict[key].strip().replace("\n", " ").replace("\t", " ")
                title_words = title.split()
                text_words = content.split()
                for word in title_words:
                    if word not in text_words:
                        content += word
            postprocess_tweet = pre_process(content)
            tweets.append(postprocess_tweet)

            no_of_urls = len(tweet_obj["entities"]["urls"])
            if no_of_urls > 0:
                expanded_urls.append(
                    str(i + 1) + "\t" + tweet_obj["entities"]["urls"][0]["expanded_url"]
                )

            ## Collect relevant counts of social features
            retweet_cnt = tweet_obj["retweet_count"]
            followers_cnt = tweet_obj["user"]["followers_count"]
            friends_cnt = tweet_obj["user"]["friends_count"]
            listed_cnt = tweet_obj["user"]["listed_count"]
            favourites_cnt = tweet_obj["user"]["favourites_count"]
            statuses_cnt = tweet_obj["user"]["statuses_count"]
            social_counts_list = [
                str(retweet_cnt),
                str(followers_cnt),
                str(friends_cnt),
                str(listed_cnt),
                str(favourites_cnt),
                str(statuses_cnt),
            ]
            social_counts.append("\t".join(social_counts_list))

    ## Re-process samples, filter low frequency words...
    fout = open(os.path.join(features_dir, "text_emoji_news.txt"), "w")
    print(len(tweets))
    for tweet in tweets:
        tweet = tweet.replace("\n", " ").replace("\r", "")
        fout.write("%s\n" % tweet)
    fout.close()

    fcnt = open(os.path.join(features_dir, "social_counts.txt"), "w")
    for cnt in social_counts:
        fcnt.write("%s\n" % cnt)
    fcnt.close()

    with open(os.path.join(context_dir, "expanded_urls.txt"), "w") as furl:
        for expanded_url in expanded_urls:
            furl.write("%s\n" % expanded_url)
        furl.close()

    print("Preprocessing is completed")
