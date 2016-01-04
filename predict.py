# attempt to classify a game into radiant or dire victory based purely on
# heroes picked in draft.

import numpy
import time
import pickle
from numpy import random
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import metrics

def unison_shuffle(a, b):
	# constant seed
	state = random.get_state()
	random.shuffle(a)
	random.set_state(state)
	random.shuffle(b)

# @param data_path: string of path to csv
# @param test_set_size: percentage of samples to use as a test set
# @return: tuple (X, y, Xt, yt) consisting of numpy arrays corresponding to
# 			features and targets of the training and test sets.
def preprocess(data_path, test_set_size):
	print("Preprocessing data set...")
	start_time = time.time()

	data = numpy.genfromtxt(data_path, delimiter=',')

	X = data[:,:224]
	y = data[:,224:]

	# shuffle then split X and y
	unison_shuffle(X, y)

	index = int(len(X) * test_set_size)
	Xt = X[0:index,:]
	yt = y[0:index,:]
	X = X[index:,:]
	y = y[index:,:]

	y = numpy.ravel(y)

	end_time = time.time()
	print("Completed in " + str(end_time - start_time) + " seconds.")

	return (X, y, Xt, yt)

# fits a model to the given data set
def train(X, y):
	print("Training model...")
	start_time = time.time()

	# model = GradientBoostingClassifier()
	# model = SVC()
	# model = LinearSVC(penalty='l2', loss='squared_hinge', C=2)
	# model = BernoulliNB()
	model = MultinomialNB()
	# model = KNeighborsClassifier(n_neighbors=5)
	# model = DecisionTreeClassifier(random_state=0)
	model.fit(X, y)

	pickle.dump(model, open('model.mdl', 'wb'))

	end_time = time.time()
	print("Completed in " + str(end_time - start_time) + " seconds.")
	return model

# tests the model given a test set and true values for their corresponding targets.
# outputs a prediction results file.
def test(model, Xt, yt):
	print("Testing model...")
	start_time = time.time()

	preds = model.predict(Xt)

	# metrics
	report = metrics.classification_report(yt, preds)
	confusion_matrix = metrics.confusion_matrix(yt, preds)
	r_squared = metrics.r2_score(yt, preds)

	print("Classification report:\n%s\n" % report)
	print("Confusion matrix:\n%s" % confusion_matrix)
	print("R2:\n%s" % r_squared)

	output = open('classification_report.txt', 'w', newline='')
	output.write(str(report) + '\n\n')
	output.write(str(confusion_matrix) + '\n')
	output.write(str(r_squared) + '\n')
	output.close()

	end_time = time.time()
	print("Completed in " + str(end_time - start_time) + " seconds.")


if __name__ == '__main__':
	X, y, Xt, yt = preprocess('draft-victory.csv', 0.2)
	model = train(X, y)
	test(model, Xt, yt)