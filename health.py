# src/core/health.py

"""Memory health monitoring utilities."""

import asyncio
from datetime import datetime
from typing import Dict, Any


async def collect_health_metrics(memory) -> Dict[str, Any]:
    """Collect current health metrics from memory."""
    health = await memory.get_health()
    health["collected_at"] = datetime.now().isoformat()
    return health


async def health_monitor_loop(memory, interval: int = 30):
    """Continuous health monitoring loop."""
    while True:
        metrics = await collect_health_metrics(memory)
        print(f"[Health] Records: {metrics['total_records']}, "
              f"Size: {metrics['total_size_bytes'] / 1024:.1f}KB, "
              f"Ratio: {metrics['compression_ratio']:.1%}")
        await asyncio.sleep(interval)
