import couchdb


class Database:
    """
    A simple helper class to abstract away interaction with the database

    It also allows us to easily switch databases in the future should it
    be required without changing any external code.
    """
    def __init__(self):
        """
        Connect to our CouchDB server on initialization.

        We reference "couchdb" here, instead of localhost because
        we're connecting to a CouchDB Docker container.
        """
        self.couch = couchdb.Server('http://couchdb:5984')

    def insert(self, table, item):
        """
        A simple abstraction for inserting data into a CouchDB table

        :param table: A string containing a table name
        :param item: A dictionary object
        :return: N/A
        """
        db = self.couch[table]
        db.save(item)

    def save(self, table, data):
        """
        A further abstraction of the above insert function.

        It receives a list and performs insert on each dictionary
        object held within it.

        :param table: A string containing a table name
        :param data: A list of dictionary objects
        :return: N/A
        """
        self.reset_table(table)
        for item in data:
            self.insert(table, item)

    def reset_table(self, table):
        """
        Rather than constantly clean out the database or look
        for entries older than X days, it's quicker to just
        keep resetting the database.

        Reset in this case is deleting a table followed by creating it
        from scratch. This approach also means that the resulting
        application/docker containers are disposable.

        It doesn't matter if I lose the containers or my server, I can just
        easily re-fetch data from scratch and carry on.

        :param table: A string containing a table name.
        :return: N/A
        """
        try:
            self.couch.delete(table)
        except Exception:
            pass
        finally:
            self.couch.create(table)
