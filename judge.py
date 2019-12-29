from app.models.config_reader import ConfigReader
from app.models.parser import QueryParser
from app.models.judge.judger import Judger

class Main:

    def __init__(self):
        # while True:
        #     query = input("Enter your query: ")
        #     print(parser.predict(query))
        configer = ConfigReader("./app/config/service.conf")
        configer.parseFile()
        configInfo = configer.config
        dbHost, dbPort, dbName = configInfo["dbHost"], configInfo["dbPort"], configInfo["dbName"]
        parser = QueryParser(dbHost, dbPort, dbName)
        parser.loadModelCategory(configInfo["vectorFile"], configInfo["learnerModelFile"])
        # parser.fit()
        # parser.saveWordCorrect("./resource/wordCorrect.sav")
        # parser.saveSentenceCorrect("./resource/sentenceCorrect.sav")
        parser.loadWordCorrect(configInfo["wordCorrectFile"])
        # parser.loadSentenceCorrect("./resource/sentenceCorrect.sav")
        parser.loadSentenceCorrect(configInfo["sentenceCorrectFile"])
        parser.loadSynonym()

        judger = Judger(configInfo["judgeData"])
        judger.setParser(parser)
        judger.testJudger()


if __name__ == "__main__":
    Main()