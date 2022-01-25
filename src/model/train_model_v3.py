import nltk
from underthesea import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from keras.utils.np_utils import to_categorical
# things we need for Tensorflow
import numpy as np
import tensorflow as tf
import keras
from tensorflow import keras
from tensorflow.keras import layers
import random
import pickle
import json
import re

patterns = {
	'[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
	'[đ]': 'd',
	'[èéẻẽẹêềếểễệ]': 'e',
	'[ìíỉĩị]': 'i',
	'[òóỏõọôồốổỗộơờớởỡợ]': 'o',
	'[ùúủũụưừứửữự]': 'u',
	'[ỳýỷỹỵ]': 'y'
}

stop_words = ['bạn', 'ban', 'anh', 'chị', 'chi', 'em', 'shop', 'bot', 'ad']

def convert_to_no_accents(text):
	output = text
	for regex, replace in patterns.items():
		output = re.sub(regex, replace, output)
		output = re.sub(regex.upper(), replace.upper(), output)
	return output

trains = {}
with open('/home/nacht/telebot/src/model/intents_v2.json', 'r', encoding='utf-8') as json_data:
	intents = json.load(json_data)
	for one_intent in intents['intents']:
		sentences = one_intent['patterns']
		trains[one_intent['tag']] = sentences
# print(trains)
classes = {}
X_train = []
y_train = []
for i, (key, value) in enumerate(trains.items()):
	X_train += [word_tokenize(v, format="text") for v in value] + [convert_to_no_accents(v) for v in value]
	y_train += [i]*len(value)*2
	classes[i] = key

pickle.dump(classes, open("/home/nacht/telebot/src/pkl/classes.pkl", "wb"))

y_train = to_categorical(y_train)

# print(X_train)
# print(y_train)
vectorizer = TfidfVectorizer(lowercase=True, stop_words=stop_words)
# print(vectorizer)

# save this
X_train = vectorizer.fit_transform(X_train).toarray()
pickle.dump(vectorizer, open("/home/nacht/telebot/src/pkl/tfidf_vectorizer.pkl", "wb"))
# print(vectorizer)

# print(X_train)
# print('shape = ', X_train.shape[1:])
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(8, input_dim = X_train.shape[1] ))
model.add(tf.keras.layers.Dense(8))
# model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Dense(len(y_train[0]), activation='softmax'))
callbacks = [
	keras.callbacks.ModelCheckpoint('model.h5', save_best_only=True),
]
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=2000, batch_size=8, callbacks=callbacks)
model.save('model.h5')

classes = pickle.load( open( "/home/nacht/telebot/src/pkl/classes.pkl", "rb" ) )

with open('/home/nacht/telebot/src/model/intents_v2.json', 'r', encoding='utf-8') as json_data:
	intents = json.load(json_data)

# with open('data/dishes_data.json', 'r', encoding='utf-8') as json_data:
#     database = json.load(json_data)

model = tf.keras.models.load_model('model.h5')
# model.summary()

vectorizer = pickle.load(open("/home/nacht/telebot/src/pkl/tfidf_vectorizer.pkl", "rb"))

def classify(sentence):
	sentence = word_tokenize(sentence, format="text")
	results = model.predict(vectorizer.transform([sentence]).toarray())[0]
	results = np.array(results)
	idx = np.argsort(-results)[0]
	return classes[idx], results[idx]

def response(tag):
	for i in intents['intents']:
		if i['tag'] == tag:
			return random.choice(i['responses'])

# while True:
# 	print('Human: ', end=''),
# 	x = input()
# 	tag, _ = classify(x)
# 	print('Bot: ', response(tag))