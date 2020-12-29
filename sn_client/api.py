import requests
import json
import re
import settings 

class SNClient:
    def __init__(self, instance, username, password):
        self.instance = instance
        self.username = username
        self.password = password
        self.headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        self.record_id_format = settings.RECORD_ID_FORMAT
        self.fields = settings.DISPLAYED_DATA_FIELDS

    def get_instance_name(self):
        return self.instance
    
    def get_instance_url(self):
        url = f'https://{self.get_instance_name()}.service-now.com'
        return url

    def test_connection(self):
        url = self.get_instance_url()
        response = requests.get(url, auth=(self.username, self.password))
        if response.ok:
            print(f'Connected to instance {url}')
        else:
            print(f'Could not connect to instance {url}. Status code {response.status_code}')
            exit()
   
   # Used for overriding the DISPLAYED_DATA_FIELDS property. If use_default is set to True, will self.fields to default values in the settings
    def set_fields(self, fields, use_default=False):
       if use_default:
           self.fields = settings.DISPLAYED_DATA_FIELDS
           return
       fields_list = fields.split(',')
       self.fields = fields_list
    
    def get_fields(self):
        return self.fields

    def get_fields_dict(self):
        return {}.fromkeys(self.fields)

    # fields = fields to look for in base table
    # record = base table record to check against
    def get_missing_fields_in_base_table(self, record):
        missing_fields = []
        for field in self.fields:
            if record.get(field) is None:
                missing_fields.append(field)
        return missing_fields
                      
    def populate_fields_dictionary(self, dict, record):
        for field in self.fields:
            dict[field] = record.get(field)
        return dict

    def is_valid_record_id(self, text):
        match = re.search(self.record_id_format, text)
        return match is not None
       
    def extract_record_id(self, text):
        if self.is_valid_record_id(text):
            ID = re.search(self.record_id_format, text)[0]
            return ID
        else:
            return None

    def query_records(self, table, query, **kwargs):
        params = '&'
        for k, v in kwargs.items():
            params += f'{k}={v}&'
        if query:
            query = f'?sysparm_query={query}'
        url = f'{self.get_instance_url()}/api/now/table/{table}{query}{params}'
        response = requests.get(url, auth=(self.username, self.password), headers=self.headers)
        result = self._handle_response(response)
        if len(result) > 0:
            return result
        else:
            return None

    def get_record(self, table, sys_id,**kwargs):
        table = table.lower()
        params = '?'
        for k, v in kwargs.items():
            params += f'{k}={v}&' 
        url = f'{self.get_instance_url()}/api/now/table/{table}/{sys_id}{params}'
        response = requests.get(url, auth=(self.username, self.password), headers=self.headers)
        result = self._handle_response(response)
        return result
        
    def display_record_data(self, record):
        for field in self.fields:
            if type(record[field]) == dict and record[field].get('display_value'):
                value = record[field]['display_value']
            else:
                value = record[field]
            print(f'{field}: {value}')

    def query_attachments(self, query):
        if query:
            query = f'?sysparm_query={query}'
        url = f'{self.get_instance_url()}/api/now/attachment{query}'
        response = requests.get(url, auth=(
            self.username, self.password), headers=self.headers)
        result = self._handle_response(response)
        return result
        
    def get_attachment(self, attachment_sys_id):
        url = f'{self.get_instance_url()}/api/now/attachment/{attachment_sys_id}/file'
        response = requests.get(url, auth=(
            self.username, self.password), headers=self.headers)
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
            return {'status': response.status_code, 'error': response.content}
        elif response.status_code == 200 and response.headers['Content-Type'] != 'application/json':
            return {'status': response.status_code, 'error': 'Something went wrong with connecting to the instance'}
            exit()
        else:
            json_body = response.json()
            result = json_body['result'] if json_body.get('result') is not None else json_body
        return result




