import sqlite3

class DatabaseConnection():
    def __init__(self, db_name, table):
        self.conn = sqlite3.connect(db_name)
        self.table = table

        # Initialize operator list
        query = f'SELECT DISTINCT Operator FROM {self.table};'
        result = self.conn.execute(query).fetchall()
        self.operators = set([row[0] for row in result])

        # Initialize instance list
        query = f'SELECT DISTINCT Instance FROM {self.table};'
        result = self.conn.execute(query).fetchall()
        self.instances = set([row[0] for row in result])

    def probability(self, operator, instance):
        query = f'SELECT Probability from {self.table} ' \
                f'WHERE Operator="{operator}" AND Instance="{instance}";'
                
        result = self.conn.execute(query).fetchall()

        if not result:
            return 0

        return result[0][0]