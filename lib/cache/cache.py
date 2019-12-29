import redis
import ast
from bson import ObjectId
import time


class Redis:

    specialField = "ObjectId"

    def __init__(self, host, port):
        self.__redisEngine = redis.Redis(host=host, port=int(port), db=0)
    
    def Set(self, keyName, dataDict):
        text = str(dataDict)
        self.__redisEngine.set(keyName, text)
    
    def Exist(self, keyName):
        text = self.__redisEngine.get(keyName)
        return text is not None

    def Get(self, keyName):
        text = self.__redisEngine.get(keyName)
        if text is None: return None
        return ast.literal_eval(text)

    def GetDocument(self, keyName):
        start = time.time()
        text = self.__redisEngine.get(keyName)
        if text is None: return None
        text = text.decode()
        text = text.replace(self.specialField, "")
        value = ast.literal_eval(text)
        for key, val in value.items():
            if type(val) == tuple:
                value[key] = ObjectId(val[0])
        print(text)
        print("Parse: %.2f" % (time.time() - start))
        return value
