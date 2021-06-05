import sqlite3

class database:
    def __init__(self):
        conn = sqlite3.connect('save1.db')
        self.conn = conn

    def createTable(self, TableName = 'userData', Values = ['user', 'points']):
        c = self.conn.cursor()
        final = f'CREATE TABLE IF NOT EXISTS {TableName}('
        for i in Values:
            final += f'{i} TEXT'
            if Values[len(Values)-1] != i:
                final += ','

        final += ')'
        print(final)

        c.execute(final)


    
    def saveData(self, user, newStats, TableName = 'userData'):
        c = self.conn.cursor()
        print(user, newStats, TableName)
        if self.getData(user, TableName) == None:
            c.execute(f"INSERT INTO {TableName} VALUES (?,?)", (user,newStats))
            self.conn.commit()
            return "Saved"
        else:
            self.updateData(newStats, user, TableName)
            return "Updated"


    def updateData(self, newStats, user, TableName = 'userData'):
        c = self.conn.cursor()
        c.execute(f"UPDATE {TableName} SET points = ? WHERE user = ?", (newStats,user))
        self.conn.commit()



    def getData(self, info, tableName = 'userData'):
        #Returns a list of data saved earlier
        c = self.conn.cursor()
        print(info, tableName)
        c.execute(f"SELECT * FROM {tableName} WHERE user='{info}'")
        return c.fetchone()



    def delete(self, TableName = 'userData'):
        c = self.conn.cursor()
        c.execute(f"DELETE FROM {TableName}")

    def close(self):
        self.conn.close()