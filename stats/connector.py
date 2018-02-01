import couchdb

class Database():
    def __init__(self):
        self.couch = couchdb.Server()

    def insert(self, table, item):
        db = self.couch[table]
        db.save(item)

    def save(self, table, data):
        self.reset_table(table)
        for item in data:
            self.insert(table, item)

    def reset_table(self, table):
        try:
            self.couch.delete(table)
        except:
            pass
        finally:
            self.couch.create(table)
