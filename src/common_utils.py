"""Shared deterministic and path-safe packer utilities."""

from pathlib import Path, PurePosixPath
import base64


HERE = Path(__file__).resolve().parent
ROOT_FOLDER = HERE.parents[1]
HYBRID_DIR = ROOT_FOLDER / "hybrid_knot_indexer"
JSON_PACK = HERE / "hybrid_knot_indexer_pak.json"

# Backward-compatible string names used by the original scripts.
root_folder = str(ROOT_FOLDER)
hybrid_dir = str(HYBRID_DIR)
json_pack = str(JSON_PACK)


def should_ignore(path: str | Path) -> bool:
    name = Path(path).name.lower()
    return (
        name.startswith(".")
        or name.endswith(".pyc")
        or name in {"javakh_ori_temp", "knot-pdcode", "knot-pdcode.exe", "sage"}
    )


def scan_dir(folder_name: str | Path) -> list[Path]:
    folder = Path(folder_name)
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    if should_ignore(folder):
        return []
    files: list[Path] = []
    for path in sorted(folder.iterdir(), key=lambda item: item.name):
        if should_ignore(path):
            continue
        if path.is_symlink():
            raise ValueError(f"refusing to package symbolic link: {path}")
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(scan_dir(path))
    return files


def scan_all(
    root: str | Path = ROOT_FOLDER, hybrid: str | Path = HYBRID_DIR
) -> list[str]:
    root_path = Path(root).resolve()
    hybrid_path = Path(hybrid).resolve()
    if not hybrid_path.is_dir():
        raise NotADirectoryError(f"hybrid_knot_indexer not found: {hybrid_path}")
    try:
        hybrid_path.relative_to(root_path)
    except ValueError as exc:
        raise ValueError("hybrid directory must be inside the selected root") from exc
    return [path.relative_to(root_path).as_posix() for path in scan_dir(hybrid_path)]


def fetch_file(filepath: str | Path) -> str:
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(path)
    return base64.b64encode(path.read_bytes()).decode("ascii")


def gen_dict(
    root: str | Path = ROOT_FOLDER, hybrid: str | Path = HYBRID_DIR
) -> dict[str, str]:
    root_path = Path(root).resolve()
    return {
        relative: fetch_file(root_path / PurePosixPath(relative))
        for relative in scan_all(root_path, hybrid)
    }


def safe_target(
    relative: str,
    root: str | Path = ROOT_FOLDER,
    hybrid: str | Path = HYBRID_DIR,
) -> Path:
    if not isinstance(relative, str):
        raise TypeError("package paths must be strings")
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or not posix.parts:
        raise ValueError(f"unsafe package path: {relative!r}")
    root_path = Path(root).resolve()
    hybrid_path = Path(hybrid).resolve()
    target = (root_path / Path(*posix.parts)).resolve()
    try:
        target.relative_to(hybrid_path)
    except ValueError as exc:
        raise ValueError(f"package path escapes hybrid_knot_indexer: {relative!r}") from exc
    return target
