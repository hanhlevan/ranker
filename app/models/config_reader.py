import os
import lib.files.fileman as fman

class ConfigReader:
    
    skipCode = "#"
    defaultFields = dict({
        # Source management
        "dataDir"           : "",
        "judgeData"         : "",
        "vectorFile"        : "",
        "learnerModelFile"  : "",
        "wordCorrectFile"   : "",
        "sentenceCorrectFile"   : "",
        # Cache config
        "redisHost"         : "",
        "redisPort"         : "",
        # Service management
        "prefixApiHost"     : "",
        # Log management
        "logPath"           : "",
        "logAppend"         : "False",
        # Database management
        "dbHost"           : "",
        "dbPort"           : "",
        "dbName"           : "",
        "dbUser"           : "",
        "dbPassword"       : ""
    })

    def __init__(self, filename):
        self.configFile = filename
        self.initConfig()
    
    def initConfig(self):
        self.config = self.defaultFields

    def parseFile(self):
        lines = []
        try:
            lines = open(self.configFile).readlines()
        except Exception as Error:
            self.config = self.defaultFields
            return {
                "status" : False,
                "content" : Error
            }
        for d, line in enumerate(lines):
            if line.startswith(self.skipCode): continue
            lst = line.split()
            if len(lst) != 2:
                return {
                    "status" : False,
                    "content" : "Syntax error at line %d: %s" % (d, line)
                }
            key, val = lst
            if  key not in self.config: 
                return {
                    "status" : False,
                    "content" : "The key is not defined %d: %s" % (d, line)
                }
            self.config[key] = val
        return {
            "status" : True
        }
