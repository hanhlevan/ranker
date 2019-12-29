import json
from app.sentence import Sentence

class WordGetter:

    wordFile = "./data/Viet74K.txt"
    tokenFile = "./data/map.json"
    __LowerCode = set("àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ")

    def __init__(self, fileName=None):
        if fileName is None:
            fileName = self.wordFile
        self.fileName = fileName
        self.__getData()
        self.__loadTelexToken()

    def __loadTelexToken(self):
        with open(self.tokenFile) as f:
            self.map = json.load(f)

    def __getData(self):
        self.__words = open(self.fileName).read().split()

    def __check(self, word):
        if not word.isalpha(): return False
        for c in word:
            if c in self.__LowerCode:
                return True
        return False

    def __get(self, word):
        word = word.lower()
        result = Sentence(word).remove_accents()
        # result, word = "", word.lower()
        # for c in word:
        #     if c in self.map:
        #         c = self.map[c]
        #     result += c
        return word, result

    def fit(self):
        self.orginalWords = dict()
        self.words = set()
        for word in self.__words:
            currentList = [self.__get(w) for w in set(word.split()) if self.__check(w)]
            self.orginalWords.update(dict((y, x) for x, y in currentList))
            self.words.update([w[1] for w in currentList])
        self.words = sorted(self.words)
        print(self.orginalWords)
        print(self.words[:100])
        print(len(self.words))