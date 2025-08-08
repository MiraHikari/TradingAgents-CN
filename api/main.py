#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

# Logging
from tradingagents.utils.logging_manager import get_logger

# Use existing API functions from the project
from tradingagents.api.stock_api import (
    get_stock_info,
    get_all_stocks,
    get_stock_data,
    search_stocks,
    get_market_summary,
    check_service_status,
)

logger = get_logger("api")

# Determine version
PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = PROJECT_ROOT / "VERSION"
if VERSION_FILE.exists():
    API_VERSION = VERSION_FILE.read_text(encoding="utf-8").strip()
else:
    API_VERSION = os.getenv("TRADINGAGENTS_VERSION", "0.0.0")

app = FastAPI(
    title="TradingAgents-CN API",
    version=API_VERSION,
    description="TradingAgents-CN 股票分析平台的轻量API服务",
    contact={
        "name": "TradingAgents-CN",
        "url": "https://github.com/",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Enable permissive CORS for development; tighten as needed in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])  # Simple health probe
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": "tradingagents-api", "version": API_VERSION}


@app.get("/status", tags=["system"])  # Detailed dependency status
def status() -> Dict[str, Any]:
    try:
        return check_service_status()
    except Exception as exc:  # pragma: no cover - best-effort status
        logger.warning(f"Status check failed: {exc}")
        return {"service_available": False, "error": str(exc)}


@app.get("/stocks/{stock_code}", tags=["stocks"])  # Get basic info of a single stock
def get_stock(stock_code: str) -> Dict[str, Any]:
    result = get_stock_info(stock_code)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=404, detail=result)
    return result


@app.get("/stocks", tags=["stocks"])  # List stocks with basic paging
def list_stocks(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip from the beginning"),
) -> List[Dict[str, Any]]:
    items = get_all_stocks()
    # tolerate error passthrough
    if isinstance(items, list) and items and isinstance(items[0], dict) and items[0].get("error"):
        raise HTTPException(status_code=503, detail=items[0])
    # ensure list
    items = items if isinstance(items, list) else [items]
    return items[offset : offset + limit]


@app.get("/stocks/search", tags=["stocks"])  # Search stocks by keyword
def search(q: str = Query(..., min_length=1, description="Keyword to search by code or name")) -> List[Dict[str, Any]]:
    return search_stocks(q)


@app.get(
    "/stocks/{stock_code}/history",
    response_class=PlainTextResponse,  # keep original return format from underlying service
    tags=["stocks"],
)
def history(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
) -> str:
    data = get_stock_data(stock_code, start_date=start_date, end_date=end_date)
    if isinstance(data, str) and data.startswith("❌"):
        raise HTTPException(status_code=503, detail=data)
    return data


@app.get("/market/summary", tags=["market"])  # Market overview
def market_summary() -> Dict[str, Any]:
    summary = get_market_summary()
    if isinstance(summary, dict) and summary.get("error"):
        raise HTTPException(status_code=503, detail=summary)
    return summary


# Convenience root endpoint
@app.get("/", include_in_schema=False)
def root() -> Dict[str, Any]:
    return {
        "message": "Welcome to TradingAgents-CN API",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "version": API_VERSION,
    }