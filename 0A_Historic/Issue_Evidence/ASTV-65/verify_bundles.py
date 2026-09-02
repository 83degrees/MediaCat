"""Verify every ASTV-65 bundle byte against its manifest and source."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HOME_ASSISTANT_ROOT = ROOT.parent
MANIFEST = Path(__file__).with_name("bundle-manifest.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = manifest["files"]
    assert manifest["issue"] == "ASTV-65"
    assert manifest["status"] == "prepared-inactive"
    assert manifest["bundle_path_base"] == "MediaCat/"
    assert len(rows) == 18
    assert sum(row["bundle"] == "deployment" for row in rows) == 9
    assert sum(row["bundle"] == "rollback" for row in rows) == 9

    checked = []
    for row in rows:
        bundle_path = ROOT / row["bundle_path"]
        source_path = HOME_ASSISTANT_ROOT / row["source_path"]
        expected_target = "/config/" + row["bundle_path"].split("/config/", 1)[1]
        assert row["target_path"] == expected_target
        assert bundle_path.stat().st_size == row["size"]
        assert source_path.stat().st_size == row["size"]
        assert sha256(bundle_path) == row["sha256"]
        assert sha256(source_path) == row["sha256"]
        assert bundle_path.read_bytes() == source_path.read_bytes()
        checked.append(row["bundle_path"])

    print(
        json.dumps(
            {
                "status": "passed",
                "files_checked": len(checked),
                "deployment_files": 9,
                "rollback_files": 9,
                "byte_equal_to_sources": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
