# encoding=utf8

import os

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB


def exec_main():
    data_dir = "./data"
    features_dir = "./features"

    # tweet_mixed_preprocessor.main()

    print("Loading data...")
    with open(os.path.join(features_dir, "text_emoji_news.txt"), "r") as f:
        x = f.readlines()

    with open(os.path.join(data_dir, "labels.txt"), "r") as f:
        y = np.array(f.readlines())

    print("Extract features...")
    x_feats = TfidfVectorizer().fit_transform(x)
    print(x_feats.shape)

    print("Start training and predict...")
    kf = KFold(n_splits=10)
    avg_p = 0
    avg_r = 0
    avg_f1 = 0
    tfidf_probs = np.empty([0, 3])

    for train, test in kf.split(x_feats):
        model = MultinomialNB().fit(x_feats[train], y[train])
        predicts = model.predict(x_feats[test])
        print(classification_report(y[test], predicts))
        avg_p += precision_score(y[test], predicts, average="macro")
        avg_r += recall_score(y[test], predicts, average="macro")
        avg_f1 += f1_score(y[test], predicts, average="macro")

        probs = model.predict_proba(x_feats[test])
        tfidf_probs = np.concatenate((tfidf_probs, probs))

    print("Average Precision is %f." % (avg_p / 10.0))
    print("Average Recall is %f." % (avg_r / 10.0))
    print("Average F1 score is %f." % (avg_f1 / 10.0))

    return tfidf_probs


if __name__ == "__main__":
    exec_main()
