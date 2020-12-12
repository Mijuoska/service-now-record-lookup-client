from sn_client.sn_client import SNClient
from utils import create_folder, save_file


sn_client = SNClient('dev96541', 'admin', 'Nv$461vGAWFhNf')

while True:
    record_ID = input('Please enter a record ID: ')
    record_ID = sn_client.extract_record_id(record_ID)
    if record_ID != None:
        folder_name = record_ID
        result = sn_client.send_table_api_request('task', f'number={record_ID}')
        if result is not None:
            print(
                f'Found record with the ID {record_ID} in {sn_client.get_instance_url()}')
            create_folder(sn_client.get_instance_name(), record_ID)
            ticket_sys_id = result[0]['sys_id']
            attachments = sn_client.send_attachment_api_request(
                f'table_sys_id={ticket_sys_id}')
            if len(attachments) > 0:
                print(f'found {len(attachments)} attachments')
                for attachment in attachments:
                    print('downloading...')
                    f = sn_client.download_attachment(attachment['sys_id'])
                    save_file(f)
                
            else:
                print('No attachments found')
        else:
            print(
                f"No record found with the ID '{record_ID}' in {sn_client.get_instance_url()}")















