# 用于将 hybrid_knot_indexer_pak.json 中的数据部署到文件夹中
import base64
import json
import os
import sys
dirnow      = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.join(dirnow, "hybrid_knot_indexer")
json_pack   = os.path.join(dirnow, "hybrid_knot_indexer_pak.json")

if not os.path.isdir(root_folder):
    sys.stderr.write("\033[1;31mERROR\033[0m: hybrid_knot_indexer not found.\n")
    exit(1)

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

def apply_json_pack(dry_run=True):
    json_obj = json.load(open(json_pack, "r"))
    cnt = 0
    for file in json_obj:
        new_content = base64.b64decode(json_obj[file])
        rawpath     = os.path.join(dirnow, file)
        old_content = safe_get_file(rawpath)
        assert isinstance(new_content, bytes)
        assert isinstance(old_content, bytes)
        if new_content != old_content or (old_content == b''):
            sys.stderr.write("\033[1;32mCHNG\033[0m: file changed: %s.\n" % file)
            if not dry_run:
                rawdirname = os.path.dirname(rawpath)
                create_path_if_not_exist(rawdirname)
                open(rawpath, "wb").write(new_content) # 写入新内容
            cnt += 1
    sys.stderr.write("\033[1;34mINFO\033[0m: totally \033[1;32m%d\033[0m file changed.\n" % cnt)

if __name__ == "__main__":
    apply_json_pack(False) # 写文件
