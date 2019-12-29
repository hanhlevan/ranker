from pyvi import ViTokenizer
import re

class Sentence:
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    u = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ'
    l = u'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'
    B_C = '__begin__'
    E_C = '__end__'
    NAME_REGREX = re.compile(r'[' + u + r'A-Z]+[' + l + 'a-z]+,?\s+(?:[' + u + r'A-Z][' + l + 'a-z]*\s*)*[' + u + r'A-Z][' + l + 'a-z]+', re.UNICODE)
    NUM_REGREX  = re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.\,]?\d*(?:[eE][-+]?\d+)?', re.UNICODE)
    replacements = {
        "name"  : "begin__name__end",
        "num"   : "begin__num__end",
        "other" : "begin__other__end"
    }
    punkts = {",", ".", '"', "'", ":", "!", "?", "..."}

    def __init__(self, sentence='', list_names=[], vocab=[]):
        self.set_sentence(sentence)
        self.set_list_name(list_names)
        self.set_vocab(vocab)
        self.replace = self.replacements
        self.results = dict()
        self.functions = {
            "tokenize"  : self.tokenize,
            "name"      : self.detect_name,
            "num"       : self.detect_num,
            "other"     : self.detect_other,
            "lower"     : self.lower
        }

    def beautify(self, list_functions=["tokenize", "other", "num", "lower"]):
        self.results = dict()
        for item in list_functions:
            if item in self.functions:
                self.functions[item]()
        self.sentence = self.sentence.strip().replace("  ", " ")
        return self.sentence

    def get_extracted_names(self):
        if "name" in self.results:
            return self.results["name"].values()
        return []

    def lower(self):
        self.sentence = self.sentence.lower()

    def set_sentence(self, sentence):
        self.sentence = sentence
        self.word_cnt = len(sentence.split())

    def set_vocab(self, vocab):
        self.vocab = set(vocab)

    def set_replace(self, name, value):
        self.replace[name] = value

    def tokenize(self, remove=True):
        self.sentence = ViTokenizer.tokenize(self.sentence)
        if remove:
            self.sentence = self.sentence.replace("_", " ")
        return self.sentence

    def extract_n_gram(self, n, style="str", delimiter=" "):
        lst = []
        words = self.sentence.split()
        word_size = len(words)
        for i in range(word_size - n + 1):
            item = tuple(words[i: i + n]) if style == "tuple" else delimiter.join(words[i: i + n])
            lst.append(item)
        return lst

    def remove_accents(self):
        input_str = self.sentence
        string = ''
        for char in input_str:
            char = char if char not in self.s1 else self.s0[self.s1.index(char)]
            string += char
        return string

    def set_list_name(self, list_names):
        self.list_names = set(list_names[:])

    def is_title(self, word):
        if len(word) >= 1:
            return word[0].isupper()
        return False

    def detect_name(self):
        """
        :param set_name:
        :return: list of names detected
        """
        results = dict()
        self.words = self.sentence.split()

        # Two or more two words are title, this also always a name
        word_cnt, start = len(self.words), 0
        index_leng = [0] * word_cnt
        check = [False] * word_cnt
        while (start < word_cnt):
            if (not check[start]) and (self.is_title(self.words[start])) and (not self.words[start].isupper()):
                check[start] = True
                end = min(word_cnt, start + 1)
                while (end < word_cnt) and (self.is_title(self.words[end])):
                    check[end] = True
                    end += 1
                if end < word_cnt:
                    end -= 1
                    while (end >= start) and (self.next_word_in_vocab(end, [2, 3, 4])):
                        end -= 1
                if end - start + 1 >= 2:
                    index_leng[start] = end - start + 1
                start = end
            else: start += 1
        # All letters are upper, this always a name
        for i, word in enumerate(self.words):
            if (len(word) > 1) and (not check[i]) and word.isalpha() and word.isupper():
                results[i] = word
                index_leng[i] = 1
        # Check first word
        if self.check_first_word():
            index_leng[0] = 1

        # Get data
        new_words = []
        start = 0
        while (start < word_cnt):
            if index_leng[start] > 0:
                next_index = start + index_leng[start]
                current_word = " ".join(self.words[start: next_index])
                new_words.append(current_word)
                results[start] = current_word
                new_words[-1] = self.replace["name"]
                start = next_index
            else:
                new_words.append(self.words[start])
                start = start + 1
        del self.words
        # for i, word in enumerate(self.words):
        #     print("%s : %d" % (word, index_leng[i]), end=",")
        self.words = new_words
        self.sentence = ' '.join(self.words)
        self.results["name"] = results
        return (self.sentence, results)

    def check_first_word(self):
        word_cnt = len(self.words)
        if word_cnt > 0:
            first_word = self.words[0]
            if first_word[0].isupper():
                if word_cnt > 1:
                    if self.next_word_in_vocab(0, [2, 3, 4]):
                        return False
            if first_word in self.list_names:
                return True
        return False

    def next_word_in_vocab(self, start, list_check):
        for n in list_check:
            next_n_words = self.get_next(start, n)
            if next_n_words in self.vocab:
                return True
            next_n_words = next_n_words.lower()
            if next_n_words in self.vocab:
                return True
        return False

    def get_next(self, start, cnt):
        word_cnt = len(self.words)
        end = min(word_cnt, start + cnt)
        return " ".join(self.words[start : end])

    def restore(self):
        results = dict()
        for _, value in self.results.items():
            results.update(value)
        for i, word in enumerate(self.words):
            if i in results:
                self.words[i] = results[i]
        self.sentence = ' '.join(self.words)
        return self.sentence

    def detect_num(self):
        results = dict()
        current_nums = re.findall(self.NUM_REGREX, self.sentence)
        self.sentence = re.sub(self.NUM_REGREX, self.replace['num'], self.sentence)
        self.words = self.sentence.split()
        cnt = 0
        for i, word in enumerate(self.words):
            if word == self.replace['num']:
                results[i] = current_nums[cnt]
                cnt += 1
        self.sentence = " ".join(self.words)
        self.results["num"] = results
        return (self.sentence, results)

    def detect_other(self):
        results = dict()
        self.words = self.sentence.split()
        for i, word in enumerate(self.words):
            if (not word.isalpha()) and (not word.isnumeric()) and (word not in self.replacements.values()):
                if word not in self.punkts:
                    results[i] = self.words[i]
                    self.words[i] = self.replace["other"]
        self.sentence = " ".join(self.words)
        self.results["other"] = results
        return self.sentence

    def restore_sentence(self, sentence, names):
        words = sentence.split()
        for i, word in enumerate(words):
            if word == self.replacements["name"]:
                words[i] = names[i]
        return ' '.join(words)

    def remove(self, list_remove=["num", "name", "other"]):
        check_list = set()
        for item in list_remove:
            check_list.add(self.replacements[item])
        for word in check_list:
            self.sentence = self.sentence.replace(word, "")
        self.sentence = self.sentence.strip().replace("  ", " ")
        return self.sentence