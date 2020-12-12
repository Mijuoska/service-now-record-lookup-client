
import os
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
        print(f'Folder named {child} already exists in {parent}')
    os.chdir(child_path)
