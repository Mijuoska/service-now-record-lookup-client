
import os
import re
from settings import ROOT_PATH, PARENT_DIR_NAME

def create_folder(parent, child):
    root_path = os.path.join(ROOT_PATH, PARENT_DIR_NAME)
    if not os.path.exists(root_path):
        os.mkdir(root_path)
        print(f'Created folder {PARENT_DIR_NAME}')
    parent_path = os.path.join(
        root_path, parent)
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
        print(f'Created parent folder {parent}')
    os.chdir(parent_path)
    child_path = os.path.join(
        parent_path, child)
    if not os.path.exists(child_path):
        os.mkdir(child_path)
        print(f'Created folder {child} in {parent}')
    else:
        print(f'Folder named {child} already exists in the folder {parent}')
    os.chdir(child_path)


def file_exists(filename):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    if os.path.exists(file_path):
        return True
    else:
        return False

def save_file(f):
    filename = f['filename']
    content = f['content']
    if type(content) == str:
        content = content.encode()
    if file_exists(filename):
        choice = input(
            f'File with the name {filename} already exists in the current directory. (c)opy or (o)verwrite (default): ')
        if choice.lower() == 'c':
            print('Creating a copy')
            has_extension = re.search(r"\.\w+", filename)
            if has_extension is not None:
                name = filename.split('.')[0]
                extension = filename.split('.')[1]
                filename = f'{name} - copy.{extension}'
            else:
                filename = f'{filename} - copy'
        elif choice.lower() == 'o':
            print('Overwriting file')
            filename = filename
        else:
            print('Invalid choice, defaulting to overwrite')
            pass
    print(f'saving file {filename}')
    saved_file = open(filename, 'w+b')
    saved_file.write(content)
    saved_file.close()
    print('Completed')

def generate_jira_template(fields_dictionary):
    file_template = {}
    content = f'Summary: {fields_dictionary["short_description"]}\n\n'
    content += f'Reporter: {fields_dictionary["caller_id"]["display_value"]}\n\n'
    content += f'Description: \n\n{fields_dictionary["number"]}\n\n'
    content += f'\"{fields_dictionary["description"].strip()}\"\n\n'
    content += f'Incident:\nCause:\nFix:\n\n'
    content += f'Update sets:\n{fields_dictionary["number"]} {fields_dictionary["short_description"]}'
    file_template["content"] = content
    file_template["filename"] = f'{fields_dictionary["number"]} jira draft.txt'
    return file_template



    
