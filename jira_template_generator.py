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
                    f'Found record {record_ID} in {sn_client.get_instance_url()}')
                record = result[0]
                sn_client.set_fields('number,short_description,description,caller_id')
                fields = sn_client.get_fields()
                fields_dict = sn_client.get_fields_dict(fields)
                missing_fields = []
                for field in fields:
                    if record.get(field) is not None:
                        fields_dict[field] = record.get(field)
                    else:
                        missing_fields.append(field)
                # For fields which are present on the inherited table but not in the base Task table, we need to do a new query to retrieve those fields
                if len(missing_fields) > 0:
                    new_record = sn_client.get_record(record['sys_class_name'], record['sys_id'], sysparm_display_value='true')
                    for missing_field in missing_fields:
                        fields_dict[missing_field] = new_record.get(missing_field)
                create_folder(sn_client.get_instance_name(), record_ID)
                result_file = {}
                content = f'Summary: {fields_dict["short_description"]}\n\n'
                content += f'Reporter: {fields_dict["caller_id"]["display_value"]}\n\n'
                content += f'Description: \n\n{fields_dict["number"]}\n\n'
                content += f'\"{fields_dict["description"].strip()}\"\n\n'
                content += f'Incident:\nCause:\nFix:\n\n'
                content += f'Update sets:\n{fields_dict["number"]} {fields_dict["short_description"]}'
                result_file["content"] = content
                result_file["filename"] = f'{fields_dict["number"]} jira draft.txt'
                save_file(result_file)
            else:
                print(f"No record found with the ID '{record_ID}' in {sn_client.get_instance_url()}")

