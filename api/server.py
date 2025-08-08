#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

import uvicorn

# Ensure project root is on sys.path for imports when running directly
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main(host: str = "0.0.0.0", port: int = 8000, reload: Optional[bool] = None) -> None:
    if reload is None:
        reload = os.getenv("TRADINGAGENTS_RELOAD", "false").lower() in {"1", "true", "yes"}

    uvicorn.run(
        "api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=os.getenv("TRADINGAGENTS_API_LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    main()