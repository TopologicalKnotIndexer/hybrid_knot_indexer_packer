# 用于生成 hybrid_knot_indexer 的 json 打包文件
import json
import sys
from common_utils import gen_dict, json_pack

sys.stderr.write("\033[1;33mWARN\033[0m: do not use this function if you're not the packer.\n")

def gen_updater() -> int: # 生成更新器
    json_obj = gen_dict()
    json.dump(json_obj, open(json_pack, "w"), ensure_ascii=True, indent=4)
    return len(json_obj)

def main():
    sys.stderr.write("\033[1;34mINFO\033[0m: generating hybrid_knot_indexer_pak.json [    ].\n")
    cnt = gen_updater()
    sys.stderr.write("\033[1;34mINFO\033[0m: generating hybrid_knot_indexer_pak.json \033[1;32m[DONE]\033[0m.\n")
    sys.stderr.write("\033[1;34mINFO\033[0m: totally \033[1;32m%d\033[0m file detected.\n" % cnt)

if __name__ == "__main__":
    main()
