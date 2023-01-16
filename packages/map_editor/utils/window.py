from os import listdir
from os.path import join
from typing import Optional, List
import yaml

CONFIG_PATH = './doc/tagsDB.yaml'


def get_id_by_type(type_of_obj: str, existing_ids: List[int]) -> Optional[int]:
    with open(CONFIG_PATH) as file:
        content = yaml.safe_load(file)
        for tag in content:
            if tag['traffic_sign_type'] == type_of_obj and int(tag['tag_id']) not in existing_ids:
                return int(tag['tag_id'])


def get_list_dir(dir_path):
    try:
        entries = listdir(dir_path)
        return entries
    except FileNotFoundError as e:
        #logger.warning(e)
        return []


def get_list_dir_with_path(dir_path): return [(filename, join(dir_path, filename)) for filename in
                                              get_list_dir(dir_path)]


def get_available_translations(lang_dir_path): return {filename[len('lang_'):-len('.qm')]: path for filename, path in
                                                       get_list_dir_with_path(lang_dir_path)}
