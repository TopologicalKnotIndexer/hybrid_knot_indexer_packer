import os
import sys
import base64

dirnow      = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(dirnow))
hybrid_dir  = os.path.join(root_folder, "hybrid_knot_indexer")
json_pack   = os.path.join(dirnow, "hybrid_knot_indexer_pak.json")

if not os.path.isdir(root_folder):
    sys.stderr.write("\033[1;31mERROR\033[0m: hybrid_knot_indexer not found.\n")
    exit(1)

# 检查不动产
javakh_ori_temp_dir = os.path.join(root_folder, "hybrid_knot_indexer", "src", "khovanov-indexer",  "src", "khovanov-solver",  "src", "javakh_ori_temp")
sage_dir            = os.path.join(root_folder, "hybrid_knot_indexer", "src", "HOMFLY-PT-indexer", "src", "HOMFLY-PT-solver", "src", "x86_64-sage-minimal", "src", "bin", "portable_sage", "sage")

if not os.path.isdir(javakh_ori_temp_dir):
    sys.stderr.write("\033[1;31mERROR\033[0m: javakh_ori_temp not found in hybrid_knot_indexer.\n")
    exit(1)

if not os.path.isdir(sage_dir):
    sys.stderr.write("\033[1;31mERROR\033[0m: sage not found in hybrid_knot_indexer.\n")
    exit(1)

def should_ignore(filepath: str) -> bool:
    basename = os.path.basename(filepath).lower()
    if basename.startswith("."):
        return True
    if basename.endswith(".pyc"):
        return True
    if basename in ["javakh_ori_temp", "knot-pdcode", "sage"]:
        return True
    return False

def scan_dir(folder_name: str) -> list:
    assert os.path.isdir(folder_name)
    if should_ignore(folder_name): # 我们不打包隐藏文件或文件夹
        return []
    arr = []
    for file in os.listdir(folder_name):
        filepath = os.path.join(folder_name, file)
        if should_ignore(filepath): # 不打包隐藏文件
            continue
        if os.path.isfile(filepath): # 考虑文件
            arr.append(filepath)
        if os.path.isdir(filepath): # 考虑文件夹
            arr += scan_dir(filepath)
    return arr

def scan_all() -> list:
    arr = []
    for file in  scan_dir(hybrid_dir):
        arr.append(os.path.relpath(file, root_folder))
    return arr

def fetch_file(filepath) -> str: # 返回字符串形式的 bas64
    assert os.path.isfile(filepath)
    bin_content = open(filepath, "rb").read()
    return base64.b64encode(bin_content).decode()

def gen_dict() -> dict: # 生成 json 对象
    dic = {}
    for filepath in scan_all():
        dic[filepath] = fetch_file(os.path.join(root_folder, filepath))
    return dic
