"""Atomic persistence helpers for authoritative current-run state."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

CURRENT_STATE_VERSION = "last30days-current/v1"


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON via same-directory fsync + replace with owner-only mode."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    try:
        os.chmod(temporary, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            try:
                directory_fd = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                # The file replacement is already atomic; some filesystems do
                # not permit directory fsync.
                pass
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
