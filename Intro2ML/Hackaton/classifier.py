"""
===================================================
     Introduction to Machine Learning (67577)
             IML HACKATHON, June 2017

            **  Headline Classifier  **

Auther(s):

===================================================
"""
from random import shuffle

from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn import feature_extraction, tree, model_selection, metrics, linear_model
import matplotlib.pyplot as plt
import matplotlib
import load_headlines
import itertools

LEFT_DATA = ['settlements', 'west bank', 'freedom', 'global', 'global warming', 'zehava gallon', 'peacenow', 'peace',
             'apartheid', 'feminism', 'tel aviv', 'racist', 'existentialism', 'merav michaeli', 'tamar zandberg',
             'homosexuals', 'lgbt', 'queer', 'theory', 'university', 'sociology', 'anthropology', 'abbas', 'activist',
             'activists', 'human rights', 'b\'tselem', 'democracy', 'fascism', 'culture', 'radical Right',
             'imperialism', 'occupation', 'Illegal', 'literature', 'patriarchal', 'researchs', 'research', 'ambivalent',
             'nakba', 'narrative']


class Classifier(object):
    def __init__(self):
        self.model = None
        self.mostCommonWords = []
        # self.train_model()

    def classify(self, X):
        """
        Recieves a list of m unclassified headlines, and predicts for each one which newspaper published it.
        :param X: A list of length m containing the headlines' texts (strings)
        :return: y_hat - a binary vector of length m
        """
        RESULTS = []
        for x in X:
            x_vec = self.getVector(x)
            x_vec = np.array(x_vec).reshape(len(x_vec),1).T
            RESULTS.append(int(self.model.predict(x_vec)))
        return RESULTS

    def train_model(self,x,y):
        # x, y = load_headlines.load_dataset()
        self.calcMostCommonWords(x)
        X1_vectors = []
        for headline in x:
            features = self.getVector(headline)
            X1_vectors.append(features)

        clf = MLPClassifier(solver='adam', alpha=1e-4,
                            hidden_layer_sizes=(700, 200))
        # clf = linear_model.SGDClassifier()
        clf.fit(X1_vectors, y)
        self.model = clf


    def getVector(self, x):
        a = [self.longest_word(x),
                self.H_entropy(x)/5,
                self.vowel_consonant_ratio(x),
                len(x)/130,
                self.getHowManyCommonWords(x)+
                self.numOfWords(x)/20,
                self.meanLengthOfWords(x),
                self.countBigLetters(x)]
        a.extend(list(self.countParatness(x)))
        return a

    def H_entropy(self, x):
        # Calculate Shannon Entropy
        prob = [float(x.count(c)) / len(x) for c in dict.fromkeys(list(x))]
        H = - sum([p * np.log2(p) for p in prob])
        return H

    def vowel_consonant_ratio(self, x):
        # Calculate vowel to consonant ratio
        x = x.lower()
        vowels_pattern = re.compile('([aeiou])')
        consonants_pattern = re.compile('([b-df-hj-np-tv-z])')
        vowels = re.findall(vowels_pattern, x)
        consonants = re.findall(consonants_pattern, x)
        try:
            ratio = len(vowels) / len(consonants)
        except:  # catch zero devision exception
            ratio = 0
        return ratio

    # ngrams: Implementation according to Schiavoni 2014: "Phoenix: DGA-based Botnet Tracking and Intelligence"
    # http://s2lab.isg.rhul.ac.uk/papers/files/dimva2014.pdf

    def ngrams(self, word, n):
        # Extract all ngrams and return a regular Python list
        # Input word: can be a simple string or a list of strings
        # Input n: Can be one integer or a list of integers
        # if you want to extract multipe ngrams and have them all in one list

        l_ngrams = []
        if isinstance(word, list):
            for w in word:
                if isinstance(n, list):
                    for curr_n in n:
                        ngrams = [w[i:i + curr_n] for i in range(0, len(w) - curr_n + 1)]
                        l_ngrams.extend(ngrams)
                else:
                    ngrams = [w[i:i + n] for i in range(0, len(w) - n + 1)]
                    l_ngrams.extend(ngrams)
        else:
            if isinstance(n, list):
                for curr_n in n:
                    ngrams = [word[i:i + curr_n] for i in range(0, len(word) - curr_n + 1)]
                    l_ngrams.extend(ngrams)
            else:
                ngrams = [word[i:i + n] for i in range(0, len(word) - n + 1)]
                l_ngrams.extend(ngrams)
                #     print(l_ngrams)
        return l_ngrams

    def ngram_feature(self, domain, d, n):
        # Input is your domain string or list of domain strings
        # a dictionary object d that contains the count for most common english words
        # finally you n either as int list or simple int defining the ngram length

        # Core magic: Looks up domain ngrams in english dictionary ngrams and sums up the
        # respective english dictionary counts for the respective domain ngram
        # sum is normalized

        l_ngrams = self.ngrams(domain, n)
        #     print(l_ngrams)
        count_sum = 0
        for ngram in l_ngrams:
            if d[ngram]:
                count_sum += d[ngram]
        try:
            feature = count_sum / (len(domain) - n + 1)
        except:
            feature = 0
        return feature

    def average_ngram_feature(self, l_ngram_feature):
        # input is a list of calls to ngram_feature(domain, d, n)
        # usually you would use various n values, like 1,2,3...
        return sum(l_ngram_feature) / len(l_ngram_feature)

    def longest_word(self, text):
        # return the len of longest word
        len_word = 0
        for word in text.split():
            len_word = max(len_word, len(word))
        # res = len_word
        # for word in text.split():
        #     if len(word) > int(0.8*len_word):
        #         res += len(word)
        return len_word/len(text)

    def left_right_confidence(self, title):
        res = 0.5
        left = 0
        for word in title:
            if word.lower() in LEFT_DATA:
                left += 1
        res += left / len(LEFT_DATA) * 0.5
        return res

    def countParatness(self, text):
        special_letters = 0
        h = {'(':0,')':0,':':0,'?':0,'!':0,'[':0,']':0, '"':0, ',':0,'.':0,
             '/':0,'-':0,'=':0,'%':0,'$':0}
        for letter in text:
            if letter in ['(',')',':','?','!','[',']', '"', ',','.','/','-','=','%','$']:
                h[letter] = 1
        return h.values()

    def numOfWords(self,text):
        return len(text.split())/len(text)

    def meanLengthOfWords(self,text):
        lengths = []
        for word in text.split():
            lengths.append(len(word))
        return np.mean(lengths)/max(lengths)

    def countBigLetters(self, text):
        special_letters = 0
        for letter in text:
            if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                special_letters += 1
        return special_letters/self.numOfWords(text)

    def calcMostCommonWords(self, X):
        h = dict()
        for x in X:
            for word in x.split():
                if word.lower() in h:
                    x = 1+h[word.lower()]
                    h[word.lower()] = x
                else:
                    h[word] = 1
        a = sorted(h, key=h.get)
        self.mostCommonWords = list(a[-20:])

    def getHowManyCommonWords(self, text):
        counter = 0
        for word in text.split():
            if word.lower() in self.mostCommonWords:
                counter += 1
        return counter/(len(text)*self.numOfWords(text))


def main():
    x_set = []
    y_set = []
    x, y = load_headlines.load_dataset()
    index_shuf = np.arange(len(x))
    np.random.shuffle(index_shuf)
    for i in index_shuf:
        x_set.append(x[i])
        y_set.append(y[i])

    size = int(0.8*len(x_set))
    test_x, test_y = x_set[size:], y_set[size:]
    c = Classifier()
    num = 0
    # test_headline, result = load_headlines.load_dataset()
    c.train_model(x_set[:size], y_set[:size])
    res = c.classify(test_x)
    # print(test_headline[num])
    print("out answer:" + str(res))
    print("result: " + str(test_y))
    good = 0
    for i in range(len(test_x)):
        if res[i] == test_y[i]:
            good += 1
    print("good : " + str(good/len(test_x)))

main()
