"""Generate the JSON/base64 update pack for hybrid_knot_indexer."""
import json
import sys
try:
    from .common_utils import gen_dict, json_pack
except ImportError:  # Direct execution from src.
    from common_utils import gen_dict, json_pack

sys.stderr.write("\033[1;33mWARN\033[0m: do not use this function if you're not the packer.\n")

def gen_updater() -> int:
    json_obj = gen_dict()
    with open(json_pack, "w", encoding="utf-8") as stream:
        json.dump(json_obj, stream, ensure_ascii=True, indent=4, sort_keys=True)
    return len(json_obj)

def main() -> None:
    sys.stderr.write("\033[1;34mINFO\033[0m: generating hybrid_knot_indexer_pak.json [    ].\n")
    cnt = gen_updater()
    sys.stderr.write("\033[1;34mINFO\033[0m: generating hybrid_knot_indexer_pak.json \033[1;32m[DONE]\033[0m.\n")
    sys.stderr.write("\033[1;34mINFO\033[0m: totally \033[1;32m%d\033[0m file detected.\n" % cnt)

if __name__ == "__main__":
    main()
