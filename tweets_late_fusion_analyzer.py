# encoding=utf8

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

import tweets_vader_sentiment_analyzer
import tweets_social_counts_analyzer
import tweets_tfidf_sentiment_analyzer

vader_probs = np.array(tweets_vader_sentiment_analyzer.exec_main())
social_cnt_probs = tweets_social_counts_analyzer.exec_main()
tfidf_probs = tweets_tfidf_sentiment_analyzer.exec_main()
data_dir = './data'

print(vader_probs.shape)
print(social_cnt_probs.shape)
print(tfidf_probs.shape)

with open(os.path.join(data_dir, 'labels.txt'), 'r') as f_labels:
	y = np.array(f_labels.readlines())

## Generate multiple sets of weights for vader, tfidf, and social counts predictions
w_vader_range = np.arange(0.0, 0.6, 0.01)
w_tfidf_range = np.arange(0, 0.4, 0.01)
weight_sets = []

for w_tfidf in w_tfidf_range:
	for w_vader in w_vader_range:
		weight_sets.append([w_vader, w_tfidf, 1 - w_vader - w_tfidf])

## Search for optimal weights to be assigned to individual classifier
y_num = np.array([int(cls[:-1]) for cls in y])
precisions = []
recalls = []
f1_scores = []

for i in range(len(weight_sets)):
	w_vader, w_tfidf, w_social_cnts = weight_sets[i]
	combined_prob = w_vader * vader_probs + w_tfidf * tfidf_probs + w_social_cnts * social_cnt_probs
	combined_pred = np.apply_along_axis(np.argmax, 1, combined_prob)

	avg_p = precision_score(y_num, combined_pred, average='macro')
	avg_r = recall_score(y_num, combined_pred, average='macro')
	avg_f1 = f1_score(y_num, combined_pred, average='macro')

	precisions.append(avg_p)
	recalls.append(avg_r)
	f1_scores.append(avg_f1)

opt_id = np.argmax(f1_scores)
print(weight_sets[opt_id])
print('Optimal Precision is %f.' %precisions[opt_id])
print('Optimal Recall is %f.' %recalls[opt_id])
print('Optimal F1 Score is %f.' %f1_scores[opt_id])
