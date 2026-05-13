from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def append_workflow_run(event: dict, path: str) -> None:
    record = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with Path(path).open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(record) + '\n')
