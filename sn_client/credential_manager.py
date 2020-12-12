import sqlite3

class CredentialManager:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor()
        self.c.execute(
                f"CREATE TABLE IF NOT EXISTS instances (instance_name TEXT, username TEXT, password TEXT);")

    def fetch_all_instances(self):
        self.c.execute('SELECT instance_name FROM instances')
        instances = self.c.fetchall()
        return instances

    def fetch_credentials_for_instance(self, instance):
        self.c.execute(
            f"SELECT username, password FROM instances WHERE instance_name=?", (instance, ))
        credentials = self.c.fetchone()
        self.conn.close()
        if credentials is not None:
            return credentials
        else:
            print(f'No credentials found for {instance}')

    def save_instance_credentials(self, credentials):
        self.c.execute(f'INSERT INTO instances VALUES (?, ?, ?)', credentials)
        self.conn.commit()
        self.conn.close()
