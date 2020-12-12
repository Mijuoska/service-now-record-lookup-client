from sn_client.sn_client import SNClient
from utils import create_folder, save_file


sn_client = SNClient('dev96541', 'admin', 'Nv$461vGAWFhNf')

while True:
    record_ID = input('Please enter a record ID: ')
    record_ID = sn_client.extract_record_id(record_ID)
    if record_ID != None:
        folder_name = record_ID
        create_folder(sn_client.get_instance_name(), record_ID)
        attachments = sn_client.download_attachment_from_ticket(record_ID)
        for attachment in attachments:
            save_file(attachment)















