import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from joblib import dump,load
import pickle


# CALL PassStrength along with the password to be tested as parameter.
# If list of passwords are given result is also list of classes.


def getTokens(inputString): #custom tokenizer. ours tokens are characters rather than full words
	tokens = []
	for i in inputString:
		tokens.append(i)
	return tokens

def PassStrength(password):
	lgs = load('pass6.joblib')
	# print("Model loaded!!!")
	vec = pickle.load(open('vectoriser6.pkl', 'rb'))
	x_predict = vec.transform([password])
	y_predict = lgs.predict(x_predict)
	# print(y_predict)
	result = []
	for i in y_predict:
		if(i==0):
			result.append('Weak')
		elif(i==1):
			result.append('Medium')
		else:
			result.append('Strong')
	# return result[0]
	print(result[0])

PassStrength("abcdef131!@#d")