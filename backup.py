def __genVectorDocs(self):
        # Term Freq of docs
        cur, cnt = 1, len(self.listDocs)
        self.vectorDocs = dict()
        for _id in self.listDocs:
            percent = (cur / cnt) * 100
            print("Processing at (%d/%d - %.2f%%)" % (cur, cnt, percent))
            cur += 1

            vectorDoc = dict()
            doc = self.db.find_one("prepost", {
                "_id" : _id
            })
            category = doc["category"]
            for field in self.fields:
                vectorField = dict()
                for term, freq in doc["tFreq"][field]:
                    try:
                        df = self.__getIndex(term, category, field)["dFreq"]
                    except:
                        print("Not found: %s, %s, %s" % (term, category, field))
                        df = 1
                    vectorField[term] = self.TFIDF(tf=freq, df=df)
                vectorDoc[field] = vectorField
            # del doc["tFreq"]
            # self.vectorDocs[_id] = {
            #     "info" : doc,
            #     "vector" : vectorDoc
            # }

Retrieval Func
self.listDocs = set()
checkList = []
for term in self.extension:
    for category in self.categories:
        for field in self.fields:
            checkList.append({
                "term" : term,
                "category" : category,
                "field" : field
            })
data = self.db.find(
    "index", { "$or" : checkList}, {
    "_id" : False,
    "listIDs" : True
})
for item in data: self.listDocs.update(item["listIDs"])
data = self.db.find("prepost", {"_id" : {"$in" : list(self.listDocs)}}, { "tFreq" : False, "biGrams" : False })
documents = dict()
for item in data: documents[item["_id"]] = item
self.listDocs = documents


 def __getDocumentFrequence(self, terms):
        checkList = [{"category" : category, "field" : field, "term" : term}\
            for category in self.categories\
                for field in self.fields\
                    for term in terms]
        indexes = self.db.find("index", {"$or" : checkList })
        results = dict()
        for index in indexes:
            key = tuple([index["category"], index["field"], index["term"]])
            results[key] = index["dFreq"]
        return results


def __getFromCache(self):
        vectors, listDocs, remindDocs = dict(), [], []
        for objectId in self.listDocs:
            keyName = str(objectId)
            item = self.cache.Get(keyName)
            if item is not None:
                vectors[keyName] = item
                listDocs.append(objectId)
            else: remindDocs.append(objectId)
        self.dataCache = self.db.find("prepost", {"_id" : {"$in" : list(listDocs)}}, { "tFreq" : False, "biGrams" : False, "vectors" : False})
        for i, item in enumerate(self.dataCache):
            keyName = str(item["_id"])
            self.dataCache[i]["vectors"] = vectors[keyName]
        self.listDocs = remindDocs

    def __pushToCache(self):
        cnt = 0
        for _id, value in self.listDocs.items():
            keyName = str(_id)
            if not self.cache.Exist(keyName):
                self.cache.Set(keyName, value["vectors"])
                cnt += 1
                print("Saved %s" % keyName)
        print("Saved %d items" % cnt)

self.__getFromCache()
for item in self.dataCache: self.listDocs[item["_id"]] = item


data = self.db.find("prepost", {"_id" : {"$in" : list(self.listDocs)}}, { "tFreq" : False, "biGrams" : False})
self.listDocs = dict()
for item in data: self.listDocs[item["_id"]] = item
print("Retrieval %d document(s)!" % len(self.listDocs))



def __genVectorQuery(self):
        self.qVectors = dict()
        self.qNorm = dict()
        tFreq = dict(Counter(self.query.split()))
        for category in self.categories:
            vectorCategory = dict()
            normCategory = dict()
            for field in self.fields:
                vectorField = dict()
                for term, freq in tFreq.items():
                    try:
                        keyGen = tuple([category, field, term])
                        df = self.indexes[keyGen]["dFreq"]
                        vectorField[term] = self.__TfIdf(tf=freq, df=df)
                    except:
                        print("Not found: '%s', '%s', '%s'" % (term, category, field))
                vectorCategory[field] = vectorField

            self.qVectors[category] = vectorCategory
        print(self.qVectors)


def saveNorm(self):
        docs = self.db.find("prepost")
        cur, cnt = 0, len(docs)
        for item in docs:
            percent = (cur / cnt) * 100
            print("Processing at (%d/%d - %.2f%%)" % (cur, cnt, percent))
            cur += 1
            vectors = item["vectors"]
            normField = dict()
            for field in self.fields:
                vector = vectors[field]
                vector = dict((x, y) for x, y in vector)
                norm = np.linalg.norm(
                    np.array(list(vector.values()))
                )
                normField[field] = norm
            self.db.update("prepost", {
                "_id" : item["_id"]
            }, {
                "normL2" : normField
            })
