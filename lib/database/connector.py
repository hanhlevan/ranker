import pymongo

class AccessDatabase:

    def __init__(self, dbHost, dbPort, dbName):
        self.accessor = pymongo.MongoClient("mongodb://%s:%s/" % (dbHost, dbPort))
        self.mydb = self.accessor[dbName]

    def write(self, colName, data):
        print("Size of data: %d" % len(data))
        mycol = self.mydb[colName]
        items = mycol.insert_many(data).inserted_ids
        print("Wrote %d/%d successfully!" % (len(items), len(data)))

    def remove(self, colName, condition={}):
        mycol = self.mydb[colName]
        mycol.remove(condition)

    def find_one(self, colName, condition={}, fields=None):
        mycol = self.mydb[colName]
        data = mycol.find_one(condition, fields)
        return data

    def find(self, colName, condition={}, fields=None):
        mycol = self.mydb[colName]
        items = []
        for item in mycol.find(condition, fields):
            items.append(item)
        return items

    def update(self, colName, query, replace):
        mycol = self.mydb[colName]
        mycol.update_one(
            query, { "$set": replace }
        )

    def test(self, colName):
        for item in self.find(colName):
            print(item)
