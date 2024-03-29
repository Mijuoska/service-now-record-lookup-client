from sn_client.api import SNClient
from sn_client.credential_manager import CredentialManager
from utils import create_folder, save_file, generate_jira_template, parse_instance_name
from settings import TEMPLATE_GENERATOR_ENABLED

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
            choice = parse_instance_name(choice) 
            new_choice = choice
    else:
        if choice >= 1 and choice < len(saved_instances) + 1:
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
            result = sn_client.query_records('task', f'number={record_ID}', sysparm_display_value='true') 
            if result is not None:
                record = result[0]
                print(
                    f'Found record {record["number"]} in {sn_client.get_instance_url()}')
                if TEMPLATE_GENERATOR_ENABLED:
                    options = input('(r)etrieve record information (default) or generate a (t)ext template? ')
                    if options.lower() == 't':
                        sn_client.set_fields(
                            'number,short_description,description,caller_id')
                        fields_dict = sn_client.get_fields_dict()
                        missing_fields = sn_client.get_missing_fields_in_base_table(record)
                        # For fields which are present on the inherited table but not in the base Task table, we need to do a new query to retrieve those fields
                        if len(missing_fields) > 0:
                            record = sn_client.get_record(
                                record['sys_class_name'], record['sys_id'], sysparm_display_value='true')
                            fields_dict = sn_client.populate_fields_dictionary(fields_dict, record)
                        else:
                            fields_dict = sn_client.populate_fields_dictionary(
                                fields_dict, record)

                        create_folder(sn_client.get_instance_name(), record_ID)
                        file_template = generate_jira_template(fields_dict)
                        save_file(file_template)

                    else:    
                        sn_client.set_fields(None, True)
                        missing_fields = sn_client.get_missing_fields_in_base_table(
                            record)
                        # For fields which are present on the inherited table but not in the base Task table, we need to do a new query to retrieve those fields
                        if len(missing_fields) > 0:
                            record = sn_client.get_record(
                                record['sys_class_name'], record['sys_id'], sysparm_display_value='true')
                        sn_client.display_record_data(record)
                        attachments = sn_client.query_attachments(
                            f'table_sys_id={record["sys_id"]}')
                        if len(attachments) > 0:
                            print(f'the record {record_ID} has {len(attachments)} attachments')
                            download_attachments = input('Download attachments (y: yes, no: any key) ? ')
                            if download_attachments.lower() == 'y':
                                create_folder(sn_client.get_instance_name(), record_ID)
                                for attachment in attachments:
                                    print('downloading...')
                                    f = sn_client.get_attachment(attachment['sys_id'])
                                    save_file(f)
                            else:
                                pass        

            else:
                print(f"No record found with the ID '{record_ID}' in {sn_client.get_instance_url()}")















