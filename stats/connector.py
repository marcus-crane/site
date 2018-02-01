import couchdb

class Database():
    def __init__(self):
        self.couch = couchdb.Server()

    def insert(self, table, data):
        db = self.couch[table]
        db.save(data)

    def reset_table(self, table):
        try:
            self.couch.delete(table)
        except:
            pass
        finally:
            self.couch.create(table)


