"""Apply a JSON/base64 update pack inside the sibling hybrid repository."""

from pathlib import Path
import base64
import binascii
import json
import sys

try:
    from .common_utils import HYBRID_DIR, JSON_PACK, ROOT_FOLDER, gen_dict, safe_target
except ImportError:  # Direct execution from src.
    from common_utils import HYBRID_DIR, JSON_PACK, ROOT_FOLDER, gen_dict, safe_target


def load_pack(path: str | Path = JSON_PACK) -> dict[str, bytes]:
    pack_path = Path(path)
    if not pack_path.is_file():
        raise FileNotFoundError(pack_path)
    raw = json.loads(pack_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("update pack must be a JSON object")
    decoded: dict[str, bytes] = {}
    for relative, payload in raw.items():
        safe_target(relative)
        if not isinstance(payload, str):
            raise ValueError(f"payload for {relative!r} is not base64 text")
        try:
            decoded[relative] = base64.b64decode(payload, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError(f"invalid base64 payload for {relative!r}") from exc
    return decoded


def try_to_erase_file(
    pack: dict[str, bytes] | None = None,
    root: str | Path = ROOT_FOLDER,
    hybrid: str | Path = HYBRID_DIR,
) -> int:
    package = load_pack() if pack is None else pack
    current = gen_dict(root, hybrid)
    deleted = 0
    for relative in sorted(set(current) - set(package)):
        target = safe_target(relative, root, hybrid)
        if target.is_file():
            target.unlink()
            deleted += 1
            print(f"DELETE: {relative}", file=sys.stderr)
    return deleted


def apply_json_pack(
    pack: dict[str, bytes] | None = None,
    root: str | Path = ROOT_FOLDER,
    hybrid: str | Path = HYBRID_DIR,
) -> int:
    package = load_pack() if pack is None else pack
    changed = 0
    for relative, content in sorted(package.items()):
        target = safe_target(relative, root, hybrid)
        old_content = target.read_bytes() if target.is_file() else None
        if old_content != content:
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + ".update-tmp")
            temporary.write_bytes(content)
            temporary.replace(target)
            changed += 1
            print(f"UPDATE: {relative}", file=sys.stderr)
    return changed


def main() -> int:
    package = load_pack()
    deleted = try_to_erase_file(package)
    changed = apply_json_pack(package)
    print(f"updated={changed} deleted={deleted}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
