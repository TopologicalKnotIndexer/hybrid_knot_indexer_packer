# 用于将 hybrid_knot_indexer_pak.json 中的数据部署到文件夹中
import base64
import json
import os
import sys
from common_utils import gen_dict, root_folder, json_pack

if not os.path.isfile(json_pack):
    sys.stderr.write("\033[1;31mERROR\033[0m: hybrid_knot_indexer_pak.json not found.\n")
    exit(1)

def safe_get_file(filepath: str) -> bytes:
    if os.path.isfile(filepath):
        return open(filepath, "rb").read()
    else:
        return b''

def create_path_if_not_exist(rawdirname: str): # 一定要注意目标文件夹可能不存在
    if not os.path.isdir(rawdirname):
        os.makedirs(rawdirname)

def try_to_erase_file(): # 考虑删除多余文件
    json_obj = json.load(open(json_pack, "r"))
    real_obj = gen_dict()
    cnt = 0
    for file in real_obj:
        if json_obj.get(file) is None:
            sys.stderr.write("\033[1;33mDELT\033[0m: file \033[1;32m%s\033[0m is deleted.\n" % file)
            filepath = os.path.join(root_folder, file)
            os.remove(filepath) # 删除指定的文件
            cnt += 1
    sys.stderr.write("\033[1;34mINFO\033[0m: totally \033[1;32m%d\033[0m file deleted.\n" % cnt)

def apply_json_pack():
    json_obj = json.load(open(json_pack, "r"))
    cnt = 0
    for file in json_obj:
        new_content = base64.b64decode(json_obj[file])
        rawpath     = os.path.join(root_folder, file)
        old_content = safe_get_file(rawpath)
        assert isinstance(new_content, bytes)
        assert isinstance(old_content, bytes)
        if new_content != old_content or (old_content == b''):
            sys.stderr.write("\033[1;32mUPDT\033[0m: file updated: \033[1;32m%s\033[0m.\n" % file)
            rawdirname = os.path.dirname(rawpath)
            create_path_if_not_exist(rawdirname)
            open(rawpath, "wb").write(new_content) # 写入新内容
            cnt += 1
    sys.stderr.write("\033[1;34mINFO\033[0m: totally \033[1;32m%d\033[0m file changed.\n" % cnt)

if __name__ == "__main__":
    try_to_erase_file()
    apply_json_pack()
