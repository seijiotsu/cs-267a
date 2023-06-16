import sqlite3

class DatabaseConnection():
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

        # Initialize operator list
        query = f'SELECT name FROM sqlite_master where type="table";'
        result = self.conn.execute(query).fetchall()
        self.operators = set([row[0] for row in result])

        # Initialize instance list
        self.instances = set()
        for operator in self.operators:
            query = f'SELECT DISTINCT Instance FROM {operator};'
            result = self.conn.execute(query).fetchall()
            self.instances = self.instances.union(set([row[0] for row in result]))

    def probability(self, operator, instance):
        query = f'SELECT Probability from {operator} ' \
                f'WHERE Instance="{instance}";'
                
        result = self.conn.execute(query).fetchall()

        if not result:
            return 0

        return result[0][0]