from sn_client.api import SNClient
from sn_client.credential_manager import CredentialManager
from utils import create_folder, save_file

while True:
    cred_manager = CredentialManager()
    saved_instances = cred_manager.fetch_all_instances()
    choices = {}
    for n, instance in enumerate(saved_instances, start=1):
        choices[n] = instance[0]

    choice = input(f'choose an instance: {choices}, type a new instance name or q to (q)uit: ')
    existing_choice = ""
    new_choice = ""

    try:
        choice = int(choice)
    except ValueError:
        if choice == 'q':
            break
        else:
            new_choice = choice
    else:
        if choice >= 1 and choice <= len(saved_instances) + 1:
            existing_choice = choice
        else:
            print('Invalid choice')
            exit()



    if existing_choice:
        selected_instance = choices[existing_choice]
        credentials = cred_manager.fetch_credentials_for_instance(selected_instance)
        username = credentials[0]
        password = credentials[1]
        sn_client = SNClient(selected_instance, username, password)
    else:
        selected_instance = new_choice
        username = input('Please enter instance username: ')
        password = input('Please enter instance password: ')
        save_credentials = input('Save these credentials? Y to confirm, any other key to disconfirm: ')
        if save_credentials.lower() == 'y':
            cred_manager.save_instance_credentials((selected_instance, username, password,))
        else:
            pass
        sn_client = SNClient(selected_instance, username, password)
        sn_client.test_connection()


    while True:
        record_ID = input('Please enter a record ID or q to (q)uit: ')
        if record_ID == None or record_ID == 'q':
            break
        else:
            record_ID = sn_client.extract_record_id(record_ID)           
            folder_name = record_ID
            result = sn_client.send_table_api_request('task', f'number={record_ID}')
            if result is not None:
                print(
                    f'Found record {record_ID} in {sn_client.get_instance_url()} with the following values')
                sn_client.display_record_data(result[0])
                ticket_sys_id = result[0]['sys_id']
                attachments = sn_client.send_attachment_api_request(
                    f'table_sys_id={ticket_sys_id}')
                if len(attachments) > 0:
                    print(f'the record {record_ID} has {len(attachments)} attachments')
                    download_attachments = input('Download attachments (y: yes, no: any key) ? ')
                    if download_attachments.lower() == 'y':
                        create_folder(sn_client.get_instance_name(), record_ID)
                        for attachment in attachments:
                            print('downloading...')
                            f = sn_client.download_attachment(attachment['sys_id'])
                            save_file(f)
                    else:
                        pass        
                
            else:
                print(f"No record found with the ID '{record_ID}' in {sn_client.get_instance_url()}")















