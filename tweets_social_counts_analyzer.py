import os
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

def exec_main():
	data_dir = './data'
	features_dir = './features'

	print("Loading data...")
	x = []
	with open(os.path.join(features_dir, 'social_counts.txt'), 'r') as f:
		for i, line in enumerate(f):
			social_counts = [int(cnt) for cnt in line.split('\t')]
			x.append(social_counts)

	with open(os.path.join(data_dir, 'labels.txt'), 'r') as f:
		y = np.array([label.replace('\n', '') for label in f.readlines()])

	print("Start training and predict...")
	kf = KFold(n_splits=10)
	x_matrix = np.array(x)
	avg_p = 0
	avg_r = 0
	avg_f1 = 0
	social_cnt_probs = np.empty([0, 3])

	## Develop classifier for tweet social counts
	for train, test in kf.split(x_matrix):
		model = RandomForestClassifier(n_estimators = 500, max_features = 6, \
					random_state=0).fit(x_matrix[train], y[train])
		# model = MultinomialNB().fit(x_matrix[train], y[train]) 
		predicts = model.predict(x_matrix[test])
		# print(classification_report(y[test],predicts))
		avg_p += precision_score(y[test],predicts, average='macro')
		avg_r += recall_score(y[test],predicts, average='macro')
		avg_f1 += f1_score(y[test],predicts, average='macro')

		probs = model.predict_proba(x_matrix[test])
		social_cnt_probs = np.concatenate((social_cnt_probs, probs))

	print('Average Precision is %f.' %(avg_p/10.0))
	print('Average Recall is %f.' %(avg_r/10.0))
	print('Average F1 score is %f.' %(avg_f1/10.0))

	return social_cnt_probs

if __name__ == '__main__':
    exec_main()