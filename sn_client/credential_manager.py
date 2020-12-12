import sqlite3
from cryptography.fernet import Fernet 
import os

class CredentialManager:
    def __init__(self):
        self.generate_key()
        self.conn = sqlite3.connect('instances.db')
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
            decrypted_password = self.decrypt_password(credentials[1])
            return (credentials[0], decrypted_password,)
        else:
            print(f'No credentials found for {instance}')

    def save_instance_credentials(self, credentials):
        encrypted_password = self.encrypt_password(credentials[2])
        encrypted_credentials = (credentials[0], credentials[1], encrypted_password,)
        self.c.execute(f'INSERT INTO instances VALUES (?, ?, ?)', encrypted_credentials)
        self.conn.commit()
        self.conn.close()

    def generate_key(self):
        path = os.getcwd()
        keypath = os.path.join(path, 'secret.key')
        if not os.path.exists(keypath):
            key = Fernet.generate_key()
            with open('secret.key', 'wb') as key_file:
                key_file.write(key)

    def load_key(self):
        return open('secret.key', 'rb').read()

    def encrypt_password(self, string):
        key = self.load_key()
        f = Fernet(key)
        encoded_string = string.encode()
        encrypted_string = f.encrypt(encoded_string)
        return encrypted_string

    def decrypt_password(self, string):
        key = self.load_key()
        f = Fernet(key)
        decrypted_string = f.decrypt(string)
        decoded_string = decrypted_string.decode()
        return decoded_string