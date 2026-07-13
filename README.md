# hybrid-knot-indexer-packer

Create and apply offline JSON/base64 updates for a sibling
`hybrid_knot_indexer` checkout.

## Layout and requirements

- Python 3.10 or newer.
- `hybrid_knot_indexer_packer` and `hybrid_knot_indexer` must be sibling
  directories under the same parent.
- No Git submodule checkout is required; both repositories are independent.

The committed `src/hybrid_knot_indexer_pak.json` contains relative paths and
base64 file payloads. Heavy runtime assets such as Sage, JavaKh binaries, and
locally compiled `knot-pdcode` executables are intentionally excluded.

## Apply the pack

```bash
python src/updater.py
```

The updater writes only inside the sibling `hybrid_knot_indexer` directory.
Absolute paths, `..` components, symbolic-link escapes, non-base64 payloads,
and paths targeting any other sibling are rejected. Changed files are written
through a temporary file and atomically replaced; scanned files absent from
the pack are removed.

## Generate a pack

Maintainers can regenerate the pack with:

```bash
python src/mytar.py
```

Directory traversal is sorted, so equivalent source trees produce stable JSON
key order. Do not regenerate a release pack from an unreviewed working tree.

## Development

Path safety and update behavior use only the standard library and are covered
with temporary-directory tests:

```bash
python -m unittest discover -s tests -v
```

