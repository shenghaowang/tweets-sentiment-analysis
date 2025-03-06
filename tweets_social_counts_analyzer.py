import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
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

    print("Loading data...")
    x = []
    with open(os.path.join(features_dir, "social_counts.txt"), "r") as f:
        for i, line in enumerate(f):
            social_counts = [int(cnt) for cnt in line.split("\t")]
            x.append(social_counts)

    with open(os.path.join(data_dir, "labels.txt"), "r") as f:
        y = np.array([label.replace("\n", "") for label in f.readlines()])

    print("Start training and predict...")
    kf = KFold(n_splits=10)
    x_matrix = np.array(x)
    avg_p = 0
    avg_r = 0
    avg_f1 = 0
    social_cnt_probs = np.empty([0, 3])

    ## Develop classifier for tweet social counts
    for train, test in kf.split(x_matrix):
        model = RandomForestClassifier(
            n_estimators=500, max_features=6, random_state=0
        ).fit(x_matrix[train], y[train])
        # model = MultinomialNB().fit(x_matrix[train], y[train])
        predicts = model.predict(x_matrix[test])
        # print(classification_report(y[test],predicts))
        avg_p += precision_score(y[test], predicts, average="macro")
        avg_r += recall_score(y[test], predicts, average="macro")
        avg_f1 += f1_score(y[test], predicts, average="macro")

        probs = model.predict_proba(x_matrix[test])
        social_cnt_probs = np.concatenate((social_cnt_probs, probs))

    print("Average Precision is %f." % (avg_p / 10.0))
    print("Average Recall is %f." % (avg_r / 10.0))
    print("Average F1 score is %f." % (avg_f1 / 10.0))

    ## Develop classifier with the full dataset and print the variable importance measurements
    rf = RandomForestClassifier(n_estimators=1000, max_features=6, random_state=0).fit(
        x_matrix[train], y[train]
    )
    features = [
        "retweet count",
        "followers count",
        "friends_count",
        "listed_count",
        "favourites_count",
        "statuses_count",
    ]
    print("Features sorted by their score:")
    print(
        sorted(
            zip(map(lambda x: round(x, 4), rf.feature_importances_), features),
            reverse=True,
        )
    )
    # importances = rf.feature_importances_
    # indices = np.argsort(importances)
    # features = ['retweet count', 'followers count', 'friends_count', \
    # 			'listed_count', 'favourites_count', 'statuses_count']
    # plt.figure(1)
    # plt.title('Feature Importances')
    # plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    # plt.yticks(range(len(indices)), features[indices])
    # plt.xlabel('Relative Importance')

    return social_cnt_probs


if __name__ == "__main__":
    exec_main()
