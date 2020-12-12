import requests
import json
import re
import sqlite3

class SNClient:
    def __init__(self, instance, username, password):
        self.instance = instance
        self.conn = sqlite3.connect('instances.db')
        self.c = self.conn.cursor()
        cursor = self.c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='instances'")
        result = self.c.fetchall()
        if len(result) > 0:
            self.c.execute(f"SELECT username, password FROM instances WHERE instance_name=?", (instance, ))
            credentials = self.c.fetchone()
            if credentials is not None:
                self.username = credentials[0]
                self.password = credentials[1]
                self.conn.close()
            else:
                self.username = username
                self.password = password
                self.save_instance_credentials((instance, username, password,))

        else:
            self.c.execute(
                f"CREATE TABLE instances (instance_name TEXT, username TEXT, password TEXT);")
            self.save_instance_credentials((instance, username, password))

        self.record_id_format = r"\D{3}\d+"
      

    def save_instance_credentials(self, credentials):
        self.c.execute(f'INSERT INTO instances VALUES (?, ?, ?)', credentials)
        self.conn.commit()
        self.conn.close()

    def get_instance_name(self):
        return self.instance
    
    def get_instance_url(self):
        url = f'{self.get_instance_name()}.service-now.com'
        return url

    def is_valid_record_id(self, text):
        match = re.search(self.record_id_format, text)
        return match is not None
       
    def extract_record_id(self, text):
        if self.is_valid_record_id(text):
            ID = re.search(self.record_id_format, text)[0]
            return ID
        else:
            return None

    def send_table_api_request(self, table, query):
        if query:
            query = f'?sysparm_query={query}'
        url = f'https://{self.get_instance_url()}/api/now/table/{table}{query}'
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        response = requests.get(url, auth=(self.username, self.password), headers=headers)
        result = self._handle_response(response)
        if len(result) > 0:
            return result
        else:
            return None
            

    def send_attachment_api_request(self, query):
        if query:
            query = f'?sysparm_query={query}'
        url = f'https://{self.get_instance_url()}/api/now/attachment{query}'
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        response = requests.get(url, auth=(
            self.username, self.password), headers=headers)
        result = self._handle_response(response)
        return result
        
    def download_attachment(self, attachment_sys_id):
        url = f'https://{self.get_instance_url()}/api/now/attachment/{attachment_sys_id}/file'
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        response = requests.get(url, auth=(
            self.username, self.password), headers=headers)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:',
                response.headers, 'Error Response:', response.content)
            exit()
        metadata = json.loads(response.headers['x-attachment-metadata'])
        attachment = {'content': response.content,
                    'filename': metadata['file_name']}
        return attachment
                        

    def _handle_response(self, response):
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:',
            response.headers, 'Error Response:', response.content)
            result = {'status': response.status_code, 'error': response.content}
        result = response.json()['result']
        return result




