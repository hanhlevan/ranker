import random, string
from lib.datastructures.sentence import Sentence
from app.models.parser import QueryParser
from pyvi import ViTokenizer

class Judger:

    rangeLens = [5, 6]
    delimiters = (",", ".", "-")

    def __init__(self, judgeFile):
        self.__funcs = [self.__edit, self.__remove, self.__insert, self.__none, self.__none, self.__none, self.__none, self.__none, self.__none, self.__none]
        self.fileName = judgeFile
        self.__corpus = open(self.fileName).read()
        self.__generateData()

    def __edit(self, word):
        randChar = random.choice(string.ascii_lowercase)
        index = random.randint(0, len(word) - 1)
        return word[:index] + randChar + word[index + 1:]
    
    def __remove(self, word):
        index = random.randint(0, len(word) - 1)
        return word[:index] + word[index + 1:]
    
    def __insert(self, word):
        randChar = random.choice(string.ascii_lowercase)
        index = random.randint(0, len(word) - 1)
        return word[:index] + randChar + word[index:]

    def __none(self, word):
        return word

    def __get(self, sentence):
        sentence = Sentence(sentence).remove_accents()
        words = sentence.split()
        for i, word in enumerate(words):
            rannum = random.randint(0, 9)
            words[i] = self.__funcs[rannum](word)
        sentence = " ".join(words)
        return sentence

    def __generateData(self):
        self.__sentences = []
        corpus = self.__corpus.split()
        lastIndex = len(corpus) - 1
        currentIndex = 0
        while currentIndex <= lastIndex:
            currentLen = random.randint(self.rangeLens[0], self.rangeLens[1])
            currentSentence = corpus[currentIndex: currentIndex + currentLen]
            currentSentence = ' '.join(currentSentence).lower()
            self.__sentences.append(currentSentence)
            currentIndex += currentLen
        # corpus = [self.__corpus.lower()]
        # for delimiter in self.delimiters:
        #     sentences = []
        #     for item in corpus:
        #         sentences.extend(item.split(delimiter))
        #     corpus = sentences
        # self.__sentences = corpus
        self.__data = []
        for sentence in self.__sentences:
            item = self.__get(sentence)
            sentence = ViTokenizer.tokenize(sentence)
            self.__data.append((item, sentence))

    def setParser(self, parser):
        self.parser = parser

    def __matchScore(self, pred, real):
        setReal = set(real.split())
        score = 0
        for item in pred:
            setItem = set(item.split())
            currentScore = len(setItem.intersection(setReal)) / max(len(setReal), len(setItem))
            score = max(score, currentScore)
        return score

    def testJudger(self):
        print(self.__data)
        print(len(self.__data))
        score, maxScore = 0, len(self.__data)
        for bef, real in self.__data:
            pred = self.parser.predict(bef)
            qPred = pred["queries"]
            matching = self.__matchScore(qPred, real)
            score += matching
            print("Before: %s\nPredict: %s\nReality: %s\nScore: %.2f\n---" % (bef, qPred, real, matching))
        print("Score: %.2f/%d (%.2f%%)" % (score, maxScore, (score / maxScore) * 100))