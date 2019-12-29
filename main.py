from app.models.config_reader import ConfigReader
from app.models.indexer import Indexer
from lib.database.connector import AccessDatabase
from lib.cache.cache import Redis
from pyvi import ViTokenizer
import time

class Main:

    def __init__(self):
        configer = ConfigReader("./app/config/service.conf")
        configer.parseFile()
        configInfo = configer.config
        dbHost, dbPort, dbName = configInfo["dbHost"], configInfo["dbPort"], configInfo["dbName"]
        accessor = AccessDatabase(dbHost, dbPort, dbName)
        cacher = Redis(configInfo["redisHost"], configInfo["redisPort"])
        indexer = Indexer(accessor, {
            "title" : 1.0,
            "content" : 0.7
        }, cacher)
        start = time.time()
        query = ViTokenizer.tokenize("có chuyện gì vậy?")
        indexer.retrieval(query, query.split(), ["Người ngoài hành tinh", "Ngày tận thế", "1001 bí ẩn", "Chinh phục sao Hỏa"])
        print("Done! %.2f" % (time.time() - start))
if __name__ == "__main__":
    Main()